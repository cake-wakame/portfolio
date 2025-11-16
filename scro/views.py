from django.shortcuts import render

def game(request):
    """横スクロールアクションゲーム"""
    return render(request, 'scro/game.html')