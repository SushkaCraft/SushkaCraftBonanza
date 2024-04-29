import telebot
from telebot import types

import sqlite3

import time
import random


TOKEN = 'TOKEN'


bot = telebot.TeleBot(TOKEN)


conn = sqlite3.connect('gamedata.db', check_same_thread=False)
cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                  (id INTEGER PRIMARY KEY,
                  user_id INTEGER,
                  username TEXT,
                  balance INTEGER DEFAULT 0,
                  bet INTEGER DEFAULT 0,
                  admin INTEGER)''')
conn.commit()


def get_or_create_user(user_id):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    if not user:
        cursor.execute('INSERT INTO users (user_id, balance, admin) VALUES (?, 0, 0)', (user_id,))
        conn.commit()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
    return user


symbols_info = {
    "❤": {"probability": 7, "count_needed": 8, "multiplier": 50},
    "💜": {"probability": 7, "count_needed": 8, "multiplier": 25},
    "💚": {"probability": 7, "count_needed": 8, "multiplier": 15},
    "💙": {"probability": 7, "count_needed": 8, "multiplier": 12},
    "🍎": {"probability": 14, "count_needed": 8, "multiplier": 10},
    "🍑": {"probability": 14, "count_needed": 8, "multiplier": 8},
    "🍉": {"probability": 14, "count_needed": 8, "multiplier": 5},
    "🍇": {"probability": 14, "count_needed": 8, "multiplier": 4},
    "🍌": {"probability": 14.5, "count_needed": 8, "multiplier": 2},
    "🍭": {"probability": 1.5, "count_needed": 4, "multiplier": 1200}
    #Для реализации бонуски нужно установить множитель как None и дописать соответствующую функцию
}


def create_board(width, height):
    return [[random.choices(population=list(symbols_info.keys()),
            weights=[info['probability'] for info in symbols_info.values()])[0] for _ in range(width)] for _ in range(height)]


def update_board(board, symbol_counts):
    for j in range(len(board[0])):
        column = [board[i][j] for i in range(len(board))]
        new_column = [sym for sym in column if symbol_counts[sym] < symbols_info[sym]['count_needed']]
        while len(new_column) < len(board):
            new_column.insert(0, random.choices(population=list(symbols_info.keys()),
                        weights=[info['probability'] for info in symbols_info.values()])[0])
        for i in range(len(board)):
            board[i][j] = new_column[i]


def send_game_board(message, board, bet):
    user_id = message.from_user.id
    user = get_or_create_user(user_id)

    symbol_counts = {symbol: 0 for symbol in symbols_info}
    for row in board:
        for symbol in row:
            symbol_counts[symbol] += 1

    board_display = "\n".join(" ".join(row) for row in board)
    result_message = "Игровое поле:\n" + board_display
    played_symbols = []
    win = 0

    for symbol, count in symbol_counts.items():
        info = symbols_info[symbol]
        if count >= info['count_needed']:
            played_symbols.append(f"Символ {symbol} сыграл, всего на поле {count} шт.")
            if info['multiplier']:
                win += bet * info['multiplier']

    if played_symbols:
        result_message += "\n" + "\n".join(played_symbols)
        bot.send_message(message.chat.id, result_message + f"\nВаш выигрыш составил {win}₽")
        update_board(board, symbol_counts)
        cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (win, user_id))
        conn.commit()
        time.sleep(1)
        send_game_board(message, board, bet)
    else:
        bot.send_message(message.chat.id,
                         result_message + "\nНи один символ не сыграл\nСыграть ещё раз /play\nВы ничего не выиграли.")


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Добро пожаловать! Это слот от SushkaCraft! Для начала игры введите /play\nДля пополнения баланса введите команду /balance")


@bot.message_handler(commands=['play'])
def handle_play(message):
    user_id = message.from_user.id
    user = get_or_create_user(user_id)

    if user[4] == 0:
        bot.send_message(message.chat.id, "Пожалуйста, установите ставку командой /bet.")
        return

    if user[3] < user[4]:
        bot.send_message(message.chat.id, "Недостаточно средств на балансе.")
        return

    cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (user[4], user_id))
    conn.commit()

    board = create_board(6, 5)
    send_game_board(message, board, user[4])


@bot.message_handler(commands=['balance'])
def handle_balance(message):
    user = get_or_create_user(message.from_user.id)
    markup = types.InlineKeyboardMarkup()
    button_deposit = types.InlineKeyboardButton("Пополнить", callback_data='deposit')
    button_withdraw = types.InlineKeyboardButton("Вывести", callback_data='withdraw')
    markup.add(button_deposit, button_withdraw)
    bot.send_message(message.chat.id, f"Ваш баланс: {user[3]}₽", reply_markup=markup)


@bot.message_handler(commands=['bet'])
def handle_bet(message):
    msg = bot.send_message(message.chat.id, "Введите размер ставки (минимальный размер 10):")
    bot.register_next_step_handler(msg, set_bet, message.from_user.id)


def set_bet(message, user_id):
    bet_size = int(message.text)
    if bet_size < 10:
        bot.send_message(message.chat.id, "Ставка должна быть не менее 10.")
        return
    cursor.execute('UPDATE users SET bet = ? WHERE user_id = ?', (bet_size, user_id))
    conn.commit()
    bot.send_message(message.chat.id, f"Ставка установлена: {bet_size}₽")


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'deposit':
        msg = bot.send_message(call.message.chat.id, "Введите сумму для пополнения:")
        bot.register_next_step_handler(msg, process_deposit_amount, call.from_user.id)
    elif call.data == 'withdraw':
        bot.answer_callback_query(call.id, "Вывод не доступен", show_alert=True)


def process_deposit_amount(message, user_id):
    amount = int(message.text)
    cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount, user_id))
    conn.commit()
    bot.send_message(message.chat.id, f"Ваш баланс успешно пополнен на {amount}₽")


bot.polling()
