from typing import Optional
from pydantic import BaseModel


class CampoCustomizado(BaseModel):
    idCampoCustomizado: int
    idVinculo: int
    valor: Optional[str] = ""
    item: Optional[str] = ""


def campos_customizados_padrao():
    return [
        CampoCustomizado(
            idCampoCustomizado=2668618,
            idVinculo=752799787,
            valor="227760129",
            item="Legítima Têxtil",
        ),
        CampoCustomizado(
            idCampoCustomizado=2668619,
            idVinculo=752799788,
            valor="227760240",
            item="China",
        ),
        CampoCustomizado(
            idCampoCustomizado=2668622,
            idVinculo=752799789,
            valor="1,00",
            item="",
        ),
        CampoCustomizado(
            idCampoCustomizado=2668624,
            idVinculo=752799790,
            valor="1",
            item="",
        ),
        CampoCustomizado(
            idCampoCustomizado=2668653,
            idVinculo=752799791,
            valor="Legítima Têxtil",
            item="",
        ),
        CampoCustomizado(
            idCampoCustomizado=2668654,
            idVinculo=752799792,
            valor="Tecido",
            item="",
        ),
        CampoCustomizado(
            idCampoCustomizado=2668655,
            idVinculo=752799793,
            valor="Textil",
            item="",
        ),
        CampoCustomizado(
            idCampoCustomizado=2668658,
            idVinculo=752799794,
            valor="",
            item="",
        ),
        CampoCustomizado(
            idCampoCustomizado=2668659,
            idVinculo=752799795,
            valor="",
            item="",
        ),
        CampoCustomizado(
            idCampoCustomizado=2668660,
            idVinculo=752799796,
            valor="1",
            item="",
        ),
        CampoCustomizado(
            idCampoCustomizado=2668662,
            idVinculo=752799797,
            valor="227770381",
            item="m",
        ),
        CampoCustomizado(
            idCampoCustomizado=2668665,
            idVinculo=752799798,
            valor="",
            item="",
        ),
        CampoCustomizado(
            idCampoCustomizado=3480772,
            idVinculo=1004684146,
            valor="315789973",
            item="Não",
        ),
    ]
