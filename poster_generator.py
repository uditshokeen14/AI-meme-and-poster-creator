from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

def create_poster(template_path, caption, font_name="Anton-Regular.ttf", font_size=40):

    image = Image.open(template_path).convert("RGBA")
    image = image.resize((800, 1000))

    draw = ImageDraw.Draw(image)

    font_path = os.path.join("fonts", font_name)

    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        font = ImageFont.load_default()

    wrapped_text = textwrap.fill(caption, width=25)

    width, height = image.size

    bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (width - text_width) / 2
    y = height - text_height - 80

    # Meme-style outline
    outline = 2
    for i in range(-outline, outline + 1):
        for j in range(-outline, outline + 1):
            draw.multiline_text(
                (x + i, y + j),
                wrapped_text,
                font=font,
                fill="black",
                align="center"
            )

    draw.multiline_text(
        (x, y),
        wrapped_text,
        font=font,
        fill="white",
        align="center"
    )

    output_path = "output.png"
    image.save(output_path)

    return output_path