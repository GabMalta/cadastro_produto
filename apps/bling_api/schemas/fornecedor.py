from typing import List, Optional, Union
from pydantic import BaseModel

class Contato(BaseModel):
    id: Optional[int] = None
    nome: Optional[str] = None

class Fornecedor(BaseModel):
    id: Optional[int] = None
    contato: Contato = Contato()
    codigo: Optional[str] = None
    precoCusto: Optional[float] = None
    precoCompra: Optional[float] = None