#Copyright @ISmartCoder
#Updates Channel https://t.me/TheSmartDev  
import asyncio
import requests
import re
from bs4 import BeautifulSoup
from telethon import TelegramClient, events, Button
import concurrent.futures
from typing import List, Dict
from config import API_ID, API_HASH, BOT_TOKEN 

DOCS_URL = "https://core.telegram.org/bots/api"
COMMAND_PREFIX = [",", ".", "/", "!", "#"]

BOT_USERNAME = None
DOCS_CACHE = []

def fetch_docs():
    try:
        r = requests.get(DOCS_URL)
        soup = BeautifulSoup(r.text, "html.parser")
        docs = []
        for section in soup.select("h4"):
            title = section.get_text(strip=True)
            anchor = section.find("a", href=True)
            if not anchor:
                continue
            link = DOCS_URL + anchor["href"]
            description_parts = []
            sibling = section.find_next_sibling()
            while sibling and sibling.name != "h4":
                if sibling.name != "table":
                    text = sibling.get_text(" ", strip=True)
                    if text:
                        description_parts.append(text)
                sibling = sibling.find_next_sibling()

            category = "botapi"
            title_lower = title.lower()
            if "payment" in title_lower or "invoice" in title_lower:
                category = "payments"
            elif "passport" in title_lower:
                category = "passport"
            elif "webapp" in title_lower or "miniapp" in title_lower:
                category = "miniapp"

            docs.append({
                "title": title,
                "url": link,
                "description": " ".join(description_parts).strip()[:500],
                "category": category
            })
        print("Loaded " + str(len(docs)) + " documentation entries")
        return docs
    except Exception as e:
        print("Error fetching docs: " + str(e))
        return []

def get_start_message():
    return ("**Hi there! 👋**\n"
            "I'm your inline assistant for the Telegram Bot API.\n\n"
            "Type `@" + BOT_USERNAME + " {query}` anywhere to search methods or types.\n\n"
            "**Bonus:**\n"
            "I also delete valid bot tokens from chat messages.\n\n"
            "**BotAPI:** ` v9.2`")

def get_start_keyboard():
    return [
        [Button.inline("⚡️ Examples", b"examples"), Button.inline("🔥 Categories", b"categories")],
        [Button.switch_inline("🔍 Search", same_peer=True)]
    ]

def get_examples_page1():
    return ("**Examples:**\n"
            "**•** `@" + BOT_USERNAME + " ` - List all methods & types.\n"
            "**•** `@" + BOT_USERNAME + " Message ` - Info about \"Message\".\n"
            "**•** `@" + BOT_USERNAME + " WebApp` - \"WebApp\"'s properties.\n"
            "**•** `@" + BOT_USERNAME + " !xyz` - Filter by category.\n"
            "**Special:**\n"
            "**• `!`** - Filter results by [category.](https://t.me/" + BOT_USERNAME + "?start=categories)\n"
            "**• `.`** - View or search properties or parameters.\n"
            "**• `*`** - Matches zero or more characters.\n"
            "**• `_`** - Matches exactly one character.\n"
            "    \nAll results link to the official [Bot API Docs.](https://core.telegram.org/bots/api)")

def get_examples_page2():
    return ("**Examples:**\n"
            "Prefix your text with \"`.f`\" to automatically deep-link API symbols.\n"
            "**INPUT:**\n"
            "`@" + BOT_USERNAME + " .f To delete messages in bulk, use $deleteMessages where message_ids is a list of each $Message's $Message.message_id.`\n"
            "**OUTPUT:**\n"
            "To delete messages in bulk, use [deleteMessages](https://t.me/" + BOT_USERNAME + "?start=randomCuteCar) where message_ids is a list of each [Message](https://t.me/" + BOT_USERNAME + "?start=randomCuteCar)'s [message_id](https://t.me/" + BOT_USERNAME + "?start=randomCuteCar).\n"
            "**Special:**\n"
            "**• `$`** - Mark API Symbol to format.\n"
            "**• `.`** - Mention property or paramter of API symbol.\n"
            "**• `$$`** - Don't replace `Abc.xyz` with `xyz` while formatting.\n"
            "    \nAll results link to the official [Bot API Docs](https://core.telegram.org/bots/api).")

def get_categories_message():
    return ("**Available Categories:**\n"
            "**• `botapi`** - General methods & types.\n"
            "**• `payments`** - Payments & invoices.\n"
            "**• `passport`** - Telegram Passport.\n"
            "**• `miniapp`** - Mini apps methods & types.")

def wildcard_match(pattern, text):
    try:
        pattern = pattern.replace('*', '.*').replace('_', '.')
        return re.match(pattern, text, re.IGNORECASE) is not None
    except:
        return False

def format_deep_link_text(text):
    def replace_symbol(match):
        symbol = match.group(1)
        if not symbol.startswith('$'):
            return "[" + symbol + "](https://t.me/" + BOT_USERNAME + "?start=randomCuteCar)"
        return match.group(0)

    return re.sub(r'\$(\w+(?:\.\w+)*)', replace_symbol, text)

def is_valid_bot_token(text):
    token_pattern = r'\b\d{8,10}:[A-Za-z0-9_-]{35}\b'
    return re.search(token_pattern, text) is not None

def extract_command(text):
    if not text:
        return None, None

    for prefix in COMMAND_PREFIX:
        if text.startswith(prefix):
            parts = text[1:].split(None, 1)
            if parts:
                return parts[0].lower(), parts[1] if len(parts) > 1 else ""
    return None, None

async def send_start_message(client, chat_id, edit_msg=None):
    message = get_start_message()
    keyboard = get_start_keyboard()

    if edit_msg:
        await edit_msg.edit(message, buttons=keyboard, parse_mode='md', link_preview=False)
    else:
        await client.send_message(chat_id, message, buttons=keyboard, parse_mode='md', link_preview=False)

async def delete_token_message(client, message):
    try:
        await asyncio.sleep(0.1)
        await message.delete()
        print("Deleted message with bot token from " + str(message.chat_id))
    except Exception as e:
        print("Failed to delete token message: " + str(e))

async def main():
    global BOT_USERNAME, DOCS_CACHE

    client = TelegramClient('bot', API_ID, API_HASH)

    try:
        await client.start(bot_token=BOT_TOKEN)

        me = await client.get_me()
        BOT_USERNAME = me.username
        print("Bot started: @" + BOT_USERNAME)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            loop = asyncio.get_event_loop()
            DOCS_CACHE = await loop.run_in_executor(executor, fetch_docs)

        @client.on(events.NewMessage)
        async def message_handler(event):
            if not event.message.text:
                return

            text = event.message.text.strip()

            if is_valid_bot_token(text):
                asyncio.create_task(delete_token_message(client, event.message))
                return

            command, args = extract_command(text)

            if command in ['start', 'help', 'cmds']:
                await send_start_message(client, event.chat_id)

        @client.on(events.CallbackQuery(data=b'examples'))
        async def examples_handler(event):
            keyboard = [
                [Button.inline("Back", b"start"), Button.inline("Next", b"examples_page2")]
            ]
            await event.edit(get_examples_page1(), buttons=keyboard, parse_mode='md', link_preview=False)

        @client.on(events.CallbackQuery(data=b'examples_page2'))
        async def examples_page2_handler(event):
            keyboard = [
                [Button.inline("Back", b"examples"), Button.inline("Home", b"start")]
            ]
            await event.edit(get_examples_page2(), buttons=keyboard, parse_mode='md', link_preview=False)

        @client.on(events.CallbackQuery(data=b'categories'))
        async def categories_handler(event):
            keyboard = [
                [Button.inline("Back", b"start")]
            ]
            await event.edit(get_categories_message(), buttons=keyboard, parse_mode='md')

        @client.on(events.CallbackQuery(data=b'start'))
        async def start_callback_handler(event):
            await event.edit(get_start_message(), buttons=get_start_keyboard(), parse_mode='md', link_preview=False)

        @client.on(events.InlineQuery)
        async def inline_handler(event):
            query = event.text.strip()
            builder = event.builder
            results = []

            if not query:
                results.append(builder.article(
                    title="@" + BOT_USERNAME,
                    description="Type method name to search...",
                    text="Start typing to search Bot API methods!"
                ))
            elif query.startswith('.f '):
                formatted_text = format_deep_link_text(query[3:])
                results.append(builder.article(
                    title="Formatted Text",
                    description="Deep-linked API symbols",
                    text=formatted_text
                ))
            elif query.startswith('!'):
                category = query[1:].lower()
                filtered = [d for d in DOCS_CACHE if d["category"] == category]
                for doc in filtered[:20]:
                    results.append(builder.article(
                        title=doc["title"],
                        description="[" + doc['category'] + "] " + doc['description'][:150],
                        text="**" + doc['title'] + "**\n\n" + doc['description'] + "\n\n[Reference](" + doc['url'] + ")",
                        buttons=[Button.url("Reference", doc["url"])]
                    ))
            elif '*' in query or '_' in query:
                filtered = [d for d in DOCS_CACHE if wildcard_match(query, d["title"])]
                for doc in filtered[:20]:
                    results.append(builder.article(
                        title=doc["title"],
                        description=doc["description"][:200],
                        text="**" + doc['title'] + "**\n\n" + doc['description'] + "\n\n[Reference](" + doc['url'] + ")",
                        buttons=[Button.url("Reference", doc["url"])]
                    ))
            else:
                filtered = [d for d in DOCS_CACHE if query.lower() in d["title"].lower()]
                for doc in filtered[:20]:
                    results.append(builder.article(
                        title=doc["title"],
                        description=doc["description"][:200],
                        text="**" + doc['title'] + "**\n\n" + doc['description'] + "\n\n[Reference](" + doc['url'] + ")",
                        buttons=[Button.url("Reference", doc["url"])]
                    ))

            if not results or len(results) == 0:
                results.append(builder.article(
                    title="No results found",
                    description="Try different keywords",
                    text="No results found for your query."
                ))

            await event.answer(results, cache_time=60)

        print("Bot is running...")
        await client.run_until_disconnected()

    except Exception as e:
        print("Error starting bot: " + str(e))

if __name__ == "__main__":
    asyncio.run(main())