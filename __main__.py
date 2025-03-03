import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from handlers import main_router
from config import get_config, BotConfig
from utils import task_scheduler  # Импортируем планировщик

logger = logging.getLogger(__name__)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )
    logger.info('Starting Bot')

    bot_config = get_config(BotConfig, "bot")
    
    if not bot_config.token:
        logger.error("Bot token is missing in the configuration.")
        return
    
    bot = Bot(token=bot_config.token.get_secret_value(),
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.include_routers(main_router)
 
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Webhook deleted, ready for polling.")
    
    # Запускаем планировщик в отдельной задаче
    asyncio.create_task(task_scheduler(bot))
    
    await dp.start_polling(bot)
    return bot

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Error while starting bot: {e}")