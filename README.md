# 🚀 SmartTgDocs

**SmartTgDocs** is your ultimate Telegram Bot API companion! 📚
Search methods, types, and properties instantly within Telegram using inline queries. Stay secure with built-in bot token protection 🔒 and enjoy a lightning-fast, interactive experience ⚡️.

---

## ✨ Features

* **🔍 Inline Search** — Query Telegram Bot API methods/types with `@BotUsername {query}`.
* **🗂️ Category Filtering** — Filter by `botapi`, `payments`, `passport`, `miniapp` with `!category`.
* **🌟 Wildcard Search** — `*` for multiple characters, `_` for single characters.
* **🔗 Deep-Link Formatting** — Use `.f` to auto-link API symbols.
* **🛡️ Bot Token Protection** — Detects & deletes valid bot tokens to prevent leaks.
* **🖱️ Interactive Interface** — Inline buttons for examples, categories, and navigation.
* **⚡ Lightweight & Fast** — Built with `telethon` & `BeautifulSoup` for efficient scraping.

---

## 📋 Prerequisites

* **Python 3.8+** 🐍
* **Telegram Account** 📱
* **Clone Repo** 🌐: `git clone https://github.com/abirxdhack/SmartTgDocs.git`
* **Text Editor** ✍️ (VSCode recommended)

---

## 🛠️ Setup Guide

### 1️⃣ Clone the Repo

```bash
git clone https://github.com/abirxdhack/SmartTgDocs.git
cd SmartTgDocs
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

Includes: `telethon`, `requests`, `beautifulsoup4`

### 3️⃣ Get Telegram API Credentials

* **Create a Bot** 🤖: Talk to [@BotFather](https://t.me/BotFather), send `/newbot`, copy the token.
* **API ID & Hash** 🆔: Go to [my.telegram.org](https://my.telegram.org), create an app to get `API_ID` & `API_HASH`.

### 4️⃣ Configure the Bot

Edit `config.py`:

```python
API_ID = your_api_id
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"
```

### 5️⃣ Run the Bot

```bash
python bot.py
```

✅ On startup:

```
Bot started: @YourBotUsername
Loaded X documentation entries
Bot is running...
```

---

## 📖 Usage

### Commands

* **/start, /help, /cmds** — Welcome message + navigation buttons
* **Inline Query** 🔍 — `@YourBotUsername {query}`

  * `@YourBotUsername Message` → `Message` type info
  * `@YourBotUsername !payments` → Filter by `payments`
  * `@YourBotUsername send*` → Wildcard search

### Special Features

* **Deep-Link Formatting** 🔗:

```
@YourBotUsername .f $deleteMessages 
```

Auto-links to the `deleteMessages` method.

* **Wildcard Search** ✨: `*` = multiple chars, `_` = single char

* **Token Deletion** 🛡️: Automatically deletes valid bot tokens

### Navigation Buttons

* **⚡ Examples** — Quick queries & syntax
* **🔥 Categories** — Browse docs categories
* **🔍 Search** — Switch to inline query mode
* **🏠 Back/Home** — Navigate menus

---

## 📂 Project Structure

```
SmartTgDocs/
├── bot.py          # Main bot script
├── config.py       # API credentials
├── requirements.txt # Dependencies
└── README.md       # This file
```

---

## 🤝 Contributing

1. Fork 🍴
2. Branch: `git checkout -b feature-branch` 🌿
3. Commit: `git commit -m "Add feature"` 💾
4. Push: `git push origin feature-branch` 🚀
5. Open PR 📬

Follow the existing style and keep code clean.

---

## 📢 Updates & Support

* **Updates Channel**: [t.me/TheSmartDev](https://t.me/TheSmartDev)
* **Developer**: [@ISmartCoder](https://t.me/abirxdhackz)
* **GitHub**: [github.com/abirxdhack](https://github.com/abirxdhack)
* **Report Issues**: [GitHub Issues](https://github.com/abirxdhack/SmartTgDocs/issues)

---

## 🙌 Acknowledgments

* Built by [@ISmartCoder](https://t.me/abirxdhackz) 💻
* Powered by [Telegram Bot API](https://core.telegram.org/bots/api) 🌐

---


