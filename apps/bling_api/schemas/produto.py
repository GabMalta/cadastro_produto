from typing import List, Optional, Union
from pydantic import BaseModel

from apps.bling_api.schemas.fornecedor import Fornecedor

from .categoria import Categoria
from .estoque import Estoque, EstoqueVar
from .dimensoes import Dimensoes
from .tributacao import Tributacao
from .midia import Midia
from .campos_customizados import CampoCustomizado, campos_customizados_padrao
from .variacao import Variacao


class ProdutoSchema(BaseModel):
    id: Optional[str] = None
    nome: str
    codigo: str
    preco: Union[float, str]
    fornecedor: Fornecedor = Fornecedor()
    tipo: str = "P"
    situacao: str = "A"
    formato: str = "V"
    descricaoCurta: Optional[str] = None
    dataValidade: Optional[str] = None
    unidade: str = "Mt"
    pesoLiquido: Optional[Union[float, str]] = None
    pesoBruto: Optional[Union[float, str]] = None
    volumes: Optional[str] = None
    itensPorCaixa: Optional[str] = None
    gtin: Optional[str] = None
    gtinEmbalagem: Optional[str] = None
    tipoProducao: str = "T"
    condicao: int = 1
    freteGratis: Union[str, bool] = "False"
    marca: str = "Legítima Textil"
    descricaoComplementar: Optional[str] = None
    linkExterno: Optional[str] = None
    observacoes: Optional[str] = None
    categoria: Categoria = Categoria(id=2432774)
    estoque: Estoque = Estoque()
    actionEstoque: Optional[str] = None
    dimensoes: Dimensoes
    tributacao: Tributacao = Tributacao(ncm="5407.52.10", origem=2)
    midia: Midia = Midia()
    camposCustomizados: List[CampoCustomizado] = campos_customizados_padrao()
    variacoes: List[Variacao] = []
