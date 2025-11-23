FROM nginx:alpine
LABEL maintainer="cake-wakame"

# 空にしてからコピー（既存の default index を消す）
RUN rm -rf /usr/share/nginx/html/*

# 全ファイルを公開ディレクトリへコピー
COPY . /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
