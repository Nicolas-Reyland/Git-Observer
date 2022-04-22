#!/bin/sh
set -e
chown -R app:app /app /git-hooks
if [ -d "/short-urls" ]; then
    chown -R app:app /short-urls || true
fi
source /run/secrets/discord-bot-env
source /py/bin/activate
su app -c "DISCORD_BOT_TOKEN=\"$DISCORD_BOT_TOKEN\" DISCORD_CHANNEL_ID=\"$DISCORD_CHANNEL_ID\"  python3 /app/bot.py"
