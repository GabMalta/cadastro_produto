from typing import Optional, Union
from pydantic import BaseModel

class Estoque(BaseModel):
    minimo: Optional[str] = None
    maximo: Optional[str] = None
    crossDocking: Optional[str] = None
    localizacao: Optional[str] = None

class EstoqueVar(BaseModel):
    minimo: Union[int, float] = 0
    maximo: Union[int, float] = 0
    crossdocking: Union[int, float] = 0
    localizacao: Optional[str] = None
    saldoVirtualTotal: Union[int, float] = 0