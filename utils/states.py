from aiogram.fsm.state import State, StatesGroup

class AccountSubmission(StatesGroup):
    waiting_for_phone = State()
    waiting_for_otp = State()

class WithdrawRequest(StatesGroup):
    waiting_for_bank_info = State()
