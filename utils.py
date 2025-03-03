import json
import os
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Optional

TASKS_FILE = "tasks.json"

def load_tasks() -> List[Dict]:
    """Загружаем задачи из JSON."""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_tasks(tasks: List[Dict]):
    """Сохраняем задачи в JSON."""
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)

def add_task(message: str, channel_id: str, schedule_type: str, schedule_time: Optional[str] = None) -> int:
    """Добавляем новую задачу и возвращаем её ID."""
    tasks = load_tasks()
    task_id = len(tasks) + 1
    new_task = {
        "id": task_id,
        "message": message,
        "channel_id": channel_id,
        "schedule_type": schedule_type,  # "immediate", "delayed", "daily"
        "schedule_time": schedule_time,  # В формате "YYYY-MM-DD HH:MM:SS" или None для immediate
        "status": "pending"
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return task_id

def edit_task(task_id: int, new_message: Optional[str] = None, new_schedule_time: Optional[str] = None):
    """Редактируем задачу по ID."""
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            if new_message:
                task["message"] = new_message
            if new_schedule_time:
                task["schedule_time"] = new_schedule_time
            break
    save_tasks(tasks)

def delete_task(task_id: int):
    """Удаляем задачу по ID."""
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)

async def task_scheduler(bot):
    """Планировщик: проверяет задачи и отправляет сообщения."""
    while True:
        tasks = load_tasks()
        current_time = datetime.now()
        
        for task in tasks:
            if task["status"] != "pending":
                continue
                
            schedule_time = task["schedule_time"]
            schedule_type = task["schedule_type"]
            
            if schedule_type == "immediate":
                await bot.send_message(chat_id=task["channel_id"], text=task["message"])
                task["status"] = "done"
            
            elif schedule_type == "delayed" and schedule_time:
                scheduled = datetime.strptime(schedule_time, "%Y-%m-%d %H:%M:%S")
                if current_time >= scheduled:
                    await bot.send_message(chat_id=task["channel_id"], text=task["message"])
                    task["status"] = "done"
            
            elif schedule_type == "daily" and schedule_time:
                scheduled = datetime.strptime(schedule_time, "%Y-%m-%d %H:%M:%S")
                current_time_only = current_time.time()
                scheduled_time_only = scheduled.time()
                if (current_time_only.hour > scheduled_time_only.hour or 
                    (current_time_only.hour == scheduled_time_only.hour and 
                     current_time_only.minute >= scheduled_time_only.minute)):
                    await bot.send_message(chat_id=task["channel_id"], text=task["message"])
                    # Для "daily" статус не меняем, чтобы повторялось каждый день

        save_tasks(tasks)  # Обновляем статусы
        await asyncio.sleep(60)  # Проверяем каждую минуту