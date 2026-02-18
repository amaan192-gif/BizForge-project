from pydantic import BaseModel
from typing import List, Optional

class BrandRequest(BaseModel):
    idea: str

class BrandResponse(BaseModel):
    names: List[str]
    tagline: str
    visual_vibe: str
    logo_prompt: str

class LogoRequest(BaseModel):
    prompt: str

class LogoResponse(BaseModel):
    logo_url: str

class ContentRequest(BaseModel):
    brand_description: str
    tone: str
    content_type: str

class DesignSystemResponse(BaseModel):
    primary_color: str
    secondary_color: str
    accent_color: str
    font_pairing: str
