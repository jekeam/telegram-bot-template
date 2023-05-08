import html
import json
import traceback

from telegram import Update
from telegram.constants import ParseMode, ChatMemberStatus
from telegram.ext import ContextTypes

from config import ADMINS, DB_USER_STATUS_OFF
import db.func as db_func
from log import app_log


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a tg message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    app_log.error("Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    message = message if len(message) <= 4000 else html.escape(message[len(message) - 3997 : len(message)] + "...")

    # Finally, send the message
    for admin in ADMINS:
        try:
            await context.bot.send_message(chat_id=admin, text=message, parse_mode=ParseMode.HTML)
        except Exception as e:
            app_log.error(f"Error submitting an error: {e}, {traceback.format_exc()}")


def remove_jobs(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        app_log.info(f"Deleting a job by name: {job.name}, data: {job.data}")
        job.schedule_removal()
    return True


def set_user_block(user_id: int, context: ContextTypes.DEFAULT_TYPE = None):
    app_log.info(f"{user_id} - bot was blocked by the user / user is deactivated")

    db_func.set_user_status(user_id, DB_USER_STATUS_OFF)
    db_func.set_user_action(user_id=user_id, message="block")

    if context:
        remove_jobs(name=str(user_id), context=context)


def get_user_id(update: Update) -> int:
    cquery = update.callback_query
    iquery = update.inline_query
    message = update.message
    edited_message = update.edited_message

    user_id = None
    if iquery:
        user_id = iquery.from_user.id
    elif cquery:
        user_id = cquery.message.chat_id
    elif message:
        user_id = message.from_user.id
    elif edited_message:
        user_id = edited_message.from_user.id
    else:
        # set user block
        if hasattr(update, "my_chat_member"):
            if hasattr(update.my_chat_member, "new_chat_member"):
                status = update.my_chat_member.new_chat_member.status
                if status is ChatMemberStatus.BANNED:
                    user_id = update.my_chat_member.from_user.id
                    set_user_block(user_id=user_id)
                # I deliberately turned it off for the time being.
                # it is necessary to refine the logic of starting the user from scratch (when not yet in the database)

                # elif status is ChatMemberStatus.MEMBER:
                #     set_user_unblock(user_id=user_id)
    return user_id


def only_admin_async(func):
    async def wrapper(*args, **kwargs):
        update = args[0]
        user_id = get_user_id(update)
        for row in db_func.get_admins():
            if user_id == row.id:
                return await func(*args, **kwargs)
        app_log.info(f"{user_id} - Access is denied")

    return wrapper
