from pydantic import BaseModel


class ImageResponse(BaseModel):
#    image_id: int
#    image_name: str
    image_data: bytes