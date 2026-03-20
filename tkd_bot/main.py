from aiogram import Bot, Dispatcher
from config import TOKEN
import logging
import asyncio
from routers.start import router as start_router
from routers.admin import router as admin_router
from routers.admin_del_db import router as delete_db
from handlers_fsm.callbacks import router as callbacks_router
from data_base.models import create_tables, create_table_reservation, middle_bd


bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(admin_router)
dp.include_router(delete_db)
dp.include_router(start_router)
dp.include_router(callbacks_router)



async def main():
    create_tables()
    create_table_reservation()

    
   
 
    await dp.start_polling(bot)

    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
