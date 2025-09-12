from typing import List, Optional, Union
from pydantic import BaseModel

class ImagemExterna(BaseModel):
    link: str

class Imagens(BaseModel):
    externas: List[ImagemExterna] = []
    internas: List = []
    imagensURL: Union[List[ImagemExterna], str] = []

class Video(BaseModel):
    url: Optional[str] = None

class Midia(BaseModel):
    video: Video = Video()
    imagens: Imagens = Imagens()
