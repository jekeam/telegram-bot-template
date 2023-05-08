# telegram-bot-template
Raises from a ready-made telegram bot template based on the library of the python-telegram-bot with built-in useful functions and a cool architecture.

A simple template for an answer-question bot. Able to forward messages from user to admins and vice versa. Writes yuezra and messages to the database.


# Requirements
[Python 3](https://www.python.org/downloads/release/python-3113/)

# Install
Copy
- `git clone https://github.com/jekeam/telegram-bot-api-template.git`
- `mv telegram-bot-api-template.git your_name_project`

Create **venv**

- `python3 -m venv venv`

- ` venv/bin/python -m pip install --upgrade pip`

- `venv/bin/python -m pip install -r requirements.txt`

Create DB
- `venv/bin/python create_db.p`

Run backgroud bot (with autostartup before restart server)
- Edit and optional - rename file **bot.service**
- `sudo cp bot.service /etc/systemd/system/`
- `sudo systemctl daemon-reload`
- `sudo systemctl enable bot`
- `sudo systemctl start bot`
