from typing import Optional, Union
from pydantic import BaseModel

class GrupoProduto(BaseModel):
    id: Union[str, int, None] = 0

class Tributacao(BaseModel):
    origem: Union[str, int] = None
    nFCI: Optional[str] = None
    ncm: Optional[str] = None
    cest: Optional[str] = None
    codigoListaServicos: Optional[str] = None
    spedTipoItem: Optional[str] = None
    codigoItem: Optional[str] = None
    percentualTributos: float = 0
    valorBaseStRetencao: float = 0
    valorStRetencao: float = 0
    valorICMSSubstituto: float = 0
    codigoExcecaoTipi: Optional[str] = None
    classeEnquadramentoIpi: Optional[str] = None
    valorIpiFixo: float = 0
    codigoSeloIpi: Optional[str] = None
    valorPisFixo: float = 0
    valorCofinsFixo: float = 0
    codigoANP: Optional[str] = None
    descricaoANP: Optional[str] = None
    percentualGLP: float = 0
    percentualGasNacional: float = 0
    percentualGasImportado: float = 0
    valorPartida: float = 0
    tipoArmamento: int = 0
    descricaoCompletaArmamento: Optional[str] = None
    dadosAdicionais: Optional[str] = None
    grupoProduto: GrupoProduto = GrupoProduto()
