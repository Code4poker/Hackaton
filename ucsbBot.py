import sql_func
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from states import States, FSMContext

storage = MemoryStorage()

bot = Bot(token='5420713508:AAECm98duPRvaA8aRDRgBZJoQy7019UWXTg', parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
pollsDataPath = "pollsData.txt"


async def on_startup(_):
    print('Бот запущен')


@dp.message_handler(commands='start', state='*')
async def start(message: types.Message):
    keyboard = create_buttons(['Начать'])

    await States.menu.set()
    await bot.send_message(message.chat.id, '<b>Добро пожаловать в UCSB Quiz Bot!</b>', reply_markup=keyboard)


@dp.message_handler(state=States.menu)
async def menu(message: types.Message, state: FSMContext):
    keyboard = create_buttons(['Пройти опрос', 'Создать опрос'], 1)

    await States.choosePoll.set()
    await bot.send_message(message.chat.id, 'Что вы хотите сделать?\n<b>(При создании нового опроса предыдущий'
                                            ' автоматически удаляется)</b>', reply_markup=keyboard)


@dp.message_handler(state=States.choosePoll)
async def choosePoll(message: types.Message, state: FSMContext):
    if message.text.lower() == 'пройти опрос':
        await state.update_data(n=0)
        await States.pollPassing.set()
        await poll_passing(message, state)
    elif message.text.lower() == 'создать опрос':
        f = open(pollsDataPath, 'w').close()
        
        await States.addQuestion.set()
        await bot.send_message(message.chat.id, 'Введите вопрос и варианты ответа на него через слеш\n(вопрос / ответ 1 / ... / ответ N)')
    elif message.text.lower() == 'завершить создание опроса':
        await menu(message, state)


@dp.message_handler(state=States.addQuestion)
async def addQuestion(message: types.Message, state: FSMContext):
    if message.text.lower() == 'завершить создание опроса':
        await choosePoll(message, state)
    else:
        f = open(pollsDataPath, 'a', encoding='utf-8')
        f.write(message.text + '\n')

        keyboard = create_buttons(['Завершить создание опроса'])
        
        await bot.send_message(message.chat.id, 'Вы можете ввести следующий вопрос, либо завершить создание опроса', reply_markup=keyboard)


@dp.message_handler(state=States.pollPassing)
async def poll_passing(message: types.Message, state: FSMContext):
    questions = get_questions()
    data = await state.get_data()
    n = data.get('n')
    if message.text.lower() != 'пройти опрос':
        sql_func.add(message.from_user.id, message.from_user.full_name, message.text.strip(), questions[n-1][0].strip())

    if n != len(questions):
        mess = questions[n].pop(0)
        keyboard = create_buttons(questions[n], 2)

        n += 1
        await state.update_data(n=n)

        await bot.send_message(message.chat.id, mess, reply_markup=keyboard)
    else:
        await bot.send_message(message.chat.id, 'Опрос завершен, спасибо!')
        await menu(message, state)


def get_questions():
    questions = []
    f = open(pollsDataPath, encoding='utf-8')
    for row in f:
        questions.append(row.replace('\n', '').split('/'))

    return questions


def create_buttons(btns, width=1):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=width)
    keyboard.add(*btns)

    return keyboard


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
