*** Begin Patch
*** Update File: portfolio/settings.py
@@
-SECRET_KEY = 'REPLACE_ME_WITH_YOUR_SECRET_KEY'
+import os
+import dj_database_url
+
+# SECURITY
+# SECRET_KEY は環境変数から取得。ローカル開発時は既存の値かデフォルトを使います。
+SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-for-local')
@@
-DEBUG = True
+# DEBUG は環境変数で制御（Render 等の本番では False にする）
+DEBUG = os.environ.get('DEBUG', 'False') == 'True'
@@
-ALLOWED_HOSTS = []
+# ALLOWED_HOSTS を環境変数から設定（カンマ区切り）
+ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')
*** End Patch
