"""
Created by Epic at 10/30/20
"""
from custom_types import CogType, ExtendedClient
from cog_manager import CommandContext

from logging import getLogger
from os import environ as env

owner_ids = [int(owner_id) for owner_id in env["OWNER_IDS"].split(" ")]


def owner_check(func):
    async def inner(_, ctx: CommandContext):
        if ctx.message.author["id"] in owner_ids:
            await func(ctx)
        else:
            await ctx.send(f"<@{ctx.message.author['id']}>, you are boring me.")
    return inner


class Admin(CogType):
    def __init__(self, bot: ExtendedClient):
        self.bot = bot
        self.logger = getLogger("commands.about")

        super().__init__(bot)

    @CogType.command("force-workers (\\d+) (\\d+)")
    @owner_check
    async def force_workers(self, ctx: CommandContext):
        guild_id = str(ctx.args[0])
        worker_count = int(ctx.args[1])
        self.bot.workers.worker_counts[guild_id] = worker_count

        await ctx.send("Updated worker count!")


def setup(bot: ExtendedClient):
    Admin(bot)
