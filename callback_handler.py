from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, message
from bot_data import *
from main import start_game

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
    await call.message.answer(f'Присоединился к {room_id};')
    await bot.send_message(opponent_id, f'Пользователь {username} присоединился к вашей игре.')
    await call.answer()
    await start_game(room_id)