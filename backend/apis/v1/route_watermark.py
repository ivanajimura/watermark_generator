from typing import BinaryIO
from fastapi import UploadFile, APIRouter
from backend.schemas.Watermark import CreateTextWatermark
from backend.core.watermarker import Watermarker
from backend.core.uploaded_file import UploadedFile
from fastapi.responses import FileResponse, RedirectResponse

from backend.core.config import settings


router: APIRouter = APIRouter()


@router.get("/")
async def redirect_docs() -> RedirectResponse:
    """Redirects to Swagger

    Returns:
        RedirectResponse: url to Swagger
    """    
    return RedirectResponse(url=f"http://0.0.0.0:{settings.PORT}/docs#/")


@router.post("/png_watermark/")
async def add_image_watermark(image: UploadFile,
                             watermark_image: UploadFile,
                             pos_x: int = 0,
                             pos_y: int = 0) -> FileResponse:
    """Adds image watermark to an image

    Args:
        image (UploadFile): background image
        watermark_image (UploadFile): watermark image
        pos_x (int, optional): x position where to start adding the top image. Defaults to 0.
        pos_y (int, optional): y position where to start adding the top image. Defaults to 0.

    Returns:
        FileResponse: FileResponse(path, media_type, filename)
    """    
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
                             ) -> FileResponse:
    """Adds text watermark to image

    Args:
        file (UploadFile): image file
        wm_text (str): text to add
        wm_orientation (int, optional): angle of orientation of text. Defaults to 0.
        wm_text_size (int, optional): text size. Defaults to 20.
        wm_text_color_red (int, optional): text color red value from RGB. Defaults to 0.
        wm_text_color_green (int, optional): text color green value from RGB. Defaults to 0.
        wm_text_color_blue (int, optional): text color blue value from RGB. Defaults to 0.
        pos_x (int, optional): x position of watermark. Defaults to 0.
        pos_y (int, optional): y position of watermark. Defaults to 0.

    Returns:
        FileResponse(path, media_type, filename)
    """    
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

