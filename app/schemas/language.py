from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

Capability = Literal["stt", "translation", "tts"]

class LanguageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    code: str
    name: str
    native_name: str
    stt_supported: bool
    translation_supported: bool
    tts_supported: bool
    is_active: bool

class LanguageCreate(BaseModel):
    code: str = Field(pattern=r"^[a-z]{2,3}(-[A-Za-z0-9]{2,8})?$")
    name: str = Field(min_length=1, max_length=80)
    native_name: str = Field(min_length=1, max_length=80)
    stt_supported: bool = False
    translation_supported: bool = False
    tts_supported: bool = False

class LanguageUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=80)
    native_name: str | None = Field(default=None, min_length=1, max_length=80)
    stt_supported: bool | None = None
    translation_supported: bool | None = None
    tts_supported: bool | None = None
    is_active: bool | None = None