FROM ruby:3.2-rc-alpine

WORKDIR /app

COPY ./Gemfile \
     ./Gemfile.lock \
     /app/

RUN apk add --no-cache build-base && \
    bundle update --bundler && \
    bundle install

COPY ./sinatra-entrypoint.sh \
     ./update-gh-ip-list \
     /

COPY ./server.rb \
     ./config.ru \
     /app/

RUN adduser --disabled-password --no-create-home app && \
    chmod +x /sinatra-entrypoint.sh

CMD [ "/sinatra-entrypoint.sh" ]

