from django.shortcuts import render, redirect
from django.http import JsonResponse
import random
import json

# カードのスート（マーク）とランク（数字・絵札）
SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
RANK_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
}

def create_deck():
    """トランプのデッキを作成"""
    return [{'suit': suit, 'rank': rank} for suit in SUITS for rank in RANKS]

def evaluate_hand(cards):
    """手札の役を判定"""
    if len(cards) != 5:
        return (0, '役なし', [])
    
    ranks = [card['rank'] for card in cards]
    suits = [card['suit'] for card in cards]
    rank_values = sorted([RANK_VALUES[r] for r in ranks], reverse=True)
    rank_counts = {}
    for r in ranks:
        rank_counts[r] = rank_counts.get(r, 0) + 1
    
    is_flush = len(set(suits)) == 1
    is_straight = False
    
    # ストレート判定（A-2-3-4-5も含む）
    if rank_values == list(range(rank_values[0], rank_values[0]-5, -1)):
        is_straight = True
    elif rank_values == [14, 5, 4, 3, 2]:  # A-2-3-4-5
        is_straight = True
        rank_values = [5, 4, 3, 2, 1]
    
    counts = sorted(rank_counts.values(), reverse=True)
    
    # 役の判定
    if is_straight and is_flush:
        if rank_values[0] == 14:
            return (10, 'ロイヤルストレートフラッシュ', rank_values)
        return (9, 'ストレートフラッシュ', rank_values)
    elif counts == [4, 1]:
        return (8, 'フォーカード', rank_values)
    elif counts == [3, 2]:
        return (7, 'フルハウス', rank_values)
    elif is_flush:
        return (6, 'フラッシュ', rank_values)
    elif is_straight:
        return (5, 'ストレート', rank_values)
    elif counts == [3, 1, 1]:
        return (4, 'スリーカード', rank_values)
    elif counts == [2, 2, 1]:
        return (3, 'ツーペア', rank_values)
    elif counts == [2, 1, 1, 1]:
        return (2, 'ワンペア', rank_values)
    else:
        return (1, 'ハイカード', rank_values)

def compare_hands(player_hand, computer_hand):
    """手札を比較して勝敗を判定"""
    p_score, p_name, p_values = evaluate_hand(player_hand)
    c_score, c_name, c_values = evaluate_hand(computer_hand)
    
    if p_score > c_score:
        return 'win', p_name, c_name
    elif p_score < c_score:
        return 'lose', p_name, c_name
    else:
        # 同じ役の場合、カードの強さで比較
        for p_val, c_val in zip(p_values, c_values):
            if p_val > c_val:
                return 'win', p_name, c_name
            elif p_val < c_val:
                return 'lose', p_name, c_name
        return 'draw', p_name, c_name

def index(request):
    """ゲームメイン画面"""
    # セッション初期化
    if 'chips' not in request.session:
        request.session['chips'] = 1000
    
    # ゲームオーバーチェック
    if request.session['chips'] <= 0:
        return redirect('poker:game_over')
    
    # 新しいゲーム開始
    if 'game_state' not in request.session or request.GET.get('new_game'):
        deck = create_deck()
        random.shuffle(deck)
        
        player_hand = deck[:5]
        computer_hand = deck[5:10]
        remaining_deck = deck[10:]
        
        request.session['deck'] = remaining_deck
        request.session['player_hand'] = player_hand
        request.session['computer_hand'] = computer_hand
        request.session['game_state'] = 'betting'
        request.session['bet_amount'] = 0
        request.session['cards_to_exchange'] = []
        request.session.modified = True
    
    context = {
        'chips': request.session['chips'],
        'player_hand': request.session.get('player_hand', []),
        'game_state': request.session.get('game_state', 'betting'),
        'bet_amount': request.session.get('bet_amount', 0),
        'result': request.session.get('result'),
    }
    
    # 結果表示後はクリア
    if 'result' in request.session:
        del request.session['result']
        request.session.modified = True
    
    return render(request, 'poker/index.html', context)

def place_bet(request):
    """ベットを行う"""
    if request.method == 'POST':
        bet = int(request.POST.get('bet', 0))
        
        if bet > request.session['chips']:
            return JsonResponse({'error': 'チップが足りません'}, status=400)
        
        if bet <= 0:
            return JsonResponse({'error': '有効なベット額を入力してください'}, status=400)
        
        request.session['bet_amount'] = bet
        request.session['game_state'] = 'exchange'
        request.session.modified = True
        
        return JsonResponse({'success': True, 'bet_amount': bet})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def exchange_cards(request):
    """カードを交換する"""
    if request.method == 'POST':
        cards_to_exchange = json.loads(request.POST.get('cards', '[]'))
        
        player_hand = request.session['player_hand']
        deck = request.session['deck']
        
        # カードを交換
        new_cards = []
        for i in sorted(cards_to_exchange, reverse=True):
            if 0 <= i < len(player_hand):
                player_hand.pop(i)
                if deck:
                    new_cards.append(deck.pop())
        
        player_hand.extend(new_cards)
        
        request.session['player_hand'] = player_hand
        request.session['deck'] = deck
        request.session['game_state'] = 'result'
        request.session.modified = True
        
        # コンピュータもカードを交換（ランダムに0〜3枚）
        computer_hand = request.session['computer_hand']
        num_exchange = random.randint(0, 3)
        for _ in range(num_exchange):
            if computer_hand and deck:
                computer_hand.pop(random.randint(0, len(computer_hand)-1))
                computer_hand.append(deck.pop())
        
        request.session['computer_hand'] = computer_hand
        
        # 勝敗判定
        result, player_hand_name, computer_hand_name = compare_hands(
            request.session['player_hand'],
            request.session['computer_hand']
        )
        
        bet_amount = request.session['bet_amount']
        
        if result == 'win':
            request.session['chips'] += bet_amount
            result_text = '勝ち！'
        elif result == 'lose':
            request.session['chips'] -= bet_amount
            result_text = '負け...'
        else:
            result_text = '引き分け'
        
        request.session.modified = True
        
        return JsonResponse({
            'success': True,
            'result': result_text,
            'player_hand': request.session['player_hand'],
            'computer_hand': request.session['computer_hand'],
            'player_hand_name': player_hand_name,
            'computer_hand_name': computer_hand_name,
            'chips': request.session['chips']
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def hand_ranking(request):
    """役の一覧ページ"""
    rankings = [
        {
            'rank': 1,
            'name': 'ロイヤルストレートフラッシュ',
            'description': '同じスートの10、J、Q、K、Aの組み合わせ',
            'example': '♠A ♠K ♠Q ♠J ♠10'
        },
        {
            'rank': 2,
            'name': 'ストレートフラッシュ',
            'description': '同じスートで連続する5枚のカード',
            'example': '♥9 ♥8 ♥7 ♥6 ♥5'
        },
        {
            'rank': 3,
            'name': 'フォーカード',
            'description': '同じランクのカード4枚',
            'example': '♠K ♥K ♦K ♣K ♠3'
        },
        {
            'rank': 4,
            'name': 'フルハウス',
            'description': '同じランクのカード3枚と別のランクのカード2枚',
            'example': '♠Q ♥Q ♦Q ♣8 ♠8'
        },
        {
            'rank': 5,
            'name': 'フラッシュ',
            'description': '同じスートの5枚のカード',
            'example': '♦A ♦10 ♦7 ♦5 ♦2'
        },
        {
            'rank': 6,
            'name': 'ストレート',
            'description': '連続する5枚のカード（スートは問わない）',
            'example': '♠10 ♥9 ♦8 ♣7 ♠6'
        },
        {
            'rank': 7,
            'name': 'スリーカード',
            'description': '同じランクのカード3枚',
            'example': '♠7 ♥7 ♦7 ♣K ♠2'
        },
        {
            'rank': 8,
            'name': 'ツーペア',
            'description': '同じランクのカード2枚が2組',
            'example': '♠J ♥J ♦4 ♣4 ♠A'
        },
        {
            'rank': 9,
            'name': 'ワンペア',
            'description': '同じランクのカード2枚',
            'example': '♠9 ♥9 ♦K ♣7 ♠3'
        },
        {
            'rank': 10,
            'name': 'ハイカード',
            'description': '上記のいずれにも当てはまらない場合',
            'example': '♠A ♥K ♦8 ♣5 ♠2'
        },
    ]
    
    return render(request, 'poker/hand_ranking.html', {'rankings': rankings})

def game_over(request):
    """ゲームオーバー画面"""
    return render(request, 'poker/game_over.html')

def reset_game(request):
    """ゲームをリセット"""
    request.session.flush()
    return redirect('poker:index')