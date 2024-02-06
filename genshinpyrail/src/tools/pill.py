# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from PIL import ImageFont,Image,ImageDraw
from io import BytesIO
from . import git_file
import aiohttp, json

from PIL import Image

from cachetools import TTLCache


git = git_file.ImageCache()


async def get_font(size):
    return ImageFont.truetype(git_file.font, size)

cache = TTLCache(maxsize=1000, ttl=300)  

async def get_dowload_img(link,size = None, thumbnail_size = None):
    cache_key = json.dumps((link, size, thumbnail_size), sort_keys=True)  # Преобразовываем в строку
        
    if cache_key in cache:
        return cache[cache_key]
    headers_p = {}
    try:
        if "pximg" in link:
            headers_p = {
                "referer": "https://www.pixiv.net/",
            }
        async with aiohttp.ClientSession(headers=headers_p) as session, session.get(link) as r:
            try:
                image = await r.read()
            finally:
                await session.close()
    except:
        raise
    try:
        image = Image.open(BytesIO(image)).convert("RGBA")
    except:
        print(link)
        raise
    if size:
        image = image.resize(size)
        cache[cache_key] = image
        return image
    elif thumbnail_size:
        image.thumbnail(thumbnail_size)
        cache[cache_key] = image
        return image
    else:
        cache[cache_key] = image
        return image


async def recolor_image(image, target_color):
    result = Image.new('RGBA', image.size, target_color)
    
    if image.mode == 'RGBA':
        result.putalpha(image.split()[-1])
    
    return result


async def create_image_text(text, font_size, max_width=336, max_height=None, color=(255, 255, 255, 255)):
    original_font = await get_font(font_size)
    font = original_font
    lines = []
    line = []
    for word in text.split():
        if '\\n' in word:
            parts = word.split('\\n')
            line.append(parts[0])
            lines.append(line)
            line = []
            if len(parts) > 1:
                line.append(parts[1])
        else:
            if line:
                temp_line = line + [word]
                temp_text = ' '.join(temp_line)
                temp_width = font.getmask(temp_text).getbbox()[2]
                if temp_width <= max_width:
                    line = temp_line
                else:
                    lines.append(line)
                    line = [word]
            else:
                line = [word]

    if line:
        lines.append(line)

    width = 0
    height = 0
    for line in lines:
        line_width = font.getmask(' '.join(line)).getbbox()[2]
        width = max(width, line_width)
        height += font.getmask(' '.join(line)).getbbox()[3]

    if max_height is not None and height > max_height:
        reduction_ratio = max_height / height
        new_font_size = int(font_size * reduction_ratio)
        font = await get_font(new_font_size)

    img = Image.new('RGBA', (min(width, max_width), height + (font_size + 2)), color=(255, 255, 255, 0))

    draw = ImageDraw.Draw(img)
    y_text = 0
    for line in lines:
        text_width, text_height = font.getmask(' '.join(line)).getbbox()[2:]
        draw.text((0, y_text), ' '.join(line), font=font, fill=color)
        y_text += text_height + 3

    return img
