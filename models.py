from pydantic import BaseModel

from dataclasses import dataclass

@dataclass
class CaseContext:
    case_id: str

class DispatchResult(BaseModel):
    category: str
    message: str