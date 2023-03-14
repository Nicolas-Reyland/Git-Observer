# Server Connections Alert COG
from __future__ import annotations
import discord
from discord.ext import commands, tasks
import os, json, time
import traceback
import yaml
import os

from .webhook_formatter import format_push_hook

GIT_HOOK_DUMPS_DIR = "/git-hooks"
CHANNEL_ID = int(os.environ.get("DISCORD_CHANNEL_ID"))

COG_ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
config_path = "/config.yml"
with open(config_path) as config:
    CONFIG = yaml.load(config, Loader=yaml.FullLoader)


class GithubBaseWebhooks(commands.Cog, name="Github Wehbooks"):
    def __init__(self, bot):
        global CONFIG

        self.bot = bot
        time.sleep(3)
        self.git_hook_notifier_task.start()
        print(f"Using config {CONFIG}")

    @commands.command(description="Check who is connected to the server")
    async def ctx_info(self, ctx):
        await ctx.send(f"Ctx dict: {ctx.__dict__}")

    @commands.command()
    async def _send_msg(self, ctx):
        channel = self.bot.get_channel(CHANNEL_ID)
        await channel.send(ctx.message.content.removeprefix("$_send_msg "))

    @commands.command()
    async def test(self, ctx):
        cid = ctx.message.channel.id
        c = self.bot.get_channel(cid)
        if c is None:
            await ctx.send(ctx.message.channel.__dict__)
            return
        await ctx.send(f"good: {cid}")

    @tasks.loop(seconds=15)
    async def git_hook_notifier_task(self):
        if not os.listdir(GIT_HOOK_DUMPS_DIR):
            return

        for git_hook_file_path in map(
            lambda f: os.path.join(GIT_HOOK_DUMPS_DIR, f),
            os.listdir(GIT_HOOK_DUMPS_DIR),
        ):
            timestamp = os.path.basename(git_hook_file_path)
            timestamp = timestamp[:-4]
            print(f"UTC: {timestamp}", git_hook_file_path)
            with open(git_hook_file_path, "r") as git_hook_file:
                file_content = git_hook_file.read()
                await self.notify_event(file_content)
            os.remove(git_hook_file_path)

        print("All done")

    async def notify_event(self, json_content):
        json_obj = json.loads(json_content)
        if "head_commit" not in json_obj.keys():
            print("Not a push hook")
            return
        try:
            messages, channel_id = format_push_hook(json_obj, CONFIG)
        except Exception as e:
            error_msg = traceback.format_exc()
            messages = (f"Error in parsing github hook json data :\n```{error_msg}```",)
            channel_id = CONFIG["default"]["channel-id"]

        channel = self.bot.get_channel(channel_id)
        if channel is None:
            print("Waiting for cache ...")
            return
        print(f"Writing to channel {channel_id}")

        for msg_string in messages:
            try:
                await channel.send(msg_string)
            except:
                error_msg = traceback.format_exc().replace("```", "\`\`\`")
                if len(error_msg) > 1800:
                    error_msg = "\n...\n" + error_msg[-1800:]
                msg = f"Error in sending message on discord :\n```{error_msg}```"
                await channel.send(msg)


def setup(bot):
    bot.add_cog(GithubBaseWebhooks(bot))
