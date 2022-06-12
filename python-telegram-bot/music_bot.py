import logging
import random
from click import command
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    Updater,
    Filters,
    CallbackQueryHandler,
)

# KEEP API TOKEN SECRET :P
BOT_TOKEN = "<- YOUR TOKEN HERE ->"
bot = Bot(token=BOT_TOKEN)

# LOGGING
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Declare global dictionary to store user choices
data = {}


# SONGS FILE_IDs
playlist = [
    [
        "CQACAgUAAxkBAANZYqUAAVVMObGIX6LQW14Bt6PT4ZOTAAJvBgACVhYpVZSYyOtPDOQTJAQ",
        "CQACAgUAAxkBAANbYqUAAViCk5y7qzJB4KKQEE-1H4ciAAJwBgACVhYpVVbn7sx2JDmMJAQ",
        "CQACAgUAAxkBAANdYqUAAVp9hbEl0VlqTX3ENdAbw5XIAAJxBgACVhYpVRAwg-1mdw77JAQ",
        "CQACAgUAAxkBAANfYqUAAV2uygQuZFgogjYoy8n-6WToAAJyBgACVhYpVSzKeTc7R34IJAQ",
        "CQACAgUAAxkBAANhYqUAAWAtLZT3wXHCxR0fbuzGTTvdAAJzBgACVhYpVXhqkgdSO-ujJAQ",
        "CQACAgUAAxkBAANjYqUAAWP9cuxE7EgxTvTf-DG1IPRcAAJ0BgACVhYpVYcf3_AvxxpFJAQ",
    ],
    [
        "CQACAgUAAxkBAANlYqUAAWUfKL5-wA5MXaAhyJnxVLldAAJ1BgACVhYpVScQeKpcyYoNJAQ",
        "CQACAgUAAxkBAANnYqUAAWh7nAmqq1p9J1oDd8EcHojhAAJ2BgACVhYpVZ9iui6EOR5EJAQ",
        "CQACAgUAAxkBAANpYqUAAWvJkXe2n956NxfuE98z79apAAJ3BgACVhYpVUT3VCYqF7KjJAQ",
        "CQACAgUAAxkBAANrYqUAAW3WDn-g8Nxwnbui1WXED7kJAAJ4BgACVhYpVceLoRaFYkIpJAQ",
        "CQACAgUAAxkBAANtYqUAAXBz7Y8O7FhyFqigJ-q3u4pLAAJ5BgACVhYpVQyHcrxJU_WGJAQ",
        "CQACAgUAAxkBAANvYqUAAXISqEMcoFaCru-FpQ7TV7s6AAJ6BgACVhYpVbItmvoqnv5_JAQ",
    ],
    [
        "CQACAgUAAxkBAANxYqUAAXRA6qTTIMbAPQ_LfeQ2jeb3AAJ7BgACVhYpVSuUG82IMlJvJAQ",
        "CQACAgUAAxkBAANzYqUAAXe2PbA1AAFbsy7KoyhGc3DykAACfAYAAlYWKVUku7LGII_ikiQE",
        "CQACAgUAAxkBAAN1YqUAAXoRot1xNWBr-QotZzJ8ZNM-AAJ9BgACVhYpVYHnW1UcVs4qJAQ",
        "CQACAgUAAxkBAAN3YqUAAXwJvwkaVC9HYtisvNTZzMTkAAJ-BgACVhYpVRl_eU7gXztVJAQ",
        "CQACAgUAAxkBAAN5YqUAAYAbnR0Y9Lc_RtkUdBnnvJZ0AAJ_BgACVhYpVU1Ft9h3ufcjJAQ",
        "CQACAgUAAxkBAAN7YqUAAYMZT4BK8brWdirpvWCYsfzoAAKABgACVhYpVbcrYA6XCyFYJAQ",
    ],
]

# Add all songs to a unified list
all = list()
all.extend(song for play in playlist for song in play)
# all.extend(playlist[0])
# all.extend(playlist[1])
# all.extend(playlist[2])

# KEYBOARDS

main_options = [
    [InlineKeyboardButton(text="Random", callback_data="random")],
    [InlineKeyboardButton(text="Shuffle", callback_data="shuffle")],
    [InlineKeyboardButton(text="Random Shuffle", callback_data="random_shuffle")],
    [InlineKeyboardButton(text="All", callback_data="all")],
]

playist_option = [
    [InlineKeyboardButton(text="Playlist 1", callback_data='0')],
    [InlineKeyboardButton(text="Playlist 2", callback_data='1')],
    [InlineKeyboardButton(text="Playlist 3", callback_data='2')],
]

main_options_markup = InlineKeyboardMarkup(main_options)

playist_option_markup = InlineKeyboardMarkup(playist_option)


def file_id_command(update, context):
    """Retrive file Id from the audio sent"""
    bot.send_message(
        chat_id=update.effective_user.id, text=f"{update.message.audio.file_id}"
    )


def start_command(update, context):
    bot.send_message(
        chat_id=update.effective_user.id, text="Hey There\nWelcome to NCS MUSIC BOT :D"
    )


def song(update, context):
    # CREATE A SIMPLE DICT TO STORE USER CHOICES
    data.update({update.effective_user.id: {}})
    bot.send_message(
        chat_id=update.effective_user.id,
        text="Choose one\n",
        reply_markup=main_options_markup,
    )
    return options_choice


def options_choice(update, context):
    option = update.callback_query
    option.answer()
    data[update.effective_user.id]["option"] = option.data
    if option.data == "random":
        option.edit_message_text(
            text="Choose a playlist\n",
            reply_markup=playist_option_markup,
        )
        return playlist_choice
    if option.data == "shuffle":
        option.edit_message_text(
            text="Choose a playlist\n",
            reply_markup=playist_option_markup,
        )
        return playlist_choice
    if option.data == "random_shuffle":
        option.edit_message_text(text="Enter a number\n")
        data[update.effective_user.id]["accept"] = 0
        return user_req
    if option.data == "all":
        option.delete_message()
        data[update.effective_user.id]["accept"] = 0
        send_songs(update, context)


def playlist_choice(update, context):
    query = update.callback_query
    query.answer()
    data[update.effective_user.id]["playlist"] = int(query.data)
    print(query.data)
    if ( query.data == '0' or query.data == '1' or query.data == '2' ):
        if data[update.effective_user.id]["option"] == 'random':
            query.edit_message_text(text="Enter a number\n")
            data[update.effective_user.id]["accept"] = 0
            return user_req
        else:
            query.delete_message()
            send_songs(update,context)


def user_req(update, context):
    # try:
    if data[update.effective_user.id]["accept"] == 0:
        data[update.effective_user.id]["num_songs"] = int(update.message.text)
        print(update.message.text)
        data[update.effective_user.id]["accept"] = 1
        send_songs(update, context)
    # except Exception as e:
    #     print(e)


def send_songs(update, context):
    """Send songs to user, depending on the option,playlist and option

    Args:
        update (_type_): Telegram update class
        option (str): random / shuffle / random_shuffle / all
        number (int): No of songs to be sent

    """
    if (
        data[update.effective_user.id]["option"] == "random"
        or data[update.effective_user.id]["option"] == "shuffle"
        or data[update.effective_user.id]["option"] == "random_shuffle"
    ):
        
        if data[update.effective_user.id]["option"] == "random":
            # songs = random.shuffle(playlist[data[update.effective_user.id]["playlist"]])
            songs = playlist[data[update.effective_user.id]["playlist"]]
            random.shuffle(songs)
            random_songs = songs[0:data[update.effective_user.id]["num_songs"]]
            for _ in random_songs:
                bot.send_audio(chat_id=update.effective_user.id, audio=_)
        elif data[update.effective_user.id]["option"] == "shuffle":
            songs = playlist[data[update.effective_user.id]["playlist"]]
            random.shuffle(songs)
            for _ in songs:
                bot.send_audio(chat_id=update.effective_user.id, audio=_)
        elif data[update.effective_user.id]["option"] == "random_shuffle":
            all_songs = all.copy()
            random.shuffle(all_songs)
            songs = all_songs[0 : data[update.effective_user.id]["num_songs"]]
            for _ in songs:
                bot.send_audio(chat_id=update.effective_user.id, audio=_)
    elif data[update.effective_user.id]["option"] == "all":
        for song in all:
            bot.send_audio(chat_id=update.effective_user.id, audio=song)


def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.audio, file_id_command))
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("song", song))
    dp.add_handler(
        CallbackQueryHandler(
            options_choice, pattern="^random|shuffle|random_shuffle|all$"
        )
    )
    dp.add_handler(
        CallbackQueryHandler(playlist_choice, pattern="^0|1|2$")
    )
    dp.add_handler(MessageHandler((Filters.text & (~Filters.command)), user_req))
    updater.start_polling()


if __name__ == "__main__":
    main()
