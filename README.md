# Git-Observer
Discord bot for notifying on github events

## Installation

You will need the following before setting this project up:
 - **docker** to be installed
 - **docker compose** to be installed (v2 is better)
 - a completely setup dicord bot (no code needed, but on the discord developer page) [tutorial](https://discordpy.readthedocs.io/en/stable/discord.html)
 - the discord bot authentification token (keep this secret) [documentation](https://discord.com/developers/docs/topics/oauth2#bots)
 - the default channel id of the discord channel you want to write messages to (maybe keep this secret ?) [tutorial](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)
 - a github webhook secret (keep this secret) [tutorial](https://docs.github.com/en/developers/webhooks-and-events/webhooks/creating-webhooks)

First, clone and cd into the project folder.
```
git clone https://github.com/Nicolas-Reyland/git-observer
cd git-observer
```

Now is the time to enter the secrets. Please run this :
```
./setup-secrets.sh
```

Once the script has been executed, deploy the project with docker compose (see next step if this fails because of the remote registry not being unavailable) :
```
docker compose up -d
```
💡 You may want to remove the `/var/www/url-short/s:/short-urls` bind-mount. 💡

⚠️ ONLY IF the previous step (docker compose) raised some error because you could not pull the image from the remote registry, do this step ⚠️
```
docker build --file discord-bot/Dockerfile --tag=public.whale.iluvatar.xyz:5050/discord-bot:latest discord-bot/
docker build --file ghwh-listener/Dockerfile --tag=public.whale.iluvatar.xyz:5050/ghwh-listener:latest ghwh-listener/
```

Finally, you have to accept the incoming github webhooks. You are free to do this however you want, but here's an example of how to forward requests to the docker container using `nginx`:

Add an upstream that looks like this :
```
upstream github-webhook-upstream {
  server unix:///tmp/ghwh-listener-container/sockets/ghwh-listener-nw.sock;
}
```

Inside your `server` block, add a location (adapt location to your liking) :
```
location /github-webhooks {
  proxy_pass http://github-webhook-upstream;
}
```

Then, test your new config (`nginx -t`) and reload the nginx service.


## Configuration
To add github projects to the observer, you should write the `discord-bot/config.yml` file (there is an example file).
It should look like this:
```yml
project1:
  name: "UserName/project1"
  channel-id: 1234567890
project2:
  name: "UserName2/projetc2"
  channel-id: 10987654321
default:
  name: "default"
  channel-id: 127001
```

You should be all set up !!
