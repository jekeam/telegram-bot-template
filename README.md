# telegram-bot-template
A ready-made telegram bot template based on the [PTB](https://github.com/python-telegram-bot/python-telegram-bot) library with built-in useful features and architecture.

* A simple bot template for answering questions. 
* Ability to forward messages from user to admin and vice versa. 
* Save users and messages to a database.

# Install
Use [Python 3](https://www.python.org/downloads/release/python-3113/)

Copy
- `git clone https://github.com/jekeam/telegram-bot-api-template.git`
- `mv telegram-bot-api-template.git your_name_project`

Create **venv**

- `python3 -m venv venv`

- `venv/bin/python -m pip install --upgrade pip`

- `venv/bin/python -m pip install -r requirements.txt`

Create DB
- `venv/bin/python create_db.py`

Run background bot (autostartup after restart server)
- Edit and optional - rename file **bot.service**
- `sudo cp bot.service /etc/systemd/system/`
- `sudo systemctl daemon-reload`
- `sudo systemctl enable bot`
- `sudo systemctl start bot`
