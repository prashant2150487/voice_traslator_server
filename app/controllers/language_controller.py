from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.language import LanguageCreate
from app.services.language_service import LanguageService


class LanguageController:

    @staticmethod
    async def get_all_language(db: AsyncSession):
        languages = await LanguageService.list(db)
        if languages is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Languages not found")
        return languages

    @staticmethod
    async def create(data: LanguageCreate, db: AsyncSession):
        lang = await LanguageService.language_by_code(data.code, db)
        if lang:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Language code already exists",
            )
        try:
            lang = await LanguageService.create(db, **data.model_dump())
            await db.commit()
            await db.refresh(lang)
            return lang

        except IntegrityError as exc:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Language code already exists",
            ) from exc
