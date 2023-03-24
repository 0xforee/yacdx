ARG COMMIT_SHA=""
FROM --platform=linux/amd64 node:alpine AS builder
WORKDIR /app
RUN npm i -g pnpm
COPY pnpm-lock.yaml package.json ./
COPY ./patches/ ./patches/
RUN pnpm i
COPY . .
RUN pnpm build \
  # remove source maps - people like small image
  && rm public/*.map || true
FROM alpine
RUN set -eux && sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories
RUN apk add --no-cache python3-dev py3-pip curl bash nginx uwsgi uwsgi-python3  \
    && ln -sf /usr/share/zoneinfo/${TZ} /etc/localtime \
    && echo "${TZ}" > /etc/timezone \
    && ln -sf /usr/bin/python3 /usr/bin/python \
WORKDIR /app
COPY clash-traffic .
RUN pip3 install -r requirements.txt
VOLUME ["/config"]
VOLUME ["/logs"]
COPY docker/nginx-default.conf /etc/nginx/http.d/default.conf
RUN rm -rf /usr/share/nginx/html/*
COPY --from=builder /app/public /usr/share/nginx/html
ENV YACD_DEFAULT_BACKEND "http://127.0.0.1:9090"
ADD docker-entrypoint.sh /
CMD ["/docker-entrypoint.sh"]