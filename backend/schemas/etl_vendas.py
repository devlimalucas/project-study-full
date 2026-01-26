from pydantic import BaseModel

class ExportResponse(BaseModel):
    filename: str
    content: str
