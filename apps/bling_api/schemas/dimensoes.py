from typing import Union, Optional
from pydantic import BaseModel

class Dimensoes(BaseModel):
    largura: Union[int, float, str] = 0
    altura: Union[int, float, str] = 0
    profundidade: Union[int, float, str] = 0
    unidadeMedida: Optional[int] = 1