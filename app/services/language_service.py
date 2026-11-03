from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.language import Language


class LanguageService:
    @staticmethod
    async def list(db: AsyncSession):
        result = await db.execute(
            select(Language)
        )
        return result.scalars().all()

    @staticmethod
    async def language_by_code(code: str, db: AsyncSession) -> Language | None:
        return await db.get(Language, code)

    @staticmethod
    async def create(db: AsyncSession, **fields) -> Language:
        lang = Language(**fields)
        db.add(lang)
        await db.flush()
        return lang
