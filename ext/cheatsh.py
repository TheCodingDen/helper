import discord.ext.commands as cmd
import requests
import re
from urllib.parse import quote_plus


escape_tt = str.maketrans({
    '`': '\\`'
})

ansi_re = re.compile(r'\x1b\[.*?m')


class CheatShCog:
    def __init__(self, bot):
        self.bot = bot

    def result_fmt(self, url, language, body_text):
        body_space = min(1992 - len(language) - len(url), self.bot.conf.cheatsh_max_len)

        if len(body_text) > body_space:
            return f'```{language}\n{body_text[:body_space - 20]}\n[...]```\nFull results: {url}'
        
        return f'```{language}\n{body_text}```\n{url}'

    @cmd.command(name='csh', usage='csh <language> <search terms>', description='Search cheat.sh')
    async def cmd_csh(self, ctx, language: str, *search_terms: str):
        url = f'https://cheat.sh/{quote_plus(language)}/{quote_plus(" ".join(search_terms))}'
        response = requests.get(url)
        result = ansi_re.sub('', response.text).translate(escape_tt)

        await ctx.send(self.result_fmt(url, language, result))


def setup(bot):
    bot.add_cog(CheatShCog(bot))
