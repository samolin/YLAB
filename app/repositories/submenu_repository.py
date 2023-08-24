from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import delete, distinct, func, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import async_session_maker
from app.db.models.dish_model import Dish
from app.db.models.submenu_model import Submenu
from app.utils.repository import AbstractRepository


class SubmenuRepository(AbstractRepository):
    model: type[Submenu] = Submenu
    assync_session_maker: AsyncSession

    async def add_new(self, data: dict) -> Submenu:
        async with async_session_maker() as session:
            try:
                query = insert(self.model).values(**data).returning(self.model)
                res = await session.execute(query)
                await session.commit()
                return res.scalar_one()
            except IntegrityError:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'{self.model.__table__} with the same name is already exists',
                )

    async def get_all(self, menu_id: UUID) -> list[Submenu]:
        async with async_session_maker() as session:
            query = select(Submenu,
                           func.count(distinct(Dish.id)).label('dishes_count')
                           ).outerjoin(Dish, Submenu.id == Dish.submenu_id)\
                            .filter(Submenu.menu_id == menu_id).group_by(Submenu.id)
            res = await session.execute(query)
            res = [row[0].to_read_model(row[1]) for row in res.all()]
            if not res:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'{self.model.__table__} not found',
                )
            return res

    async def get_one(self, submenu_id: UUID) -> Submenu:
        async with async_session_maker() as session:
            query = select(Submenu,
                           func.count(distinct(Dish.id)).label('dishes_count')
                           ).outerjoin(Dish, Submenu.id == Dish.submenu_id)\
                            .filter(Submenu.id == submenu_id).group_by(Submenu.id)
            res = await session.execute(query)
            res = res.one_or_none()
            if not res:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'{self.model.__table__} not found',
                )
            res = res[0].to_read_model(res[1])
            return res

    async def patch_one(self, data: dict, submenu_id: UUID) -> Submenu:
        async with async_session_maker() as session:
            query = update(self.model).filter(self.model.id == submenu_id).values(**data).returning(self.model)
            res = await session.execute(query)
            res = res.scalar_one_or_none()
            if not res:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'{self.model.__table__} not found',
                )
            await session.commit()
            return res

    async def del_one(self, submenu_id: UUID) -> int:
        async with async_session_maker() as session:
            query = delete(self.model).filter(self.model.id == submenu_id).returning(self.model)
            res = await session.execute(query)
            if not res.first():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'{self.model.__table__} not found',
                )
            await session.commit()
            return 1
