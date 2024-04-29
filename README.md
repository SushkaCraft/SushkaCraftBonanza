# Telegram Slot Game Bot. CraftBonanza 

## English Version
This Telegram bot simulates a slot game using emojis as symbols. The bot uses a SQLite database to store user data and game states.

## Setup

1. **Dependencies**:
    - Install `pyTelegramBotAPI` by running `pip install pyTelegramBotAPI`.
    - SQLite is used for the database, which comes built-in with Python.

2. **Database Setup**:
    - The bot initializes a SQLite database `gamedata.db`.
    - A table named `users` is created to store user information and game states.

## Commands

### `/start`
- Initializes interaction with the user.
- Welcomes the user and introduces the game commands like `/play` and `/balance`.

### `/play`
- Starts the game if the user has already set a bet.
- Checks if the user's balance is sufficient for the bet.
- Creates and sends the game board.

### `/balance`
- Displays the user's current balance.
- Provides buttons for depositing or withdrawing money (withdrawal is currently disabled).

### `/bet`
- Asks the user to set a bet amount.
- Updates the bet amount in the database.

## Function Descriptions

### Function: `get_or_create_user(user_id)`
**Purpose**: Ensures each user interacting with the bot has a database record.
**Process**:
  1. Queries the database for a user with `user_id`.
  2. If the user does not exist, inserts a new record with initial values and fetches it.
  3. Returns the user data.

### Function: `create_board(width, height)`
**Purpose**: Generates a random game board using predefined symbols and their probabilities.
**Process**:
  1. Creates a 2D grid with specified `width` and `height`.
  2. Fills each cell using a random choice of symbols based on their probabilities.

### Function: `update_board(board, symbol_counts)`
**Purpose**: Updates the game board to remove fulfilled symbols and repopulate with new ones.
**Process**:
  1. Iterates through each column and removes symbols that exceed their required counts.
  2. Adds new symbols at the top, simulating symbols "falling" down.
  3. Updates the board with the new columns.

### Function: `send_game_board(message, board, bet)`
**Purpose**: Manages game rounds, displays the board, calculates winnings, and handles user prompts.
**Process**:
  1. Retrieves or creates user data from sender's ID.
  2. Calculates symbol occurrences and constructs the board display.
  3. Sends game results to the user and updates their balance if they win.
  4. Calls itself recursively if there are winnings, otherwise prompts for next actions.

### Function: `set_bet(message, user_id)`
**Purpose**: Allows users to set their betting amount.
**Process**:
  1. Prompts for bet input.
  2. Validates and updates the bet in the database.

### Function: `handle_query(call)`
**Purpose**: Handles interactions from inline keyboard buttons for financial transactions.
**Process**:
  1. Identifies if the action is a deposit or withdrawal.
  2. Processes deposits and informs users that withdrawals are unavailable.

### Function: `process_deposit_amount(message, user_id)`
**Purpose**: Processes user deposits.
**Process**:
  1. Receives and validates the deposit amount.
  2. Updates the user's balance in the database.

## Database Structure

- **Users Table**:
  - `id`: Primary key.
  - `user_id`: Telegram user ID.
  - `username`: Telegram username.
  - `balance`: Current balance of the user.
  - `bet`: Current bet amount set by the user.

## Symbols Information

- The game uses various emoji symbols with associated probabilities, required counts, and multipliers for payouts.

## Bot Polling

- The bot uses long polling to continuously check for new updates.

## Note

- This bot is designed for demonstration purposes and does not support real money transactions.

# Телеграм-бот для игры в слоты. CraftBonanza

## Russian Version

Этот бот в Телеграме симулирует игру в слоты с использованием эмодзи в качестве символов. Бот использует базу данных SQLite для хранения данных пользователя и состояний игры.

## Настройка

1. **Зависимости**:
    - Установите `pyTelegramBotAPI`, выполнив команду `pip install pyTelegramBotAPI`.
    - Для базы данных используется SQLite, который встроен в Python.

2. **Настройка базы данных**:
    - Бот инициализирует базу данных SQLite `gamedata.db`.
    - Создается таблица `users` для хранения информации о пользователях и состояниях игры.

## Команды

### `/start`
- Инициирует взаимодействие с пользователем.
- Приветствует пользователя и представляет команды игры, такие как `/play` и `/balance`.

### `/play`
- Начинает игру, если пользователь уже установил ставку.
- Проверяет, достаточно ли средств на балансе пользователя для ставки.
- Создает и отправляет игровое поле.

### `/balance`
- Отображает текущий баланс пользователя.
- Предоставляет кнопки для пополнения или вывода денег (вывод в настоящее время отключен).

### `/bet`
- Просит пользователя установить сумму ставки.
- Обновляет сумму ставки в базе данных.

## Описание функций

### Функция: `get_or_create_user(user_id)`
**Назначение**: Обеспечивает наличие записи в базе данных для каждого пользователя, взаимодействующего с ботом.
**Процесс**:
  1. Запрашивает в базе данных пользователя с `user_id`.
  2. Если пользователя нет, вставляет новую запись с начальными значениями и извлекает ее.
  3. Возвращает данные пользователя.

### Функция: `create_board(width, height)`
**Назначение**: Генерирует случайное игровое поле с использованием предопределенных символов и их вероятностей.
**Процесс**:
  1. Создает 2D сетку с указанными `width` и `height`.
  2. Заполняет каждую ячейку случайным выбором символов на основе их вероятностей.

### Функция: `update_board(board, symbol_counts)`
**Назначение**: Обновляет игровое поле, удаляя выполненные символы и пополняя новыми.
**Процесс**:
  1. Проходит по каждому столбцу и удаляет символы, превышающие требуемое количество.
  2. Добавляет новые символы сверху, имитируя падение символов.
  3. Обновляет поле с новыми столбцами.

### Функция: `send_game_board(message, board, bet)`
**Назначение**: Управляет раундами игры, отображает поле, рассчитывает выигрыши и обрабатывает запросы пользователя.
**Процесс**:
  1. Извлекает или создает данные пользователя по ID отправителя.
  2. Рассчитывает встречаемость символов и создает дисплей поля.
  3. Отправляет результаты игры пользователю и обновляет его баланс в случае выигрыша.
  4. Вызывает себя рекурсивно, если есть выигрыши, в противном случае предлагает следующие действия.

### Функция: `set_bet(message, user_id)`
**Назначение**: Позволяет пользователям устанавливать размер ставки.
**Процесс**:
  1. Запрашивает ввод ставки.
  2. Проверяет и обновляет ставку в базе данных.

### Функция: `handle_query(call)`
**Назначение**: Обрабатывает взаимодействия с кнопками встроенной клавиатуры для финансовых операций.
**Процесс**:
  1. Определяет, является ли действие пополнением или выводом.
  2. Обрабатывает пополнения и информирует пользователей о недоступности вывода.

### Функция: `process_deposit_amount(message, user_id)`
**Назначение**: Обрабатывает пополнения пользователей.
**Процесс**:
  1. Получает и проверяет сумму пополнения.
  2. Обновляет баланс пользователя в базе данных.

## Структура базы данных

- **Таблица пользователей**:
  - `id`: Первичный ключ.
  - `user_id`: ID пользователя в Телеграме.
  - `username`: Имя пользователя в Телеграме.
  - `balance`: Текущий баланс пользователя.
  - `bet`: Текущая установленная ставка пользователя.

## Информация о символах

- В игре используются различные символы эмодзи с соответствующими вероятностями, необходимыми количествами и множителями выплат.

## Опрос бота

- Бот использует длинный опрос для постоянной проверки новых обновлений.

## Примечание

- Этот бот предназначен для демонстрационных целей и не поддерживает реальные денежные операции.
