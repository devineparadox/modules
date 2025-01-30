import requests
from pyrogram import Client, filters

@Client.on_message(filters.command("ud"))
async def ud(client, message):
    try:
        text = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await message.reply_text("ɪɴᴘᴜᴛ sᴇᴀʀᴄʜ ᴋᴇʏᴡᴏʀᴅs ғᴏʀ ᴜᴅ!")

    url = f"https://api.urbandictionary.com/v0/define?term={text}"
    response = requests.get(url)
    results = response.json()

    if results.get("list"):
        definition = results["list"][0].get("definition", "")
        example = results["list"][0].get("example", "")
        definition = definition.replace("[", "").replace("]", "")
        example = example.replace("[", "").replace("]", "")

        reply_txt = f'**ᴡᴏʀᴅ:** {text}\n\n**ᴅᴇғɪɴɪᴛɪᴏɴ:**\n{definition}\n\n**ᴇɢ:**\n{example}'
    else:
        reply_txt = f'**ᴡᴏʀᴅ:** {text}\n\nɴᴏᴛʜɪɴɢ ғᴏᴜɴᴅ'

    await message.reply_text(reply_txt)
