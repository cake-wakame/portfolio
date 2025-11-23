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

*** Begin Patch
*** Update File: portfolio/settings.py
@@
 MIDDLEWARE = [
-    'django.middleware.security.SecurityMiddleware',
+    'django.middleware.security.SecurityMiddleware',
+    # WhiteNoise を最初の方に入れることで静的ファイルを効率的に配信します
+    'whitenoise.middleware.WhiteNoiseMiddleware',
     'django.contrib.sessions.middleware.SessionMiddleware',
     'django.middleware.common.CommonMiddleware',
     'django.middleware.csrf.CsrfViewMiddleware',
*** End Patch

*** Begin Patch
*** Update File: portfolio/settings.py
@@
 # Static files (CSS, JavaScript, Images)
 # https://docs.djangoproject.com/en/4.2/howto/static-files/
 
-STATIC_URL = '/static/'
+STATIC_URL = '/static/'
+# 本番用に collectstatic が吐くディレクトリを指定
+STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
+# WhiteNoise 用に圧縮・キャッシュ可能なストレージを利用
+STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
@@
-DATABASES = {
-    'default': {
-        'ENGINE': 'django.db.backends.sqlite3',
-        'NAME': BASE_DIR / 'db.sqlite3',
-    }
-}
+DATABASES = {
+    'default': {
+        'ENGINE': 'django.db.backends.sqlite3',
+        'NAME': BASE_DIR / 'db.sqlite3',
+    }
+}
+
+# If DATABASE_URL is present (e.g. Render Postgres service), override DATABASES
+DATABASE_URL = os.environ.get('DATABASE_URL')
+if DATABASE_URL:
+    DATABASES['default'] = dj_database_url.parse(DATABASE_URL, conn_max_age=600)
*** End Patch
