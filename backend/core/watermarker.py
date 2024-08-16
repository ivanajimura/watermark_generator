from typing import BinaryIO
from PIL import Image, ImageDraw, ImageFont, ImageOps
from PIL.ImageFile import ImageFile

from backend.schemas.Watermark import CreateTextWatermark
from backend.core.config import settings


class Watermarker():
    """Collection of methods related to adding watermark to an image
    """
    @staticmethod
    def add_text_watermark(image_file: BinaryIO,
                           watermark_options: CreateTextWatermark,
                           file_name: str = "watermarked_image",
                           output_folder: str = settings.OUTPUT_FOLDER) -> dict[str, str]:
        """Adds watermark from a string

        Args:
            image_file (BinaryIO): binary of the image
            watermark_options (CreateTextWatermark): Options related to position and color
            file_name (str, optional): name of the output file. Defaults to "watermarked_image".
            output_folder (str, optional): Folder where to save the image. Defaults to settings.OUTPUT_FOLDER.

        Returns:
            dict[str, str]: {"output_folder": output_folder, "file_name": f"{file_name}.{pic.format}"}
        """        
        pic: ImageFile = Watermarker.open_image_binary(image_file)
        width = Watermarker.get_img_width(img = pic)
        height = Watermarker.get_img_heigth(img = pic)
        watermark_text: str = Watermarker.get_watermarker_text(wm_object = watermark_options)
        fill_color: tuple[int, int, int]  = Watermarker.set_color(r = watermark_options.text_color_red,
                                                                  g = watermark_options.text_color_green,
                                                                  b = watermark_options.text_color_blue)
        x: float = Watermarker.set_pos_if_zero(orig_position = watermark_options.pos_x, default_value = width/4)
        y: float = Watermarker.set_pos_if_zero(orig_position = watermark_options.pos_y, default_value = height/4)
        position: tuple[int, int] = Watermarker.get_position(x = x, y = y)
        font_size: int = Watermarker.get_watermarker_size(wm_object = watermark_options)
        font: ImageFont = Watermarker.load_font(font_size = font_size)

        Watermarker.add_text_to_img(img=pic, position = position, text = watermark_text, font = font, fill_color = fill_color, angle = watermark_options.watermark_orientation)
        file_name = file_name.split(sep=".")[0]
        Watermarker.save_img(img = pic, file_path = output_folder, file_name = file_name)
        pic.show()
        return {"output_folder": output_folder, "file_name": f"{file_name}.{pic.format}"}

    @staticmethod
    def set_pos_if_zero(orig_position: float, default_value: float) -> float:
        """Returns orig_position if it is not zero, otherise returns default_value

        Args:
            orig_position (float): original position
            default_value (float): default location for the watermark

        Returns:
            float: orig_position or default_value
        """        
        return orig_position if orig_position != 0 else default_value
    
    @staticmethod
    def set_color(r: int,g: int,b: int) -> tuple[int, int, int]:
        """Returns tuple[r,g,b] if all values are between 0 and 128

        Args:
            r (int): red value
            g (int): green value
            b (int): blue value

        Returns:
            tuple[int, int, int]: RGB tuple
        """        
        if 0 <= r <= 128 and 0 <= g <= 128 and 0 <= b <= 128:
            return (r, g, b)
        return (0, 0, 0)
    
    @staticmethod
    def open_image_binary(binary: BinaryIO) -> ImageFile:
        """Opens an image from its binary

        Args:
            binary (BinaryIO): binary of the image

        Returns:
            ImageFile: ImageFile object
        """        
        return Image.open(fp = binary)
    
    @staticmethod
    def get_img_width(img: ImageFile) -> float:
        """Gets width of the image

        Args:
            img (ImageFile): image

        Returns:
            float: width
        """        
        return img.size[0]
    
    @staticmethod
    def get_img_heigth(img: ImageFile) -> float:
        """Gets height of the image

        Args:
            img (ImageFile): image

        Returns:
            float: height
        """    
        return img.size[1]
    
    @staticmethod
    def get_watermarker_text(wm_object: CreateTextWatermark) -> str:
        """Gets watermark text from object

        Args:
            wm_object (CreateTextWatermark): object with watermark properties

        Returns:
            str: Watermark text
        """        
        return wm_object.text_watermark
    
    @staticmethod
    def get_watermarker_size(wm_object: CreateTextWatermark) -> int:
        """Gets watermark text size from object

        Args:
            wm_object (CreateTextWatermark): object with watermark properties

        Returns:
            str: Watermark text size
        """       
        return wm_object.text_size
    
    @staticmethod
    def add_text_to_img(
                        img: ImageFile,
                        position: tuple[int, int],
                        text: str,
                        font: ImageFont,
                        fill_color: tuple[int, int, int],
                        angle: int = 0
                        ) -> ImageDraw.ImageDraw:
        """Adds text to an image

        Args:
            img (ImageFile): image to add text
            position (tuple[int, int]): position [width, heigth] where to start the text
            text (str): text to insert
            font (ImageFont): font to use
            fill_color (tuple[int, int, int]): color of the  text
            angle (int, optional): Angle of the text. Defaults to 0. #Not working properly.

        Returns:
            ImageDraw.ImageDraw: _description_
        """        
        if angle != 0:
            return Watermarker.add_rotated_text_to_img(img=img, position=position, text=text, font=font, fill_color=fill_color, angle=angle)
        drawing: ImageDraw.ImageDraw = ImageDraw.Draw(im = img)
        drawing.text(xy = position, text = text, font = font, fill = fill_color)
        return drawing
        
    
    @staticmethod
    def add_rotated_text_to_img(
                                img: ImageFile,
                                position: tuple[int, int],
                                text: str,
                                font: ImageFont,
                                fill_color: tuple[int, int, int],
                                angle: int = 90
                                ):       
        """Adds text with rotation to an image

        Args:
            img (ImageFile): image where to add text
            position (tuple[int, int]): position of the text [width, height]
            text (str): text to insert
            font (ImageFont): font of the text
            fill_color (tuple[int, int, int]): color of the text
            angle (int, optional): Angle of the text. Defaults to 90.
        """        
        txt=Image.new('L', img.size)
        d = ImageDraw.Draw(txt)
        d.text( position, text,  font=font, fill=255)
        w=txt.rotate(angle,  expand=1)
        img.paste(ImageOps.colorize(w, (0,0,0), fill_color), (0,0),  w)

             
    @staticmethod
    def save_img(img: ImageFile, file_name: str = "watermarked", file_path: str = settings.OUTPUT_FOLDER) -> None:
        """Save image to file

        Args:
            img (ImageFile): image
            file_name (str, optional): name of the file. Defaults to "watermarked".
            file_path (str, optional): folder. Defaults to settings.OUTPUT_FOLDER.
        """        
        output_filename: str = f"{file_path}/{file_name}.{img.format}"
        img.save(fp = output_filename)
    
    @staticmethod
    def load_font(font: str = "", font_size: int = 100) -> ImageFont:
        """Loads font if it exists otherwise loads default font

        Args:
            font (str, optional): font name. Defaults to "".
            font_size (int, optional): font size. Defaults to 100.

        Returns:
            ImageFont: ImageFont object containing font name and font size
        """        
        if font == "":
            return ImageFont.load_default(size=int(font_size))
        try:
            return ImageFont.truetype(f"{font}.ttf", int(font_size))
        except Exception as e:
            print(e)
            return ImageFont.load_default(size=int(font_size))
    
    @staticmethod
    def get_position(x: float, y:float) -> tuple[int, int]:
        """Obtain position

        Args:
            x (float): x position
            y (float): y position

        Returns:
            tuple[int, int]: x, y
        """        
        return (int(x),int(y))
    
    @staticmethod
    def add_img_wm_to_img(main_image: BinaryIO, watermark_image: BinaryIO, pos_x: int = 0, pos_y: int = 0, file_name: str = "watermarked")-> dict: 
        """Adds image on top of another imge

        Args:
            main_image (BinaryIO): background image
            watermark_image (BinaryIO): image on top
            pos_x (int, optional): where to start the image on top (x). Defaults to 0.
            pos_y (int, optional): where to start the image on top (y). Defaults to 0.
            file_name (str, optional): nane of the output file. Defaults to "watermarked".

        Returns:
            dict: {"file_name": f"{file_name}.{main_image.format}"}
        """        
        main_image = Watermarker.open_image_binary(main_image)
        watermark_image = Watermarker.open_image_binary(watermark_image)
        main_image.paste(watermark_image, (pos_x, pos_y), watermark_image)
        Watermarker.save_img(img = main_image, file_name = file_name)       
        main_image.show()
        return {"file_name": f"{file_name}.{main_image.format}"}