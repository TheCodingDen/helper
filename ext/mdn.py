import discord
import discord.ext.commands as cmd
import requests
import json
import re

from helper.common import *


url_tt = str.maketrans({
    ')': '\\)'
})

mark_re = re.compile(r'</?mark>')


class MDNCog:
    def __init__(self, bot):
        self.bot = bot

    @cmd.command(name='mdn', usage='mdn <search terms>', description='Search the Mozilla Developer Network')
    async def cmd_mdn(self, ctx, *search_terms: str):
        response = requests.get('https://developer.mozilla.org/en-US/search.json', params={'q': ' '.join(search_terms)})
        result = json.loads(response.text, object_hook=Obj)

        embed = discord.Embed(
            colour=getattr(ctx.me, 'color', 0),
            description='\n'.join(
                f'**[{doc.title}]({doc.url.translate(url_tt)})**\n{mark_re.sub("*", doc.excerpt)}\n'
                for doc in result.documents[:3]
            )
        )

        embed.set_author(
            name="Mozilla Developer Network [Full results]",
            url=f'https://developer.mozilla.org/en-US/search?q={"+".join(search_terms)}',
            icon_url="https://developer.mozilla.org/static/img/opengraph-logo.72382e605ce3.png"
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(MDNCog(bot))
