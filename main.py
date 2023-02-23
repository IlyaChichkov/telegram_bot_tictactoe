import random

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, message

from bot_data import *
import callback_handler

menu_btns = ReplyKeyboardMarkup(resize_keyboard=True)
m_btns = ["Найти игру", "Создать игру"]
menu_btns.add(*m_btns)

finish_markup = ReplyKeyboardMarkup(resize_keyboard=True)
finish_btns = ["Заново", "Выйти"]
finish_markup.add(*finish_btns)

empty_markup = ReplyKeyboardMarkup(resize_keyboard=True)

waiting_turn_markup = ReplyKeyboardMarkup(resize_keyboard=True)
waiting_turn_btns = ["Выйти"]
waiting_turn_markup.add(*waiting_turn_btns)

make_turn_markup = ReplyKeyboardMarkup(resize_keyboard=True)
make_turn_btns = ["[1, 1]", "[1, 2]", "[1, 3]", "[2, 1]", "[2, 2]", "[2, 3]", "[3, 1]", "[3, 2]", "[3, 3]", "Выйти из игры"]
make_turn_markup.add(*make_turn_btns)

async def start_game(room_id):
    player_ids = get_players_at_room(room_id)

    await bot.send_message(player_ids[0], f'Игра начинается')
    await bot.send_message(player_ids[1], f'Игра начинается')

    player_turn = random.randint(0, 1)
    player_idle = (1, 0)[player_turn == 1]
    room = get_room(room_id)
    reset_room(room)
    player_turn_name = room['players'][player_turn]
    player_idle_name = room['players'][player_idle]

    print('Current turn: ', player_turn_name)
    print('Waiting turn: ', player_idle_name)
    set_room_turn(room, player_turn_name)
    set_player_sides(room, player_turn_name, player_idle_name)

    set_player_state(player_turn_name, PLAYER_STATE.MAKING_TURN)
    set_player_state(player_idle_name, PLAYER_STATE.WAITING_TURN)

    player_turn_id = get_player_id(player_turn_name)
    player_idle_id = get_player_id(player_idle_name)
    await show_map(room)
    await bot.send_message(player_turn_id, f'Ваш ход', reply_markup=make_turn_markup)
    await bot.send_message(player_idle_id, f'Сейчас ход оппонента', reply_markup=waiting_turn_markup)

async def check_win_state(room):
    room_map = room['map']
    winner = 0

    # Horizontal
    if room_map[0][0] == room_map[0][1] and room_map[0][1] == room_map[0][2] and room_map[0][1] != 0:
        winner = room_map[0][1]

    if room_map[1][0] == room_map[1][1] and room_map[1][1] == room_map[1][2] and room_map[1][1] != 0:
        winner = room_map[1][1]

    if room_map[2][0] == room_map[2][1] and room_map[2][1] == room_map[2][2] and room_map[2][1] != 0:
        winner = room_map[2][1]

    # Vertical
    if room_map[0][0] == room_map[1][0] and room_map[0][0] == room_map[2][0] and room_map[0][0] != 0:
        winner = room_map[0][0]

    if room_map[0][1] == room_map[1][1] and room_map[0][1] == room_map[2][1] and room_map[0][1] != 0:
        winner = room_map[0][1]

    if room_map[0][2] == room_map[1][2] and room_map[0][2] == room_map[2][2] and room_map[0][2] != 0:
        winner = room_map[0][2]

    # Diagonal
    if room_map[0][0] == room_map[1][1] and room_map[0][0] == room_map[2][2] and room_map[0][0] != 0:
        winner = room_map[0][0]

    if room_map[0][2] == room_map[1][1] and room_map[1][1] == room_map[2][0] and room_map[0][2] != 0:
        winner = room_map[0][2]

    hasZeros = False
    if winner == 0:
        for row in room_map:
            for item in row:
                if item == 0:
                    hasZeros = True

    if winner != 0:
        winner_name = ''
        loser_name = ''
        if winner == 1:
            winner_name = room['cross']
            loser_name = room['circle']
        else:
            loser_name = room['cross']
            winner_name = room['circle']

        loser_id = get_player_id(loser_name)
        winner_id = get_player_id(winner_name)
        await bot.send_message(loser_id, f'Вы проиграли!', reply_markup=finish_markup)
        await bot.send_message(winner_id, f'Вы победили!', reply_markup=finish_markup)
        return True
    else:
        if not hasZeros:
            pl0 = room['cross']
            pl1 = room['circle']
            pl0_id = get_player_id(pl0)
            pl1_id = get_player_id(pl1)
            await bot.send_message(pl0_id, f'Ничья.', reply_markup=finish_markup)
            await bot.send_message(pl1_id, f'Ничья.', reply_markup=finish_markup)
            return True
        return False


async def change_turn(player_turn_name, room):
    room_players = room['players'].copy()
    room_players.remove(player_turn_name)
    opponent_name = room_players[0]
    set_room_turn(room, opponent_name)
    set_player_state(opponent_name, PLAYER_STATE.MAKING_TURN)
    set_player_state(player_turn_name, PLAYER_STATE.WAITING_TURN)
    opponent_id = get_player_id(opponent_name)
    player_turn_id = get_player_id(player_turn_name)
    await bot.send_message(opponent_id, f'Ваш ход', reply_markup=make_turn_markup)
    await bot.send_message(player_turn_id, f'Сейчас ход оппонента', reply_markup=waiting_turn_markup)

async def show_map(room):
    cross = '❎'
    circle = '✅'
    empty = '🔲'
    tictactoe_map = ''
    room_map = room['map']
    for row in room_map:
        for item in row:
            if item == 1:
                tictactoe_map += cross
            elif item == 2:
                tictactoe_map += circle
            else:
                tictactoe_map += empty
        tictactoe_map += '\n'

    players_id = get_players_at_room(room['id'])
    for pl in players_id:
        await bot.send_message(pl, tictactoe_map)

async def show_games(message: types.Message):
    add_player(message.from_user)
    userName = str(message.from_user.username)
    print('show games for ', userName)
    if(is_player_state(userName, PLAYER_STATE.WAITING_OPPONENT)):
        remove_from_room(userName, get_player_room(userName))
        set_player_state(userName, PLAYER_STATE.IDLE)

    if len(games) < 1:
        await message.reply('Пусто...')
        return

    for game in games:
        if game['isOpen']:
            join_callback = f'join;{str(game["id"])};{message.from_user.username};{message.from_user.id}'
            print('IMPORTANT: Join room callback: ', join_callback)
            join_btn = types.InlineKeyboardMarkup()
            join_btn.add(InlineKeyboardButton('Присоединиться', callback_data=join_callback))
            game_info = f"ID: {game['id']}, Игроки: { ''.join(game['players']) }"
            await message.reply(game_info, reply_markup=join_btn)

@dp.message_handler(Text(equals=["Выйти", "Выйти из игры"]))
async def exit_room(message: types.Message):
    print('WARNING: Exiting room!')
    add_player(message.from_user)
    user = message.from_user
    username = user.username
    set_player_state(username, PLAYER_STATE.IDLE)
    room_id = get_player_room(username)
    remove_from_room(username, room_id)
    # make opponent know
    room = get_room(room_id)
    players_ids = get_players_at_room(room_id)
    print('ids in room: ', players_ids)
    if(len(players_ids) > 0):
        opponent_id = players_ids[0]
        set_player_state(room['players'][0], PLAYER_STATE.WAITING_OPPONENT)
        await bot.send_message(opponent_id, f'Игрок {username} вышел. Ожидание игроков...', reply_markup=waiting_turn_markup)

    await message.reply("Меню:", reply_markup=menu_btns)

@dp.message_handler(Text(equals="Найти игру"))
async def find_room(message: types.Message):
    await show_games(message)

@dp.message_handler(Text(equals="Заново"))
async def find_room(message: types.Message):
    room_id = get_player_room(message.from_user.username)
    await start_game(room_id)

@dp.message_handler(Text(startswith="["))
async def cell_select(message: types.Message):
    userName = str(message.from_user.username)
    room = get_room(get_player_room(userName))
    userSide = get_user_side(room, userName)
    print(userSide)
    print(message.text)
    y = int(message.text.split(',')[0].replace('[', '')) - 1
    x = int(message.text.split(',')[1].replace(']', '')) - 1
    print(x, y)
    room_map = room['map']
    cell_set = 0
    match userSide:
        case 'cross':
            cell_set = 1
        case 'circle':
            cell_set = 2
        case 'none':
            cell_set = 0

    if (room_map[y][x] == 0):
        room_map[y][x] = cell_set
        await show_map(room)
        if await check_win_state(room):
            return
        await change_turn(userName, room)
    else:
        await show_map(room)
        await bot.send_message(message.from_user.id, 'Попробуй еще раз', reply_markup=make_turn_markup)

@dp.message_handler(Text(equals='Создать игру'))
async def create_room(message: types.Message):
    add_player(message.from_user)
    userName = str(message.from_user.username)
    if not is_player_state(userName, PLAYER_STATE.IDLE):
        return
    roomId = random.randint(10000000, 99999999)
    games.append({
        'id': roomId,
        'players': [userName],
        'currentTurn': '',
        'map': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        'isOpen': True
    })
    set_player_state(userName, PLAYER_STATE.WAITING_OPPONENT)
    set_player_room(userName, roomId)
    await message.answer('Ожидаем игроков...', reply_markup=waiting_turn_markup)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    add_player(message.from_user)
    await message.reply("Игра в крестики нолики", reply_markup=menu_btns)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)