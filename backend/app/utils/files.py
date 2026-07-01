import base64
from fastapi import UploadFile


async def encode_image_to_base64(image: UploadFile) -> str:
    """Кодировать изображение в base64"""
    if not image or not image.filename:
        return None
    
    content = await image.read()
    return (
        "data:"
        + image.content_type
        + ";base64,"
        + base64.b64encode(content).decode()
    )
