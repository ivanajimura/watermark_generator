from pydantic import BaseModel, Field

class CreateTextWatermark(BaseModel):
    text_watermark: str = Field(default = "", description = "Text to add to the image.")
    watermark_orientation: int = Field(default = 0, description = "Angle to rotate the watermark. 0 means horizontal, 90 means vertical top to bottom, 270 means vertical bottom to top")
    text_size: int = Field(default = 20, description = "Font size of the watermark")
    text_color_red: int = Field(default = 0, description = "Red value from 0 to 128")
    text_color_blue: int = Field(default = 0, description = "Blue value from 0 to 128")
    text_color_green: int = Field(default = 0, description = "Green value from 0 to 128")
    pos_x: int = Field(default=0, description = "Where the text will start on x axis")
    pos_y: int = Field(default=0, description = "Where the text will start on y axis")