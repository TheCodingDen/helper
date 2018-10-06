import re
import datetime
import inspect
import logging

import discord.ext.commands as cmd
from discord.ext.commands.view import StringView

from .common import *

log = logging.getLogger('bot')

class Helper(cmd.Bot):
    def __init__(self, conf):
        super().__init__(command_prefix='', description='', pm_help=False, help_attrs={})

        super().remove_command('help')

        self.conf = conf
        self.first_ready = None
        self.last_ready = None
        self.last_resume = None

        self.command_regex = None
        self.command_dms_regex = None

        def clean_code(content):
            content = content.strip()

            if content.startswith('```py'):
                content = content[5:]

            if content.startswith('```'):
                content = content[3:]

            if content.endswith('```'):
                content = content[:-3]

            return content.strip('`').strip()

        def create_env(ctx):
            env = {
                'bot': self,
                'ctx': ctx
            }
            env.update(globals())
            return env

        @self.command(name='eval', hidden=True, usage='eval <code>', description='Evaluate a piece of python code')
        @is_superuser()
        async def cmd_eval(ctx, *, code: str):
            code = clean_code(code)

            result = eval(code, create_env(ctx))
            if inspect.isawaitable(result):
                result = await result

            await ctx.send_paginated(result)

        @cmd_eval.error
        async def err_eval(ctx, error):
            if isinstance(error, cmd.CheckFailure):
                pass
            else:
                await ctx.send_paginated(error)

        @self.command(name='exec', hidden=True, usage='exec <code>', description='Execute a piece of python code')
        @is_superuser()
        async def cmd_exec(ctx, *, code: str):
            code = clean_code(code)

            env = create_env(ctx)
            code = f'import asyncio\nasync def _func():\n{textwrap.indent(code, "    ")}'

            exec(code, env)

            result = await env['_func']()

            if result is not None:
                await ctx.send_paginated(result)

        @cmd_exec.error
        async def err_exec(ctx, error):
            if isinstance(error, cmd.CheckFailure):
                pass
            else:
                await ctx.send(error)

        @self.command(name='times', hidden=True, usage='times', description='Show time stats')
        async def cmd_times(ctx):
            await ctx.send(f'```prolog\nFirst Ready: {self.first_ready}\nLast Ready:  {self.last_ready}\nLast Resume: {self.last_resume}\nUptime:      {datetime.datetime.utcnow() - self.first_ready}```')

        for ext in conf.initial_extensions:
            try:
                self.load_extension(ext)
            except:
                log.exception(f'Failed to load extension {ext!r} on startup')
            else:
                log.info(f'Loaded extension {ext!r} on startup')

    async def on_ready(self):
        log.info(f'Ready with Username {self.user.name!r}, ID {self.user.id!r}')

        now = datetime.datetime.utcnow()
        if self.first_ready is None:
            self.first_ready = now

        self.last_ready = now

        self.command_regex = re.compile(fr'^<@!?{self.user.id}>\s*(.*?)\s*$')
        self.command_dms_regex = re.compile(fr'^(?:<@!?{self.user.id}>)?\s*(.*?)\s*$')

    async def on_resumed(self):
        log.warning(f'Resumed')
        self.last_resume = datetime.datetime.utcnow()

    async def get_context(self, message, *, cls=cmd.Context):
        r"""AAAAAAAHHHHHHHHHHHHHHHH WHY!!!!!!"""

        cmd_regex = self.command_dms_regex if message.guild is None else self.command_regex
        match = cmd_regex.match(message.content)

        if not match:
            return cls(prefix=None, view=None, bot=self, message=message)

        view = StringView(match.group(1))
        ctx = cls(prefix=None, view=view, bot=self, message=message)

        if self._skip_check(message.author.id, self.user.id):
            return ctx

        invoker = view.get_word()
        ctx.invoked_with = invoker
        ctx.command = self.all_commands.get(invoker)
        return ctx
