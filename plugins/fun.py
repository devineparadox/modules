import aiohttp
import random

from pyjokes import get_joke
from pyrogram import Client, filters
from Devine import app 


async def make_request(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            data = await response.json()
            return data["question"]


@app.on_message(filters.command("truth"))
async def truth(client, message):
    truth_question = await make_request("https://api.truthordarebot.xyz/v1/truth")
    await message.reply_text(truth_question)


@app.on_message(filters.command("dare"))
async def dare(client, message):
    dare_question = await make_request("https://api.truthordarebot.xyz/v1/dare")
    await message.reply_text(dare_question)


@app.on_message(filters.command("joke"))
async def joke(client, message):
    await message.reply_text(get_joke())


