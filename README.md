# Git-Observer
Discord bot for notifying on github events

## Installation

You will need the following before installing this project:
 - **docker** to be installed
 - **docker compose** to be installed (v2 is better)
 - a completely setup dicord bot (no code needed, but on the discord developer page) [tutorial](https://discordpy.readthedocs.io/en/stable/discord.html)
 - the discord bot authentification token (keep this secret) [documentation](https://discord.com/developers/docs/topics/oauth2#bots)
 - the channel id of the discord channel you want to write messages to (maybe keep this secret ?) [tutorial](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)
 - a github webhook secret (keep this secret) [tutorial](https://docs.github.com/en/developers/webhooks-and-events/webhooks/creating-webhooks)

First, clone and cd into the project folder.
```
git clone https://github.com/Nicolas-Reyland/git-observer
cd git-observer
```

Then, build the two images needed :
```
docker build --file discord-bot/Dockerfile --tag=discord-bot:latest discord-bot/
docker build --file ghwh-listener/Dockerfile --tag=ghwh-listener:latest ghwh-listener/
```

Now is the time to enter the secrets. Please run this :
```
./setup-secrets.sh
```

Once the script has been executed, deploy the project with docker compose :
```
docker compose up -d
```
⚠️ You may want to remove the '/short-urls' bind-mount. ⚠️

Finally, you have to accept the incoming github webhooks. I am going to show you how to do it with `nginx`, but it's pretty straight-forward: we just need to redirect traffic to a unix socket.
In one of you nginx sites files `sites-available`, add an upstream object like this :
```
upstream github-webhook-upstream {
  server unix:///tmp/ghwh-listener-container/sockets/ghwh-listener-nw.sock;
}
```

And inside your `server` block, add a location (adapt location to your liking) :
```
location /github-webhooks {
  proxy_pass http://github-webhook-upstream;
}
```

The, test your new config (`nginx -t`) and reload the nginx service. You should be all setup !!