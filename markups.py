from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, message
from localization import  get_localization

def LanguageMarkup(username):
    language_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    language_btns = ["Русский 🇷🇺", "English 🇬🇧", get_localization('back_btn', username)]
    language_markup.add(*language_btns)
    return language_markup

def MenuMarkup(username):
    menu_btns = ReplyKeyboardMarkup(resize_keyboard=True)
    m_btns = [get_localization('find_game_btn', username), get_localization('create_game_btn', username), get_localization('lang_btn', username)]
    menu_btns.add(*m_btns)
    return menu_btns

def FinishMarkup(username):
    finish_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    finish_btns = [get_localization('retry_btn', username), get_localization('exit_btn', username)]
    finish_markup.add(*finish_btns)
    return finish_markup

def EmptyMarkup():
    empty_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    return empty_markup

def WaitingTurnMarkup(username):
    waiting_turn_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    waiting_turn_btns = [get_localization('exit_btn', username)]
    waiting_turn_markup.add(*waiting_turn_btns)
    return waiting_turn_markup

def MakeTurnMarkup(username):
    make_turn_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    make_turn_btns = ["[1, 1]", "[1, 2]", "[1, 3]", "[2, 1]", "[2, 2]", "[2, 3]", "[3, 1]", "[3, 2]", "[3, 3]", get_localization('exit_btn', username)]
    make_turn_markup.add(*make_turn_btns)
    return make_turn_markup