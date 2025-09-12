from typing import Optional, List, Union
from pydantic import BaseModel, field_validator


class FornecedorLoja(BaseModel):
    id: int


class MarcaLoja(BaseModel):
    id: int


class CategoriaProduto(BaseModel):
    id: int


class ProdutoLojaSchema(BaseModel):
    preco: float
    precoPromocional: float
    idProduto: int
    idLoja: Union[int, str]

    codigo: Optional[str] = None
    idProdutoLoja: Optional[str] = " "
    fornecedorLoja: Optional[FornecedorLoja] = None
    marcaLoja: Optional[MarcaLoja] = None
    categoriasProdutos: Optional[List[CategoriaProduto]] = None

    @field_validator('idProdutoLoja')
    @classmethod
    def validar_id_produto_loja(cls, v):
        if v is not None and ' ' not in v:
            raise ValueError("idProdutoLoja deve conter pelo menos um espaço.")
        return v
