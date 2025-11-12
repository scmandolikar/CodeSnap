# codesnap/core/image_generator.py

from PIL import Image, ImageDraw, ImageFont
from pygments import highlight
from pygments.lexers import get_lexer_by_name
# This is the final corrected import:
from pygments.formatters.img import ImageFormatter
from pygments.styles import get_style_by_name
import io


def generate_image(code: str, language: str, style_name: str, font_name: str, font_size: int, line_numbers: bool):
    """
    Generates a PNG image of the code snippet using the new ImageFormatter.
    """
    try:
        lexer = get_lexer_by_name(language, stripall=True)
        style = get_style_by_name(style_name)

        # Use the new ImageFormatter and specify the format as PNG
        formatter = ImageFormatter(
            image_format='PNG',
            style=style,
            font_face=font_name,
            font_size=font_size,
            line_numbers=line_numbers,
            image_padding=20
        )

        # Highlight the code and get the image data
        image_bytes = highlight(code, lexer, formatter)
        
        # Load the image from bytes
        image = Image.open(io.BytesIO(image_bytes))
        
        # --- Add a custom background ---
        bg_color = style.background_color or "#272822" # Default to Monokai's background
        
        # Calculate new image size with extra padding for the frame effect
        final_padding = 40
        new_size = (image.width + final_padding, image.height + final_padding)
        
        final_image = Image.new('RGBA', new_size, bg_color)
        
        # Paste the code image onto the background, centered
        paste_position = (final_padding // 2, final_padding // 2)
        final_image.paste(image, paste_position)
        
        return final_image

    except Exception as e:
        print(f"Error generating image: {e}")
        return None