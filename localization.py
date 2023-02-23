from bot_data import get_player_lang, set_player_lang

language = 'ru'

localization_dict = {
    'try_again': {'ru': 'Попробуй еще раз', 'en': 'Try again'},
    'waiting_players': {'ru': 'Ожидаем игроков...', 'en': 'Waiting players...'},
    'menu': {'ru': 'Меню', 'en': 'Menu'},
    'lang_change': {'ru': 'Выбор языка', 'en': 'Choose language'},
    'your_turn': {'ru': 'Ваш ход', 'en': 'Your turn'},
    'opponent_turn': {'ru': 'Сейчас ход оппонента', 'en': 'Opponent turn'},
    'draw': {'ru': 'Ничья.', 'en': 'Draw.'},
    'you_win': {'ru': 'Вы победили!', 'en': 'You win!'},
    'you_lost': {'ru': 'Вы проиграли!', 'en': 'You lost!'},
    'game_starts': {'ru': 'Игра начинается', 'en': 'The game starts'},
    'find_game_btn': {'ru': 'Найти игру', 'en': 'Search games'},
    'create_game_btn': {'ru': 'Создать игру', 'en': 'Create new game'},
    'lang_btn': {'ru': 'Язык', 'en': 'Language'},
    'retry_btn': {'ru': 'Заново', 'en': 'Retry'},
    'exit_btn': {'ru': 'Выйти', 'en': 'Exit'},
    'back_btn': {'ru': 'Назад', 'en': 'Back'},
    'user': {'ru': 'Пользователь', 'en': 'User'},
    'joined': {'ru': 'присоединился к вашей игре.', 'en': 'joined your game.'},
    'you_joined': {'ru': 'Присоединился к', 'en': 'Joined the'},
    'player': {'ru': 'Игрок', 'en': 'Player'},
    'players': {'ru': 'Игроки', 'en': 'Players'},
    'title': {'ru': 'Крестики нолики', 'en': 'Tic Tac Toe'},
    'no_rooms': {'ru': 'Нет комнат, чтобы присоединиться', 'en': 'No rooms to join'},
    'join_btn': {'ru': 'Присоединиться', 'en': 'Join'},
    'player_exit': {'ru': 'вышел. Ожидание игроков...', 'en': ' exit. Waiting for players...'}
}

def change_lang(newLang, username):
    set_player_lang(username, newLang)

def get_localization(value, username):
    global language
    return localization_dict[value][get_player_lang(username)]

def get_word_localizations(word):
    return localization_dict[word].values()