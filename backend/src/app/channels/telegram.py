# src/app/channels/telegram.py
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, MessageHandler, filters

from src.app.channels.base import Channel
from src.app.core.types import Channels


class Telegram(Channel):
    channel = Channels.Telegram

    def __init__(self, flow_name):
        super().__init__(flow_name)
        self.app = Application.builder().token(os.environ["TELEGRAM_BOT_TOKEN"]).build()
        self.app.add_handler(CommandHandler("start", self.on_event))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.on_event))
        self.app.add_handler(CallbackQueryHandler(self.on_event))
        print("--BUILD SUCCESSFUL--")

    async def render(self, target, out):
        markup = None
        if out.buttons:
            markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton(b.label, callback_data=str(i))] for i, b in enumerate(out.buttons, 1)]
            )
        await target.send_message(out.text or "...", reply_markup=markup)

    async def on_event(self, update, _):
        user, chat = update.effective_user, update.effective_chat

        if update.callback_query:
            await update.callback_query.answer()
            await update.callback_query.edit_message_reply_markup(None)
            raw = update.callback_query.data
        else:
            raw = update.message.text

        await self.process(
            user_id=str(user.id),
            name=user.full_name,
            raw=raw,
            target=chat,
            restart=raw.startswith("/start"),
        )

    def run(self):
        self.app.run_polling()
