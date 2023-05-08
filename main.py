import traceback

from telegram import ForceReply, Update
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, TypeHandler

import config
from db import func as db_func
from log import app_log
import tg.utils as tg_utils


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user

    db_func.set_user(
        user_id=user.id,
        first=user.first_name,
        last=user.last_name,
        username=user.username,
        url=user.link,
        lang_code=user.language_code,
    )

    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def set_last_touch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    action_data = None
    if update.message:
        action_data = update.message.text
    elif update.callback_query:
        action_data = update.callback_query.data

    user_id = tg_utils.get_user_id(update)
    if user_id:
        if action_data:
            try:
                await context.bot.send_chat_action(chat_id=user_id, action=ChatAction.TYPING)
            except Exception as e:
                app_log.error(f"{e}, {traceback.format_exc()}")

            db_func.set_last_touch(user_id)

            if action_data:
                action_data = str(action_data)

            db_func.set_user_action(user_id=user_id, message=action_data[:4000])
    else:
        tg_utils.remove_jobs(name=str(user_id), context=context)
        return


@tg_utils.only_admin_async
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(config.API_KEY).build()

    application.add_handler(TypeHandler(Update, callback=set_last_touch), group=1)
    application.add_error_handler(tg_utils.error_handler)

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
