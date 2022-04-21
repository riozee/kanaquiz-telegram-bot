from telegram import Update
from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    Filters,
)
import logging
import yaml
import kana
import random

with open("config.yaml", "r") as file:
    CONFIG = yaml.safe_load(file)

updater = Updater(token=CONFIG["BOT_TOKEN"], use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def generate_kana(chars: int):
    res = {"hiragana": [], "katakana": [], "romaji": []}
    for _ in range(chars):
        r = kana.random_kana()
        res["hiragana"] += r[0]
        res["katakana"] += r[1]
        res["romaji"] += r[2]
    # remove leading small tsu
    if res["hiragana"][0].startswith("っ"):
        res["hiragana"] = res["hiragana"][1:]
        res["katakana"] = res["katakana"][1:]
        res["romaji"] = res["romaji"][1:]
    return res


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.message.chat.id,
        text=(
            "<b>ハロー！こんにちは！</b>\n\n"
            "<i>I'll help you quickly learn to recognize any kana characters, by playing a simple game.</i>\n\n"
            "/play - play the game\n"
            "/quit - cancel the game\n"
            "/gamemode - change game mode"
        ),
        parse_mode="HTML",
    )


dispatcher.add_handler(CommandHandler("start", start))


def gamemode(update: Update, context: CallbackContext):
    if context.user_data.get("answer"):
        quit(update, context)
    if context.user_data.get("gamemode"):
        context.user_data["gamemode"] = None
    context.bot.send_message(
        chat_id=update.message.chat.id,
        text="<b>Select game mode:</b>",
        reply_markup={
            "keyboard": [
                [{"text": "Hiragana => Romaji"}],
                [{"text": "Katakana => Romaji"}],
                [{"text": "Romaji => Hiragana"}],
                [{"text": "Romaji => Katakana"}],
                [{"text": "Hiragana => Katakana"}],
                [{"text": "Katakana => Hiragana"}],
            ],
            "one_time_keyboard": True,
        },
        parse_mode="HTML",
    )


dispatcher.add_handler(CommandHandler("gamemode", gamemode))


def play(update: Update, context: CallbackContext):
    mode = context.user_data.get("gamemode")
    if not mode:
        context.user_data["gamemode"] = 0
        return gamemode(update, context)
    mode = mode.split("/")
    chars = random.randint(1, 5)
    question = generate_kana(chars)
    ans = "".join(question[mode[1]])
    _keyboard = list(
        map(
            lambda x: [{"text": "".join(generate_kana(chars)[mode[1]])}],
            range(3),
        )
    ) + [[{"text": ans}]]
    random.shuffle(_keyboard)
    context.user_data["answer"] = ans
    context.bot.send_message(
        chat_id=update.message.chat.id,
        text="<b>{}</b> in {}...?".format(
            f'"{"".join(question[mode[0]])}"'
            if mode[0] == "romaji"
            else f'「{"".join(question[mode[0]])}」',
            mode[1].capitalize(),
        ),
        reply_markup={
            "keyboard": _keyboard,
        },
        parse_mode="HTML",
    )


dispatcher.add_handler(CommandHandler("play", play))


def quit(update: Update, context: CallbackContext):
    ans = context.user_data["answer"]
    context.user_data["answer"] = None
    context.bot.send_message(
        chat_id=update.message.chat.id,
        text="<b>Game cancelled.</b>\n\nThe answer is: <b>{}</b>\n\n<i>Type /play to play again.</i>".format(
            ans
        ),
        reply_markup={"keyboard": [[{"text": "/play"}]], "resize_keyboard": True},
        parse_mode="HTML",
    )


dispatcher.add_handler(CommandHandler("quit", quit))


def handler(update: Update, context: CallbackContext):
    text = update.message.text
    mode = context.user_data.get("gamemode")

    def done():
        if mode == 0:
            return play(update, context)
        else:
            return context.bot.send_message(
                chat_id=update.message.chat.id,
                text="<b>Game mode changed.</b>\n\n<i>Type /play to play.</i>",
                reply_markup={
                    "keyboard": [[{"text": "/play"}]],
                    "resize_keyboard": True,
                },
                parse_mode="HTML",
            )

    if not mode:
        if text == "Hiragana => Romaji":
            context.user_data["gamemode"] = "hiragana/romaji"
            return done()
        elif text == "Katakana => Romaji":
            context.user_data["gamemode"] = "katakana/romaji"
            return done()
        elif text == "Romaji => Hiragana":
            context.user_data["gamemode"] = "romaji/hiragana"
            return done()
        elif text == "Romaji => Katakana":
            context.user_data["gamemode"] = "romaji/katakana"
            return done()
        elif text == "Hiragana => Katakana":
            context.user_data["gamemode"] = "hiragana/katakana"
            return done()
        elif text == "Katakana => Hiragana":
            context.user_data["gamemode"] = "katakana/hiragana"
            return done()
        else:
            return gamemode(update, context)
    ans = context.user_data.get("answer")
    if not ans:
        context.bot.send_message(
            chat_id=update.message.chat.id,
            text="<b>Type /play to play.</b>",
            reply_markup={
                "keyboard": [[{"text": "/play"}]],
                "resize_keyboard": True,
            },
            parse_mode="HTML",
        )
    elif text.lower().strip() == ans:
        context.bot.send_message(
            chat_id=update.message.chat.id, text="<b>Correct!</b> 🌟", parse_mode="HTML"
        )
        return play(update, context)
    else:
        context.bot.send_message(
            chat_id=update.message.chat.id,
            text="<b>Wrong.</b> ❌\n\nThe answer is: <b>{}</b>".format(ans),
            parse_mode="HTML",
        )
        return play(update, context)


dispatcher.add_handler(MessageHandler(Filters.text, handler))

updater.start_polling()

updater.idle()
