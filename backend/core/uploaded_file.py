import os
from typing import BinaryIO
from fastapi import UploadFile
from starlette.responses import FileResponse

class UploadedFile:
    """Collection of methods to handle uploaded files
    """    

    @staticmethod
    def get_file_name(uploaded_file: UploadFile) -> str | None:
        """Obtains name of the file using .filename

        Args:
            uploaded_file (UploadFile): file itself

        Returns:
            str | None: name of the file
        """        
        return uploaded_file.filename
    
    @staticmethod
    def get_file(uploaded_file: UploadFile) -> BinaryIO:
        """ Returns content of the file using .file

        Args:
            uploaded_file (UploadFile): file itself

        Returns:
            BinaryIO: binary of the file
        """        
        return uploaded_file.file
    
    @staticmethod
    def get_content_type(uploaded_file: UploadFile) -> str | None:
        """Returns type of content of the file using .content_type

        Args:
            uploaded_file (UploadFile): file itself

        Returns:
            str | None: content type
        """        
        return uploaded_file.content_type
    
    @staticmethod
    def create_response_obj(file_location: str, file_name: str, media_type: str = 'image/jpeg') -> FileResponse:
        """Creates response object for API

        Args:
            file_location (str): complete path of the file
            file_name (str): name of the file
            media_type (str, optional): content type. Defaults to 'image/jpeg'.

        Returns:
            FileResponse: Object FileResponse(path, media_type, filename)
        """        
        file_path: str = f"{os.getcwd()}/{file_location}/{file_name}"
        response = FileResponse(path = file_path, media_type = media_type, filename = file_name)
        return response