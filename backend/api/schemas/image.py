from pydantic import BaseModel


class ImageResponse(BaseModel):
    image_data: bytes

class ImageCreate(BaseModel):
    name: str
    imgdata: bytes
