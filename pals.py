from pydantic import BaseModel


class Pal(BaseModel):
    parent1: str
    parent2: str
    child: str
