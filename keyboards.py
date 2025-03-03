from typing import List, Dict
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime, timedelta

def get_schedule_type_keyboard() -> InlineKeyboardBuilder:
    """Инлайн-клавиатура для выбора типа отправки."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Сразу", callback_data="schedule_immediate"),
        InlineKeyboardButton(text="С отсрочкой", callback_data="schedule_delayed"),
        InlineKeyboardButton(text="Ежедневно", callback_data="schedule_daily")
    )
    return builder.as_markup()

def get_channel_keyboard(channels: List[Dict]) -> InlineKeyboardBuilder:
    """Инлайн-клавиатура для выбора канала."""
    builder = InlineKeyboardBuilder()
    for channel in channels:
        builder.row(InlineKeyboardButton(text=channel.url, callback_data=f"channel_{channel.id}"))
    return builder.as_markup()

def get_task_management_keyboard(tasks: List[Dict]) -> InlineKeyboardBuilder:
    """Инлайн-клавиатура для редактирования/удаления задач."""
    builder = InlineKeyboardBuilder()
    for task in tasks:
        button_text = f"Задача {task['id']}: {task['message'][:20]}..."
        builder.row(InlineKeyboardButton(text=button_text, callback_data=f"task_{task['id']}"))
    return builder.as_markup()

def get_task_action_keyboard(task_id: int) -> InlineKeyboardBuilder:
    """Инлайн-клавиатура для выбора действия с задачей (редактировать/удалить)."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Редактировать", callback_data=f"edit_{task_id}"),
        InlineKeyboardButton(text="Удалить", callback_data=f"delete_{task_id}")
    )
    return builder.as_markup()

def get_date_keyboard(selected_date: datetime = None) -> InlineKeyboardBuilder:
    """Инлайн-клавиатура для выбора даты."""
    builder = InlineKeyboardBuilder()
    current_date = selected_date or datetime.now()

    # Кнопки для изменения дня
    builder.row(
        InlineKeyboardButton(text="⬅️ День", callback_data=f"date_prev_day_{current_date.strftime('%Y-%m-%d')}"),
        InlineKeyboardButton(text=current_date.strftime("%Y-%m-%d"), callback_data="date_noop"),
        InlineKeyboardButton(text="День ➡️", callback_data=f"date_next_day_{current_date.strftime('%Y-%m-%d')}")
    )

    # Кнопка подтверждения
    builder.row(InlineKeyboardButton(text="Подтвердить дату", callback_data=f"confirm_date_{current_date.strftime('%Y-%m-%d')}"))
    return builder.as_markup()

def get_time_keyboard(selected_time: datetime = None) -> InlineKeyboardBuilder:
    """Инлайн-клавиатура для выбора времени."""
    builder = InlineKeyboardBuilder()
    current_time = selected_time or datetime.now().replace(hour=0, minute=0, second=0)

    # Кнопки для изменения часов и минут
    builder.row(
        InlineKeyboardButton(text="⬅️ Час", callback_data=f"time_prev_hour_{current_time.strftime('%H:%M')}"),
        InlineKeyboardButton(text=current_time.strftime("%H:%M"), callback_data="time_noop"),
        InlineKeyboardButton(text="Час ➡️", callback_data=f"time_next_hour_{current_time.strftime('%H:%M')}")
    )
    builder.row(
        InlineKeyboardButton(text="⬅️ Мин", callback_data=f"time_prev_min_{current_time.strftime('%H:%M')}"),
        InlineKeyboardButton(text="Подтвердить время", callback_data=f"confirm_time_{current_time.strftime('%H:%M')}"),
        InlineKeyboardButton(text="Мин ➡️", callback_data=f"time_next_min_{current_time.strftime('%H:%M')}")
    )
    return builder.as_markup()

def get_edit_action_keyboard(task_id: int) -> InlineKeyboardBuilder:
    """Инлайн-клавиатура для выбора, что редактировать: текст или время."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Редактировать текст", callback_data=f"edit_message_{task_id}"),
        InlineKeyboardButton(text="Редактировать время", callback_data=f"edit_time_{task_id}")
    )
    return builder.as_markup()

def get_start_keyboard() -> InlineKeyboardBuilder:
    """Инлайн-клавиатура для стартового сообщения."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Создать задачу", callback_data="start_create"),
        InlineKeyboardButton(text="Управление задачами", callback_data="start_manage")
    )
    return builder.as_markup()

def back_keyboard() -> InlineKeyboardBuilder:

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Назад", callback_data="back"),
    )
    return builder.as_markup()