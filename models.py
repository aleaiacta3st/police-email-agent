from pydantic import BaseModel

class DispatchResult(BaseModel):
    category: str
    message: str