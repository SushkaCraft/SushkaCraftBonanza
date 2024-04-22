import telebot
import time
import random
import sqlite3


TOKEN = '7131618116:AAHy-F5_4y2Xqx5P2q2JhbE22J6lr129K0Y'


bot = telebot.TeleBot(TOKEN)


conn = sqlite3.connect('gamedata.db')
cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                  (id INTEGER PRIMARY KEY, user_id INTEGER, username TEXT, balance INTEGER, admin INTEGER)''')
conn.commit()


symbols_info = {
    "❤": {"probability": 6, "count_needed": 8, "multiplier": 50},
    "💜": {"probability": 7, "count_needed": 8, "multiplier": 25},
    "💚": {"probability": 8, "count_needed": 8, "multiplier": 15},
    "💙": {"probability": 9, "count_needed": 8, "multiplier": 12},
    "🍎": {"probability": 12, "count_needed": 8, "multiplier": 10},
    "🍑": {"probability": 12.95, "count_needed": 8, "multiplier": 8},
    "🍉": {"probability": 13.25, "count_needed": 8, "multiplier": 5},
    "🍇": {"probability": 14.5, "count_needed": 8, "multiplier": 4},
    "🍌": {"probability": 15.8, "count_needed": 8, "multiplier": 2},
    "🍭": {"probability": 1.5, "count_needed": 4, "multiplier": None}
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

def send_game_board(message, board):
    symbol_counts = {symbol: 0 for symbol in symbols_info}
    for row in board:
        for symbol in row:
            symbol_counts[symbol] += 1

    board_display = "\n".join(" ".join(row) for row in board)
    result_message = "Игровое поле:\n" + board_display
    played_symbols = []

    for symbol, count in symbol_counts.items():
        info = symbols_info[symbol]
        if count >= info['count_needed']:
            played_symbols.append(f"Символ {symbol} сыграл, всего на поле {count} шт.")

    if played_symbols:
        result_message += "\n" + "\n".join(played_symbols)
        bot.send_message(message.chat.id, result_message)
        update_board(board, symbol_counts)
        time.sleep(1)
        send_game_board(message, board)
    else:
        bot.send_message(message.chat.id, result_message + "\nНи один символ не сыграл\nСыграть ещё раз /play")

@bot.message_handler(commands=['play'])
def handle_play(message):
    board = create_board(6, 5)
    send_game_board(message, board)

bot.polling()
