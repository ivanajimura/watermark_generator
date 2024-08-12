import os
from typing import Annotated, BinaryIO
from fastapi import FastAPI, File, UploadFile, APIRouter
from fastapi.responses import FileResponse
from backend.schemas.Watermark import CreateTextWatermark
from backend.core.watermarker import Watermarker
from backend.core.uploaded_file import UploadedFile
from fastapi.responses import RedirectResponse

from backend.core.config import settings


router: APIRouter = APIRouter()
@router.get("/")
async def redirect_docs() -> RedirectResponse:
    return RedirectResponse(url="http://127.0.0.1:8000/docs#/")

@router.post("/png_watermark/")
async def add_image_watermark(image: UploadFile,
                             watermark_image: UploadFile,
                             pos_x: int = 0,
                             pos_y: int = 0):
    image_content: BinaryIO = UploadedFile.get_file(uploaded_file = image)
    watermark_image_content: BinaryIO = UploadedFile.get_file(uploaded_file = watermark_image)
    file_name: str = UploadedFile.get_file_name(uploaded_file = image).split(".")[0]
    file_name = Watermarker.add_img_wm_to_img(main_image = image_content, watermark_image = watermark_image_content, pos_x=pos_x, pos_y=pos_y, file_name= file_name)
    response = UploadedFile.create_response_obj(
                                                                file_location = settings.OUTPUT_FOLDER,
                                                                media_type="image/jpeg",
                                                                file_name = file_name.get("file_name"))
    return response


@router.post("/text_watermark/")
async def add_text_watermark(file: UploadFile,
                             wm_text: str,
                             wm_orientation: int = 0,
                             wm_text_size: int = 20,
                             wm_text_color_red = 0,
                             wm_text_color_green = 0,
                             wm_text_color_blue = 0,
                             pos_x = 0,
                             pos_y = 0
                             ) -> dict[str, str | None]:
    
    watermark_input: CreateTextWatermark = CreateTextWatermark(
        text_watermark=wm_text,
        watermark_orientation=wm_orientation,
        text_size = wm_text_size,
        text_color_red=wm_text_color_red,
        text_color_green=wm_text_color_green,
        text_color_blue=wm_text_color_blue,
        pos_x = pos_x,
        pos_y = pos_y
        )
    file_name: str = UploadedFile.get_file_name(uploaded_file = file)
    file_content: BinaryIO = UploadedFile.get_file(uploaded_file = file)


    watermarked_file = Watermarker.add_text_watermark(
        image_file = file_content,
        watermark_options = watermark_input,
        file_name = file_name
        )
    response = UploadedFile.create_response_obj(
                                                                file_location = settings.OUTPUT_FOLDER,
                                                                media_type="image/jpeg",
                                                                file_name = watermarked_file.get("file_name"))
    return response

