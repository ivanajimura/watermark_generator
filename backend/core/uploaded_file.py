import json
import yaml
import os
import time
from typing import BinaryIO
from fastapi import UploadFile
from starlette.responses import FileResponse



class UploadedFile:
    
    @staticmethod
    def get_file_name(uploaded_file: UploadFile) -> str | None:
        return uploaded_file.filename
    
    @staticmethod
    def get_file(uploaded_file: UploadFile) -> BinaryIO:
        return uploaded_file.file
    
    @staticmethod
    def get_content_type(uploaded_file: UploadFile) -> str | None:
        return uploaded_file.content_type
    
    @staticmethod
    def create_response_obj(file_location: str, file_name: str, media_type: str = 'image/jpeg') -> FileResponse:
        file_path: str = f"{os.getcwd()}/{file_location}/{file_name}"
        response = FileResponse(path = file_path, media_type = media_type, filename = file_name)
        return response