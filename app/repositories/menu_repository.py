from uuid import UUID

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy import delete, distinct, func, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.database import async_session_maker
from app.db.models.dish_model import Dish
from app.db.models.menu_model import Menu
from app.db.models.submenu_model import Submenu
from app.schemas.menu_schemas import MenuEverything
from app.utils.repository import AbstractRepository


class MenuRepository(AbstractRepository):
    model: type[Menu] = Menu
    assync_session_maker: AsyncSession

    async def add_new(self, data: dict) -> Menu:
        async with async_session_maker() as session:
            try:
                query = insert(self.model).values(**data).returning(self.model)
                result = await session.execute(query)
                await session.commit()
                return result.scalar_one()
            except IntegrityError:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'{self.model.__table__} with the same name is already exists',
                )

    async def get_all(self) -> list[Menu]:
        async with async_session_maker() as session:
            query = select(Menu,
                           func.count(distinct(Submenu.id)).label('submenus_count'),
                           func.count(distinct(Dish.id)).label('dishes_count'))\
                .outerjoin(Submenu, Menu.id == Submenu.menu_id)\
                .outerjoin(Dish, Submenu.id == Dish.submenu_id)\
                .group_by(Menu.id)
            result = await session.execute(query)
            result = [row[0].to_read_model(row[1], row[2]) for row in result.all()]
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'{self.model.__table__} not found',
                )
            return result

    async def get_one(self, id: UUID) -> Menu:
        async with async_session_maker() as session:
            query = select(Menu,
                           func.count(distinct(Submenu.id)).label('submenus_count'),
                           func.count(distinct(Dish.id)).label('dishes_count'),
                           ).outerjoin(Submenu, Menu.id == Submenu.menu_id)\
                            .outerjoin(Dish, Submenu.id == Dish.submenu_id)\
                            .filter(Menu.id == id).group_by(Menu.id)
            result = await session.execute(query)
            result = result.one_or_none()
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'{self.model.__table__} not found',
                )
            result = result[0].to_read_model(result[1], result[2])
            return result

    async def patch_one(self, id: UUID, data: dict) -> Menu:
        async with async_session_maker() as session:
            query = update(self.model).filter(self.model.id == id).values(**data).returning(self.model)
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'{self.model.__table__} not found',
                )
            await session.commit()
            return result

    async def del_one(self, id: UUID) -> int:
        async with async_session_maker() as session:
            query = delete(self.model).filter(self.model.id == id).returning(self.model)
            result = await session.execute(query)
            if not result.first():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'{self.model.__table__} not found',
                )
            await session.commit()
            return 1

    async def get_everything(self):
        async with async_session_maker() as session:
            query = select(Menu)\
                .options(selectinload(Menu.submenus).options(selectinload(Submenu.dishes)))\
                .group_by(Menu.id)
            result = await session.execute(query)
            result = result.scalars().all()
            result = jsonable_encoder(result)
            result = [MenuEverything.model_validate(i) for i in result]
            if result:
                return result
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'{self.model.__table__} not found',
            )
