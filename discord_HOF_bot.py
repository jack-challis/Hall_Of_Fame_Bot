#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 19:02:03 2024

@author: jackchallis
"""
import discord
from discord.ext import commands
import nest_asyncio
import heapq

TOKEN = "[DISCORD BOT TOKEN HERE]"
DISCORD_GALLERY_CHANNELS = ["DISCORD CHANNEL ID HERE"]

nest_asyncio.apply()
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

top_count = 1  # Default number of top messages to retrieve

async def get_top_messages(ctx, gallery_channels, target_emote):
    top_messages = list()
    tiebreak_counter = 0
    message_counter = 0
    await ctx.send(f"Launching top {top_count} {target_emote} search.")

    for gallery_id in gallery_channels:
        gallery = ctx.guild.get_channel(int(gallery_id))
        if gallery:
            await gallery.send(f"Parsing messages.")

            async for message in gallery.history(limit=None):
                message_counter += 1
                if message_counter % 1000 == 0:
                    await ctx.send(f"Parsed {message_counter} channel posts")

                emote_reactions = [reaction for reaction in message.reactions if str(reaction.emoji) == target_emote]
                reaction_count = sum(emote.count for emote in emote_reactions)

                if len(top_messages) == top_count and reaction_count < top_messages[0][0]:
                    continue

                heapq.heappush(top_messages, (reaction_count, tiebreak_counter, message))
                if len(top_messages) > top_count:
                    heapq.heappop(top_messages)
                tiebreak_counter += 1

    result_message = f"\nTop {top_count} {target_emote} moments:\n"
    for count, _, message in sorted(top_messages, reverse=True):
        formatted_date = message.created_at.strftime("%d/%m/%Y %H:%M")
        
        if message.content:
            content_info = f"\n{message.content}"
        
        if message.attachments:            
            for attachment in message.attachments:
                if attachment.content_type.startswith('image/'):
                    content_info += f"\n{attachment.url} "
                elif attachment.content_type.startswith('video/') and attachment.url.lower().endswith(('gif', 'gifv')):
                    content_info += f"\n{attachment.url} "
                    
        if message.embeds:
            for embed in message.embeds:
                if embed.type == 'image' and embed.url.lower().endswith(('gif', 'gifv')):
                    content_info += f"\n{embed.url} "
                else:
                    content_info += f"\n{embed.url} "

        result_message += f"\n{target_emote} count : {count}\nDate: {formatted_date} \nSender: {message.author.name}, \n{content_info}\n"
    
    await ctx.send(result_message)

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')

@bot.command()
async def top(ctx, target_emote: str):  # Updated command to accept count parameter
    await get_top_messages(ctx, DISCORD_GALLERY_CHANNELS, target_emote)

bot.run(TOKEN)
