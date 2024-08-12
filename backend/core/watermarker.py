from typing import BinaryIO
from PIL import Image, ImageDraw, ImageFont, ImageOps
from PIL.ImageFile import ImageFile

from backend.schemas.Watermark import CreateTextWatermark
from backend.core.config import settings


class Watermarker():

    @staticmethod
    def add_text_watermark(image_file: BinaryIO,
                           watermark_options: CreateTextWatermark,
                           file_name: str = "watermarked_image",
                           output_folder: str = settings.OUTPUT_FOLDER) -> dict[str, str]:
        
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
        return orig_position if orig_position != 0 else default_value
    
    @staticmethod
    def set_color(r: int,g: int,b: int) -> tuple[int, int, int]:
        if 0 <= r <= 128 and 0 <= g <= 128 and 0 <= b <= 128:
            return (r, g, b)
        return (0, 0, 0)
    
    @staticmethod
    def open_image_binary(binary: BinaryIO) -> ImageFile:
        return Image.open(fp = binary)
    
    @staticmethod
    def get_img_width(img: ImageFile) -> float:
        return img.size[0]
    
    @staticmethod
    def get_img_heigth(img: ImageFile) -> float:
        return img.size[1]
    
    @staticmethod
    def get_watermarker_text(wm_object: CreateTextWatermark) -> str:
        return wm_object.text_watermark
    
    @staticmethod
    def get_watermarker_size(wm_object: CreateTextWatermark) -> int:
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
        txt=Image.new('L', img.size)
        d = ImageDraw.Draw(txt)
        d.text( position, text,  font=font, fill=255)
        w=txt.rotate(angle,  expand=1)
        img.paste( ImageOps.colorize(w, (0,0,0), fill_color), (0,0),  w)
             
    @staticmethod
    def save_img(img: ImageFile, file_name: str = "watermarked", file_path: str = settings.OUTPUT_FOLDER) -> None:
        output_filename: str = f"{file_path}/{file_name}.{img.format}"
        img.save(fp = output_filename)
    
    @staticmethod
    def load_font(font: str = "", font_size: int = 100) -> ImageFont:
        if font == "":
            return ImageFont.load_default(size=int(font_size))
        try:
            return ImageFont.truetype(f"{font}.ttf", int(font_size))
        except Exception as e:
            print(e)
            return ImageFont.load_default(size=int(font_size))
    
    @staticmethod
    def get_position(x: float, y:float) -> tuple[int, int]:
        return (int(x),int(y))
    
    @staticmethod
    def add_img_wm_to_img(main_image: BinaryIO, watermark_image: BinaryIO, pos_x: int = 0, pos_y: int = 0, file_name: str = "watermarked"):
        main_image = Watermarker.open_image_binary(main_image)
        watermark_image = Watermarker.open_image_binary(watermark_image)
        main_image.paste(watermark_image, (pos_x, pos_y), watermark_image)
        Watermarker.save_img(img = main_image, file_name = file_name)       
        main_image.show()
        return {"file_name": f"{file_name}.{main_image.format}"}