変更概要:
- settings.py を本番向けに修正:
  - SECRET_KEY, DEBUG, ALLOWED_HOSTS を環境変数で制御するように変更
  - WhiteNoise ミドルウェアを追加して静的ファイルを配信
  - STATIC_ROOT と STATICFILES_STORAGE を追加
  - DATABASE_URL が設定されていれば dj-database-url でデータベース接続を上書き
- Render デプロイ用ファイルを追加:
  - render.yaml, Dockerfile, entrypoint.sh, .dockerignore
- requirements.txt に production 用パッケージを追加（whitenoise, gunicorn, dj-database-url, psycopg2-binary）

動作確認手順（ローカル）:
1. SECRET_KEY を環境変数にセットして DEBUG=False にして起動するか、ローカルでは DEBUG=True を使用する。
2. python manage.py collectstatic を実行して staticfiles が生成されることを確認。
3. docker build -t portfolio . してコンテナ起動確認。

Render デプロイ手順:
1. 新ブランチを作成 (例: feature/deploy-render)。
2. 上記ファイルを追加してコミット・push。
3. GitHub 上で PR を作成。
4. Render にこのリポジトリを接続し、render.yaml を検出させる。環境変数をサービス設定で追加:
   - SECRET_KEY
   - DEBUG=false
   - ALLOWED_HOSTS=<your-render-service-name>.onrender.com
   - DATABASE_URL (もし Render Postgres を使うなら自動で設定されます)
