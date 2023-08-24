# # from sqlalchemy.orm import Session
# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession

# from app.db.database import async_session_maker
# from app.db.models.dish_model import Dish
# from app.db.models.submenu_model import Submenu


# async def menu_counter(id):
#     print('HAKKOOIEIE')
#     sub_count = 0
#     dish_counter = 0
#     async with async_session_maker() as session:
#         query = select(Submenu).filter(Submenu.menu_id == id)
#         print(query)
#         submenus = session.execute(query)
#         print('SUBMENUS', submenus.all())

#         sub_count = len(submenus.all())
#         for submenu in submenus:
#             dishlen = len(submenu.dishes)
#             dish_counter += dishlen
#         return sub_count, dish_counter


# async def submenu_counter(sub_id):
#     dish_counter = 0
#     async with async_session_maker() as session:
#         dish_counter = session.query(Dish).filter(Dish.submenu_id == sub_id).count()
#     return dish_counter
