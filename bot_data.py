import aiogram.types
from aiogram import Bot, Dispatcher, executor, types
from enum import Enum

API_TOKEN = '5931483729:AAHxVMTbfCbndvzSNmDcdQfPWHtxYxnGOUo'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

players = {}
games = []

class PLAYER_STATE(Enum):
    IDLE = 0
    WAITING_OPPONENT = 1
    MAKING_TURN = 2
    WAITING_TURN = 3

def add_player(user: aiogram.types.user.User):
    username = user.username
    user_id = user.id
    if username not in players:
        print('Add new player: ', username)
        players[username] = str(PLAYER_STATE(PLAYER_STATE.IDLE)) + ';NoRoom;' + str(user_id) + ';en'
    else:
        print(f'Player already exist: {username}; Data: {players[username]}')

def get_player_lang(username):
    return players[username].split(';')[3]

def get_player_name(user_id):
    for player in players:
        data = players[player].split(';')
        if str(data[2]) == str(user_id):
            return player
    return 'None'

def set_player_lang(username, lang):
    players[username] = players[username].split(';')[0] + ';' + players[username].split(';')[1] + ';' + str(players[username].split(';')[2]) + ';' + lang

def set_player_state(username, state: PLAYER_STATE):
    print('new state: ', state)
    players[username] = str(PLAYER_STATE(state)) + ';' + players[username].split(';')[1] + ';' + str(players[username].split(';')[2]) + ';' + str(players[username].split(';')[3])
    print(f'set {username} state ', players[username])

def set_player_room(username, room_id):
    state = players[username].split(';')[0]
    user_id = players[username].split(';')[2]
    user_lang = players[username].split(';')[3]
    players[username] = str(state) + ';' + str(room_id) + ';' + str(user_id)  + ';' + str(user_lang)

def get_player_state(username):
    state = players[username].split(';')[0]
    print(f'get player {players[username]} state: {state}')
    return state

def get_room(room_id):
    for room in games:
        if str(room['id']) == str(room_id):
            return room
    return None

def get_player_id(username):
    print('INFO: Current global players in game: ', players)
    id = players[username].split(';')[2]
    print(f'get player {players[username]} id: {id}')
    return id

def get_player_room(username):
    room_id = players[username].split(';')[1]
    return room_id

def get_players_at_room(room_id):
    print(f"GET: Players at room {room_id}")
    players_arr = []
    for room in games:
        if str(room['id']) == str(room_id):
            print("Players: ", room['players'])
            for pl in room['players']:
                players_arr.append(get_player_id(pl))
    return players_arr

def is_player_state(username, state: PLAYER_STATE):
    print(f'compare player {players[username]} state to {state}')
    print(f'get_player_state {get_player_state(username)}')
    if(str(get_player_state(username)) == str(state)):
        print('> True')
        return True
    return False

def get_player_room(username):
    playerRoomId = str(players[username].split(';')[1])
    for room in games:
        if str(room['id']) == str(playerRoomId):
            print(f'get_player_room found {username} in {room["id"]}')
            return str(room['id'])
    return 'NoRoom'

def add_to_room(username, room_id):
    print(games)
    set_player_room(username, room_id)
    for game in games:
        if str(game['id']) == str(room_id):
            if game['isOpen'] == False:
                print('ERROR: Can`t connect, room is already full!')
                return

            game['players'].append(username)

            if len(game['players']) > 1:
                game['isOpen'] = False

def set_room_turn(room, username):
    room['currentTurn'] = username

def set_player_sides(room, player_cross, player_circle):
    room['cross'] = player_cross
    room['circle'] = player_circle

def get_user_side(room, username):
    print(f'GET: Player {username} side is ')
    if room['cross'] == username:
        print('cross')
        return 'cross'
    if room['circle'] == username:
        print('circle')
        return 'circle'
    return 'none'

def remove_from_room(username, room_id):
    print(f'remove {username} from room {room_id}')
    set_player_room(username, 'NoRoom')
    for room in games:
        if str(room['id']) == room_id:
            room['players'].remove(username)
            players_count = len(room['players'])
            if players_count < 1:
                games.remove(room)
            elif players_count == 1:
                room['isOpen'] = True

def reset_room(room):
    room['map'] = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

'''
games = [
    {
        'id': 61356125,
        'players': ['Ostin'],
        'currentTurn': '',
        'map': [],
        'isOpen': True
    },
    {
        'id': 53357822,
        'players': ['Harry', 'Tom'],
        'currentTurn': 'Tom',
        'map': [[0, 0, 0], [1, 0, 0], [0, 0, 0]],
        'isOpen': True
    }
]
'''