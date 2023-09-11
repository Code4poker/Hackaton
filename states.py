from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
    menu = State()
    choosePoll = State()
    addQuestion = State()
    pollPassing = State()
