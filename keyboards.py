from typing import List, Dict
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta

def get_schedule_type_keyboard() -> InlineKeyboardMarkup:
    """Инлайн-клавиатура для выбора типа отправки."""
    kb = InlineKeyboardMarkup()
    kb.row(
        InlineKeyboardButton("Сразу", callback_data="schedule_immediate"),
        InlineKeyboardButton("С отсрочкой", callback_data="schedule_delayed"),
        InlineKeyboardButton("Ежедневно", callback_data="schedule_daily")
    )
    return kb

def get_channel_keyboard(channels: List[Dict]) -> InlineKeyboardMarkup:
    """Инлайн-клавиатура для выбора канала."""
    kb = InlineKeyboardMarkup()
    for channel in channels:
        kb.add(InlineKeyboardButton(channel.url, callback_data=f"channel_{channel.id}"))
    return kb

def get_task_management_keyboard(tasks: List[Dict]) -> InlineKeyboardMarkup:
    """Инлайн-клавиатура для редактирования/удаления задач."""
    kb = InlineKeyboardMarkup()
    for task in tasks:
        button_text = f"Задача {task['id']}: {task['message'][:20]}..."
        kb.add(InlineKeyboardButton(button_text, callback_data=f"task_{task['id']}"))
    return kb

def get_task_action_keyboard(task_id: int) -> InlineKeyboardMarkup:
    """Инлайн-клавиатура для выбора действия с задачей (редактировать/удалить)."""
    kb = InlineKeyboardMarkup()
    kb.row(
        InlineKeyboardButton("Редактировать", callback_data=f"edit_{task_id}"),
        InlineKeyboardButton("Удалить", callback_data=f"delete_{task_id}")
    )
    return kb

# Новые клавиатуры для выбора даты и времени
def get_date_keyboard(selected_date: datetime = None) -> InlineKeyboardMarkup:
    """Инлайн-клавиатура для выбора даты."""
    kb = InlineKeyboardMarkup()
    current_date = selected_date or datetime.now()

    # Кнопки для изменения дня
    kb.row(
        InlineKeyboardButton("⬅️ День", callback_data=f"date_prev_day_{current_date.strftime('%Y-%m-%d')}"),
        InlineKeyboardButton(current_date.strftime("%Y-%m-%d"), callback_data="date_noop"),
        InlineKeyboardButton("День ➡️", callback_data=f"date_next_day_{current_date.strftime('%Y-%m-%d')}")
    )

    # Кнопка подтверждения
    kb.add(InlineKeyboardButton("Подтвердить дату", callback_data=f"confirm_date_{current_date.strftime('%Y-%m-%d')}"))
    return kb

def get_time_keyboard(selected_time: datetime = None) -> InlineKeyboardMarkup:
    """Инлайн-клавиатура для выбора времени."""
    kb = InlineKeyboardMarkup()
    current_time = selected_time or datetime.now().replace(hour=0, minute=0, second=0)

    # Кнопки для изменения часов и минут
    kb.row(
        InlineKeyboardButton("⬅️ Час", callback_data=f"time_prev_hour_{current_time.strftime('%H:%M')}"),
        InlineKeyboardButton(current_time.strftime("%H:%M"), callback_data="time_noop"),
        InlineKeyboardButton("Час ➡️", callback_data=f"time_next_hour_{current_time.strftime('%H:%M')}")
    )
    kb.row(
        InlineKeyboardButton("⬅️ Мин", callback_data=f"time_prev_min_{current_time.strftime('%H:%M')}"),
        InlineKeyboardButton("Подтвердить время", callback_data=f"confirm_time_{current_time.strftime('%H:%M')}"),
        InlineKeyboardButton("Мин ➡️", callback_data=f"time_next_min_{current_time.strftime('%H:%M')}")
    )
    return kb

def get_edit_action_keyboard(task_id: int) -> InlineKeyboardMarkup:
    """Инлайн-клавиатура для выбора, что редактировать: текст или время."""
    kb = InlineKeyboardMarkup()
    kb.row(
        InlineKeyboardButton("Редактировать текст", callback_data=f"edit_message_{task_id}"),
        InlineKeyboardButton("Редактировать время", callback_data=f"edit_time_{task_id}")
    )
    return kb

# Новая функция для стартовой клавиатуры
def get_start_keyboard() -> InlineKeyboardMarkup:
    """Инлайн-клавиатура для стартового сообщения."""
    kb = InlineKeyboardMarkup()
    kb.row(
        InlineKeyboardButton("Создать задачу", callback_data="start_create"),
        InlineKeyboardButton("Управление задачами", callback_data="start_manage")
    )
    return kb