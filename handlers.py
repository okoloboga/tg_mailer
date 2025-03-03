from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from datetime import datetime, timedelta

from config import get_config, Channel, Admin
from utils import add_task, edit_task, delete_task, load_tasks
from keyboards import (
    get_schedule_type_keyboard,
    get_channel_keyboard,
    get_task_management_keyboard,
    get_task_action_keyboard,
    get_date_keyboard,
    get_time_keyboard,
    get_edit_action_keyboard,
    get_start_keyboard,
    back_keyboard
)

main_router = Router()

# Определяем состояния для создания и редактирования задачи
class CreateTask(StatesGroup):
    message = State()
    schedule_type = State()
    schedule_date = State()
    schedule_time = State()
    channel = State()
    edit_action = State()  # Новое состояние для выбора, что редактировать
    edit_message = State()  # Для редактирования текста
    edit_date = State()  # Для редактирования даты
    edit_time = State()  # Для редактирования времени

# Проверка, что пользователь — админ, и стартовое сообщение
@main_router.message(Command("start"))
async def cmd_start(message: Message):
    admin_config = get_config(Admin, "admin")
    if str(message.from_user.id) != admin_config.id:
        await message.answer("Вы не администратор!")
        return
    await message.answer(
        "Привет! Я бот для управления каналами. Что хочешь сделать?",
        reply_markup=get_start_keyboard()
    )

# Проверка, что пользователь — админ, и стартовое сообщение
@main_router.callback_query(F.data == 'back')
async def cmd_start(callback: CallbackQuery):
    admin_config = get_config(Admin, "admin")
    if str(callback.from_user.id) != admin_config.id:
        await callback.message.edit_text("Вы не администратор!")
        return
    await callback.message.edit_text(
        "Привет! Я бот для управления каналами. Что хочешь сделать?",
        reply_markup=get_start_keyboard()
    )

# Обработка кнопок стартового меню
@main_router.callback_query(F.data.in_(["start_create", "start_manage"]))
async def process_start_action(callback: CallbackQuery, state: FSMContext):
    action = callback.data
    admin_config = get_config(Admin, "admin")
    if str(callback.from_user.id) != admin_config.id:
        await callback.message.edit_text("Вы не администратор!")
        await callback.answer()
        return

    if action == "start_create":
        await callback.message.edit_text("Введите текст сообщения:", reply_markup=back_keyboard())
        await state.set_state(CreateTask.message)
    elif action == "start_manage":
        tasks = load_tasks()
        if not tasks:
            await callback.message.edit_text("Нет активных задач!", reply_markup=back_keyboard())
        else:
            await callback.message.edit_text("Выберите задачу для управления:", reply_markup=get_task_management_keyboard(tasks))
    
    await callback.answer()

@main_router.message(CreateTask.message)
async def process_message(message: Message, state: FSMContext):
    await state.update_data(message=message.text)
    await message.answer("Выберите тип отправки:", reply_markup=get_schedule_type_keyboard())
    await state.set_state(CreateTask.schedule_type)

@main_router.callback_query(CreateTask.schedule_type, F.data.startswith("schedule_"))
async def process_schedule_type(callback: CallbackQuery, state: FSMContext):
    schedule_type = callback.data.split("_")[1]  # "immediate", "delayed", "daily"
    await state.update_data(schedule_type=schedule_type)
    
    if schedule_type == "immediate":
        await state.update_data(schedule_time=None)
        channels = get_config(list[Channel], "channels")
        await callback.message.edit_text("Выберите канал:", reply_markup=get_channel_keyboard(channels))
        await state.set_state(CreateTask.channel)
    else:
        await callback.message.edit_text("Выберите дату:", reply_markup=get_date_keyboard())
        await state.set_state(CreateTask.schedule_date)
    await callback.answer()

# Обработка выбора даты
@main_router.callback_query(CreateTask.schedule_date, F.data.startswith("date_"))
async def process_date_selection(callback: CallbackQuery, state: FSMContext):
    action = callback.data
    if action.startswith("date_prev_day_"):
        current_date_str = action.split("_")[-1]
        current_date = datetime.strptime(current_date_str, "%Y-%m-%d")
        new_date = current_date - timedelta(days=1)
        await callback.message.edit_text("Выберите дату:", reply_markup=get_date_keyboard(new_date))
    
    elif action.startswith("date_next_day_"):
        current_date_str = action.split("_")[-1]
        current_date = datetime.strptime(current_date_str, "%Y-%m-%d")
        new_date = current_date + timedelta(days=1)
        await callback.message.edit_text("Выберите дату:", reply_markup=get_date_keyboard(new_date))
    
    elif action.startswith("confirm_date_"):
        selected_date_str = action.split("_")[-1]
        await state.update_data(schedule_date=selected_date_str)
        await callback.message.edit_text("Выберите время:", reply_markup=get_time_keyboard())
        await state.set_state(CreateTask.schedule_time)
    
    await callback.answer()

# Обработка выбора времени
@main_router.callback_query(CreateTask.schedule_time, F.data.startswith("time_"))
async def process_time_selection(callback: CallbackQuery, state: FSMContext):
    action = callback.data
    if action.startswith("time_prev_hour_"):
        current_time_str = action.split("_")[-1]
        current_time = datetime.strptime(current_time_str, "%H:%M")
        new_time = current_time - timedelta(hours=1)
        await callback.message.edit_text("Выберите время:", reply_markup=get_time_keyboard(new_time))
    
    elif action.startswith("time_next_hour_"):
        current_time_str = action.split("_")[-1]
        current_time = datetime.strptime(current_time_str, "%H:%M")
        new_time = current_time + timedelta(hours=1)
        await callback.message.edit_text("Выберите время:", reply_markup=get_time_keyboard(new_time))
    
    elif action.startswith("time_prev_min_"):
        current_time_str = action.split("_")[-1]
        current_time = datetime.strptime(current_time_str, "%H:%M")
        new_time = current_time - timedelta(minutes=5)  # Шаг 5 минут
        await callback.message.edit_text("Выберите время:", reply_markup=get_time_keyboard(new_time))
    
    elif action.startswith("time_next_min_"):
        current_time_str = action.split("_")[-1]
        current_time = datetime.strptime(current_time_str, "%H:%M")
        new_time = current_time + timedelta(minutes=5)  # Шаг 5 минут
        await callback.message.edit_text("Выберите время:", reply_markup=get_time_keyboard(new_time))
    
    elif action.startswith("confirm_time_"):
        selected_time_str = action.split("_")[-1]
        data = await state.get_data()
        selected_date = data["schedule_date"]
        full_datetime = f"{selected_date} {selected_time_str}:00"  # Добавляем секунды
        await state.update_data(schedule_time=full_datetime)
        channels = get_config(list[Channel], "channels")
        await callback.message.edit_text("Выберите канал:", reply_markup=get_channel_keyboard(channels))
        await state.set_state(CreateTask.channel)
    
    await callback.answer()

# Обработка выбора канала
@main_router.callback_query(CreateTask.channel, F.data.startswith("channel_"))
async def process_channel(callback: CallbackQuery, state: FSMContext):
    channel_id = callback.data.split("_")[1]
    channels = get_config(list[Channel], "channels")
    selected_channel = next((ch for ch in channels if ch.id == channel_id), None)
    
    if not selected_channel:
        await callback.message.edit_text("Канал не найден! Попробуйте снова:", reply_markup=get_channel_keyboard(channels))
        await callback.answer()
        return

    data = await state.get_data()
    task_id = add_task(
        message=data["message"],
        channel_id=selected_channel.id,
        schedule_type=data["schedule_type"],
        schedule_time=data["schedule_time"]
    )
    await callback.message.edit_text(f"Задача #{task_id} создана!", reply_markup=back_keyboard())
    await state.clear()
    await callback.answer()


@main_router.callback_query(F.data.startswith("task_"))
async def process_task_selection(callback: CallbackQuery):
    task_id = int(callback.data.split("_")[1])
    await callback.message.edit_text("Выберите действие:", reply_markup=get_task_action_keyboard(task_id))
    await callback.answer()

@main_router.callback_query(F.data.startswith("delete_"))
async def process_delete_task(callback: CallbackQuery):
    task_id = int(callback.data.split("_")[1])
    delete_task(task_id)
    await callback.message.edit_text(f"Задача #{task_id} удалена!", reply_markup=back_keyboard())
    await callback.answer()

# Обработка редактирования — выбор, что редактировать
@main_router.callback_query(F.data.startswith("edit_"))
async def process_edit_task(callback: CallbackQuery, state: FSMContext):
    task_id = int(callback.data.split("_")[1])
    await state.update_data(task_id=task_id)
    await callback.message.edit_text("Что хотите редактировать?", reply_markup=get_edit_action_keyboard(task_id))
    await state.set_state(CreateTask.edit_action)
    await callback.answer()

# Обработка выбора действия редактирования
@main_router.callback_query(CreateTask.edit_action, F.data.startswith("edit_"))
async def process_edit_action(callback: CallbackQuery, state: FSMContext):
    action = callback.data
    data = await state.get_data()
    task_id = data["task_id"]
    
    if action.startswith("edit_message_"):
        await callback.message.edit_text("Введите новый текст сообщения (или /skip, чтобы оставить без изменений):", reply_markup=back_keyboard())
        await state.set_state(CreateTask.edit_message)
    
    elif action.startswith("edit_time_"):
        tasks = load_tasks()
        task = next((t for t in tasks if t["id"] == task_id), None)
        if task and task["schedule_type"] == "immediate":
            await callback.message.edit_text("Эта задача отправляется сразу, редактирование времени невозможно!")
            await state.clear()
        else:
            # Если время уже задано, используем его как начальное значение
            selected_date = datetime.now()
            if task and task["schedule_time"]:
                selected_date = datetime.strptime(task["schedule_time"], "%Y-%m-%d %H:%M:%S")
            await callback.message.edit_text("Выберите новую дату:", reply_markup=get_date_keyboard(selected_date))
            await state.set_state(CreateTask.edit_date)
    
    await callback.answer()

# Обработка редактирования текста
@main_router.message(CreateTask.edit_message)
async def process_edit_message(message: Message, state: FSMContext):
    data = await state.get_data()
    task_id = data["task_id"]
    new_message = message.text
    if new_message != "/skip":
        edit_task(task_id, new_message=new_message)
        await message.answer(f"Текст задачи #{task_id} обновлён!")
    else:
        await message.answer("Текст оставлен без изменений.")
    await state.clear()

# Обработка редактирования даты
@main_router.callback_query(CreateTask.edit_date, F.data.startswith("date_"))
async def process_edit_date_selection(callback: CallbackQuery, state: FSMContext):
    action = callback.data
    if action.startswith("date_prev_day_"):
        current_date_str = action.split("_")[-1]
        current_date = datetime.strptime(current_date_str, "%Y-%m-%d")
        new_date = current_date - timedelta(days=1)
        await callback.message.edit_text("Выберите дату:", reply_markup=get_date_keyboard(new_date))
    
    elif action.startswith("date_next_day_"):
        current_date_str = action.split("_")[-1]
        current_date = datetime.strptime(current_date_str, "%Y-%m-%d")
        new_date = current_date + timedelta(days=1)
        await callback.message.edit_text("Выберите дату:", reply_markup=get_date_keyboard(new_date))
    
    elif action.startswith("confirm_date_"):
        selected_date_str = action.split("_")[-1]
        await state.update_data(edit_date=selected_date_str)
        # Используем текущее время задачи или текущее, если его нет
        data = await state.get_data()
        task_id = data["task_id"]
        tasks = load_tasks()
        task = next((t for t in tasks if t["id"] == task_id), None)
        selected_time = datetime.now().replace(hour=0, minute=0, second=0)
        if task and task["schedule_time"]:
            selected_time = datetime.strptime(task["schedule_time"], "%Y-%m-%d %H:%M:%S")
        await callback.message.edit_text("Выберите новое время:", reply_markup=get_time_keyboard(selected_time))
        await state.set_state(CreateTask.edit_time)
    
    await callback.answer()

# Обработка редактирования времени
@main_router.callback_query(CreateTask.edit_time, F.data.startswith("time_"))
async def process_edit_time_selection(callback: CallbackQuery, state: FSMContext):
    action = callback.data
    if action.startswith("time_prev_hour_"):
        current_time_str = action.split("_")[-1]
        current_time = datetime.strptime(current_time_str, "%H:%M")
        new_time = current_time - timedelta(hours=1)
        await callback.message.edit_text("Выберите время:", reply_markup=get_time_keyboard(new_time))
    
    elif action.startswith("time_next_hour_"):
        current_time_str = action.split("_")[-1]
        current_time = datetime.strptime(current_time_str, "%H:%M")
        new_time = current_time + timedelta(hours=1)
        await callback.message.edit_text("Выберите время:", reply_markup=get_time_keyboard(new_time))
    
    elif action.startswith("time_prev_min_"):
        current_time_str = action.split("_")[-1]
        current_time = datetime.strptime(current_time_str, "%H:%M")
        new_time = current_time - timedelta(minutes=5)  # Шаг 5 минут
        await callback.message.edit_text("Выберите время:", reply_markup=get_time_keyboard(new_time))
    
    elif action.startswith("time_next_min_"):
        current_time_str = action.split("_")[-1]
        current_time = datetime.strptime(current_time_str, "%H:%M")
        new_time = current_time + timedelta(minutes=5)  # Шаг 5 минут
        await callback.message.edit_text("Выберите время:", reply_markup=get_time_keyboard(new_time))
    
    elif action.startswith("confirm_time_"):
        selected_time_str = action.split("_")[-1]
        data = await state.get_data()
        selected_date = data["edit_date"]
        task_id = data["task_id"]
        full_datetime = f"{selected_date} {selected_time_str}:00"
        edit_task(task_id, new_schedule_time=full_datetime)
        await callback.message.edit_text(f"Время задачи #{task_id} обновлено!")
        await state.clear()
    
    await callback.answer()