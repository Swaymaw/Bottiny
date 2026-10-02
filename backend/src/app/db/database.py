from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.app.db.tables import Base


class Database:
    def __init__(self, url: str, **engine_kwargs):
        self.engine = create_async_engine(url, **engine_kwargs)
        self.session_factory = async_sessionmaker(self.engine, expire_on_commit=False)

    async def init(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def close(self) -> None:
        await self.engine.dispose()

    async def get(self, model, *where):
        async with self.session_factory() as s:
            result = await s.execute(select(model).where(*where))
            return result.scalars().first()

    async def get_all(self, model, *where) -> list:
        async with self.session_factory() as s:
            result = await s.execute(select(model).where(*where))
            return list(result.scalars())

    async def add(self, obj):
        async with self.session_factory() as s:
            s.add(obj)
            await s.commit()
            return obj

    async def add_many(self, objs: list) -> list:
        async with self.session_factory() as s:
            s.add_all(objs)
            await s.commit()
            return objs

    async def update(self, model, *where, **values) -> int:
        async with self.session_factory() as s:
            result = await s.execute(update(model).where(*where).values(**values))
            await s.commit()
            return result.rowcount
