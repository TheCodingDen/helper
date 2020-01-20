import re
from urllib.parse import quote_plus

import aiohttp

from ...common import *
from ... import module as mod



escape_tt = str.maketrans({
    '`': '\\`'
})

ansi_re = re.compile(r'\x1b\[.*?m')


class CheatShModule(mod.Module):
    def on_load(self):
        self.conf.setdefault('max_length', 1000)
        self.conf.sync()

        self.session = None
    
    def on_unload(self):
        if self.session:
            self.log.info('Closing session...')
            mod.loop.create_task(self.session.close())

    def result_fmt(self, url, language, body_text):
        body_space = min(1992 - len(language) - len(url), self.conf['max_length'])

        if len(body_text) > body_space:
            return f'```{language}\n{body_text[:body_space - 20]}\n[...]```\nFull results: {url}'
        
        return f'```{language}\n{body_text}```\n{url}'

    @mod.command(name='csh', usage='csh <language> <search terms>', description='Search cheat.sh')
    async def cmd_csh(self, ctx, language: str, *search_terms: str):
        url = f'https://cheat.sh/{quote_plus(language)}/{quote_plus(" ".join(search_terms))}'

        if not self.session:
            self.session = aiohttp.ClientSession()
            self.log.info('Session opened')

        async with self.session.get(
            url,
            headers={'User-Agent': 'curl/7.68.0'},
            timeout=aiohttp.ClientTimeout(total=10)
        ) as response:
            result = ansi_re.sub('', await response.text()).translate(escape_tt)

        await ctx.send(self.result_fmt(url, language, result))
