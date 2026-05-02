from pydantic import BaseModel


class URLCreate(BaseModel):
    original_url: str