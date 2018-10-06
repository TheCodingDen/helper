import discord
import discord.ext.commands as cmd

from helper.common import *


def cmd_str(c):
    return f'**{c.usage or c.name}**\n{c.description or "No description"}\n'


def cmd_str_debug(c):
    return f'**{c.usage or c.name}** [{", ".join(check.__qualname__.split(".", maxsplit=1)[0] for check in c.checks)}]\n{c.description or "No description"}\n'


class HelpCog:
    def __init__(self, bot):
        self.bot = bot


    @cmd.command(name='hello', hidden=True, usage='hello', description='???')
    async def cmd_hello(self, ctx):
        await ctx.send('Hewwo!')


    @cmd.command(name='help', usage='help', description='Show this message')
    async def cmd_help(self, ctx):
        commands = [c for c in ctx.bot.commands if not c.hidden]
        commands.sort(key=lambda c: c.name)
        commands.sort(key=lambda c: c.name != 'help')

        embed = discord.Embed(colour=getattr(ctx.me, 'color', 0), description='\n'.join(cmd_str(c) for c in commands))
        embed.set_author(name="Helper", url="https://hmry.io", icon_url=ctx.me.avatar_url)

        await ctx.send(embed=embed)


    @cmd.command(name='_help', hidden=True, usage='_help', description='Show debug information about all commands')
    @is_superuser()
    async def cmd__help(self, ctx):
        commands = [c for c in ctx.bot.commands]
        commands.sort(key=lambda c: c.name)
        commands.sort(key=lambda c: c.name != 'help')

        embed = discord.Embed(colour=getattr(ctx.me, 'color', 0), description='\n'.join(cmd_str_debug(c) for c in commands))
        embed.set_author(name="Helper", url="https://hmry.io", icon_url=ctx.me.avatar_url)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(HelpCog(bot))
