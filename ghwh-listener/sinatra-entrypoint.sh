#!/bin/sh
set -e
source /run/secrets/ghwh-listener-env
chown -R app:app /app /git-hooks /sockets
cd /app
su app -c "GITHUB_WH_SECRET=ZzUlEPCXzLaVrv0P8p6SZMEWynN59mmI7NOkqGJw3rPfMs994nMSoOmMOsvZnyRhaJj0oUQFa6BpQAo1O RACK_ENV=production bundle exec rackup -s puma -E production -o /sockets/ghwh-listener-nw.sock config.ru"
