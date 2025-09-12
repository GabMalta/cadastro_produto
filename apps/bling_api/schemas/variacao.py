from typing import List, Optional, Union
from pydantic import BaseModel

from .categoria import Categoria
from .estoque import EstoqueVar
from .dimensoes import Dimensoes
from .tributacao import Tributacao
from .midia import Midia

class Contato(BaseModel):
    id: int
    nome: str

class Fornecedor(BaseModel):
    id: str = None
    contato: Optional[Contato] = None
    codigo: Optional[str] = None
    precoCusto: float = 0
    precoCompra: float = 0

class ProdutoPai(BaseModel):
    id: int
    cloneInfo: bool

class VariacaoInterna(BaseModel):
    nome: str
    ordem: int
    produtoPai: ProdutoPai

class LinhaProduto(BaseModel):
    id: int

class Estrutura(BaseModel):
    tipoEstoque: Optional[str] = None
    lancamentoEstoque: Optional[str] = None
    componentes: List = []

class Variacao(BaseModel):
    id: Optional[int] = None
    nomeVariacao: str
    codigo: str
    preco: float
    precoCusto: Optional[float] = 0
    estoque: EstoqueVar = EstoqueVar()
    tipo: str = "P"
    situacao: str = "A"
    formato: str = "S"
    descricaoCurta: Optional[str] = None
    imagemURL: Optional[str] = None
    dataValidade: Optional[str] = None
    unidade: str = "Mt"
    pesoLiquido: float
    pesoBruto: float
    volumes: Union[int, float] = 0
    itensPorCaixa: Union[int, float] = 0
    gtin: Optional[str] = None
    gtinEmbalagem: Optional[str] = None
    tipoProducao: str = "T"
    condicao: int = 1
    freteGratis: Union[bool, str] = False
    marca: Optional[str] = None
    descricaoComplementar: Optional[str] = None
    linkExterno: Optional[str] = None
    observacoes: Optional[str] = None
    descricaoEmbalagemDiscreta: Optional[str] = None
    categoria: Categoria = Categoria(id=2432774)
    fornecedor: Fornecedor = Fornecedor()
    actionEstoque: Optional[str] = None
    dimensoes: Dimensoes
    tributacao: Tributacao = Tributacao(ncm="5407.52.10", origem=2)
    midia: Midia = Midia()
    linhaProduto: Optional[LinhaProduto] = None
    estrutura: Optional[Estrutura] = None
    camposCustomizados: List = []
