from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, message
from bot_data import *
from main import start_game
from localization import get_localization
@dp.callback_query_handler(Text(startswith="join;"))
async def joining_room(call: types.CallbackQuery):
    callback_data = call.data.split(";")
    print('callback ', callback_data)
    room_id = callback_data[1]
    username = callback_data[2]
    user_id = callback_data[3]

    player_ids = get_players_at_room(room_id)
    opponent_id = player_ids[0]
    add_to_room(username, room_id)
    await call.message.answer(f'{get_localization("you_joined", get_player_name(user_id))} {room_id};')
    await bot.send_message(opponent_id, f'{get_localization("user", get_player_name(opponent_id))} {username} {get_localization("joined",  get_player_name(opponent_id))}')
    await call.answer()
    await start_game(room_id)