from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.language_controller import LanguageController
from app.dependencies.db import get_db
from app.schemas.language import LanguageCreate, LanguageOut
from app.schemas.response import Envelope, ok

router = APIRouter(prefix="/language", tags=["Language"])


@router.get("/", response_model=Envelope[list[LanguageOut]], status_code=200)
async def languages(db: AsyncSession = Depends(get_db)):
    all_languages = await LanguageController.get_all_language(db)
    return ok(all_languages, message="Language fetched successfully")


@router.post("/", response_model=Envelope[LanguageOut], status_code=201)
async def create_language(
    data: LanguageCreate,
    db: AsyncSession = Depends(get_db),
):
    language = await LanguageController.create(data, db)
    return ok(language, message="Language created successfully")
