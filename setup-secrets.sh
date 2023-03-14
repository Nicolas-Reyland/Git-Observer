#!/bin/sh
# reading the information
echo "[Discord Secrets]"
echo -n "Enter your discord bot token : "
read discord_bot_token
echo -n "Enter the default discord channel id : "
read discord_channel_id
echo "[Github Secret]"
echo -n "Enter the github webhook secret : "
read github_wh_secret
# writing to the .env files
printf "#!/bin/sh\nexport DISCORD_BOT_TOKEN=\"$discord_bot_token\"\nexport DISCORD_CHANNEL_ID=\"$discord_channel_id\"\n" > discord-bot/.env
printf "#!/bin/sh\nexport GITHUB_WB_SECRET=\"$github_wh_secret\"\n" > ghwh-listener/.env

