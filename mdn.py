import discord
import discord.ext.commands as cmd
import json
import re

import aiohttp

from ...common import *
from ... import module as mod


url_tt = str.maketrans({
    ')': '\\)'
})

mark_re = re.compile(r'</?mark>')


class MDNModule(mod.Module):
    def on_load(self):
        self.session = None
    
    def on_unload(self):
        if self.session:
            self.log.info('Closing session...')
            mod.loop.create_task(self.session.close())

    @cmd.command(name='mdn', usage='mdn <search terms>', description='Search the Mozilla Developer Network')
    async def cmd_mdn(self, ctx, *search_terms: str):
        if not self.session:
            self.session = aiohttp.ClientSession()
            self.log.info('Session opened')

        # TODO: Deal with timeouts ~hmry (2020-01-20, 01:25)
        async with self.session.get(
            'https://developer.mozilla.org/api/v1/search/en-US',
            params={'q': ' '.join(search_terms)},
            timeout=aiohttp.ClientTimeout(total=10)
        ) as response:
            result = json.loads(await response.text(), object_hook=Obj)


        embed = discord.Embed(
            colour=getattr(ctx.me, 'color', 0),
            description='\n'.join(
                f'**[{doc.title}]({f"https://developer.mozilla.org/{doc.locale}/docs/{doc.slug}".translate(url_tt)})**\n{mark_re.sub("*", doc.excerpt)}\n'
                for doc in result.documents[:3]
            )
        )

        embed.set_author(
            name="Mozilla Developer Network [Full results]",
            url=f'https://developer.mozilla.org/en-US/search?q={"+".join(search_terms)}',
            icon_url="https://developer.mozilla.org/static/img/opengraph-logo.72382e605ce3.png"
        )

        await ctx.send(embed=embed)
