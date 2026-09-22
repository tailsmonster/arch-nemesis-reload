from pydantic import BaseModel


class NemesisResponse(BaseModel):
    content: str
