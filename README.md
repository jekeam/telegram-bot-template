# telegram-bot-template
Raises from a ready-made telegram bot template based on the library of the [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) with built-in useful functions and a cool architecture.

A simple template for an answer-question bot. Able to forward messages from user to admins and vice versa. Save users and messages to the database.

# Install
Use [Python 3](https://www.python.org/downloads/release/python-3113/)

Copy
- `git clone https://github.com/jekeam/telegram-bot-api-template.git`
- `mv telegram-bot-api-template.git your_name_project`

Create **venv**

- `python3 -m venv venv`

- ` venv/bin/python -m pip install --upgrade pip`

- `venv/bin/python -m pip install -r requirements.txt`

Create DB
- `venv/bin/python create_db.p`

Run background bot (autostartup after restart server)
- Edit and optional - rename file **bot.service**
- `sudo cp bot.service /etc/systemd/system/`
- `sudo systemctl daemon-reload`
- `sudo systemctl enable bot`
- `sudo systemctl start bot`
