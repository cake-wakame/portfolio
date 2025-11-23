# PR: Add Render deploy configuration and production settings

変更概要:
- settings.py を本番向けに修正:
  - SECRET_KEY, DEBUG, ALLOWED_HOSTS を環境変数で制御するように変更
  - WhiteNoise ミドルウェアを追加して静的ファイルを配信
  - STATIC_ROOT と STATICFILES_STORAGE を追加
  - DATABASE_URL が設定されていれば dj-database-url でデータベース接続を上書き
- Render デプロイ用ファイルを追加:
  - render.yaml, Dockerfile, entrypoint.sh, .dockerignore, requirements.txt（production向けパッケージを追加）
- settings の差分は settings.py.patch にまとめてあります.

動作確認手順（ローカル）:
1. SECRET_KEY を環境変数にセットして DEBUG=False にして起動するか、ローカルでは DEBUG=True を使用する.
2. python manage.py collectstatic を実行して staticfiles が生成されることを確認.
3. docker build -t portfolio . してコンテナ起動確認.

Render デプロイ手順:
1. 新ブランチ (feature/deploy-render) にコミット & push（既にブランチ作成済み）.
2. Render に接続してサービスを作成. render.yaml があるため Docker ビルドでデプロイされます.
3. Render の Service settings で環境変数を追加:
   - SECRET_KEY
   - DEBUG=false
   - ALLOWED_HOSTS=<your-render-service-name>.onrender.com
   - DATABASE_URL (Render Postgres を使う場合)