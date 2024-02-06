# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

import aiohttp
import asyncio
import re
from . import git_file

of = git_file.ImageCache()

TOKENS_GIT = "GHSAT0AAAAAACHCJSG3GG56ELVN4KHNC6ZOZNZPSNQ"

LINK_CHARTER_GENSHIN = "https://api.ambr.top/v2/{lang}/avatar"
LINK_MONSTER_GENSHIN = "https://api.ambr.top/v2/{lang}/monster"

AMBR_LINK_IMAGE = "https://api.ambr.top/assets/UI/{splash}.png"

LINK_CHARTER_STARRAIL = "https://api.yatta.top/hsr/v2/{lang}/avatar"

convertor_lang = {
    "ru": "ru-ru",
    "en": "en-us",
    "cn": "zh-cn",
    "tw": "zh-tw",
    "de": "de-de",
    "es": "es-es",
    "fr": "fr-fr",
    "id": "id-id",
    
    "it": "it-it",
    "ja": "ja-ja",
    "ko": "ko-kr",
    "pt": "pt-pt",
    "th": "th-th",
    "vi": "vi-vn",
    "tr": "tr-tr"
}

convertor_lang_swapped = {
    'ru-ru': 'ru',
    'en-us': 'en',
    'zh-cn': 'cn',
    'zh-tw': 'tw',
    'de-de': 'de',
    'es-es': 'es',
    'fr-fr': 'fr',
    'id-id': 'id',
    'it-it': 'it',
    'ja-ja': 'ja',
    'ko-kr': 'ko',
    'pt-pt': 'pt',
    'th-th': 'th',
    'vi-vn': 'vi',
    'tr-tr': 'tr'
}

element_genshin_color = {
    "Pyro": (255,85,85,255),
    "Cryo": (85,197,255,255),
    "Dendro": (161,255,85,255),
    "Electro": (197,85,255,255),
    "Geo": (243,184,71,255),
    "Anemo": (85,255,193,255),
    "Hydro": (85,181,255,255),
}


def replace_values(text, params, keywords):
    if params:
        for key, value in params.items():
            placeholder = f'$[{key}]'
            if placeholder in text:
                text = text.replace(placeholder, str(value))
    if keywords:
        for key, value in keywords.items():
            placeholder = f'$[{key}]'
            if placeholder in text:
                text = text.replace(placeholder, str(value))

    #text = text.replace("\\n"," ")
    
    return text

async def remove_html_tags(text):
    clean_text = re.sub('<.*?>', '', text)
    return clean_text

def remove_brackets_content(text):
    cleaned_text = re.sub(r'\{.*?\}', '', text)
    return cleaned_text

async def get_data_charter(url):
    while True:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["data"]
                else:
                    await asyncio.sleep(1)

async def get_path_img(path):
    if path == "Rogue":
        return await of.hunt
    elif path == "Knight":
        return await of.preservation
    elif path == "Mage":
        return await of.erudition
    elif path == "Priest":
        return await of.abundance
    elif path == "Shaman":
        return await of.harmony
    elif path == "Warlock":
        return await of.nihility
    else:
        return await of.destruction
    
async def get_element_img(element):
    if element == "Fire":
        return await of.fire
    elif element == "Ice":
        return await of.ice
    elif element == "Imaginary":
        return await of.imaginary
    elif element == "Physical":
        return await of.physical
    elif element == "Quantum":
        return await of.quantum
    elif element == "Thunder":
        return await of.thunder
    else:
        return await of.wind
    
async def get_element_genshin_img(element):
    if element == "Anemo":
        return await of.anemo
    elif element == "Cryo":
        return await of.cryo
    elif element == "Dendro":
        return await of.dendro
    elif element == "Electro":
        return await of.electro
    elif element == "Geo":
        return await of.geo
    elif element == "Pyro":
        return await of.pyro
    elif element == "Hydro":
        return await of.gydro

async def ups(x):
    if x == 5:
        return "V"
    elif x == 4:
        return "IV"
    elif x == 3:
        return "III"
    elif x == 2:
        return "II"
    elif x == 1:
        return "I"
    else:
        return "0"

async def get_stars_raill(rank, style = 0):
    if style == 0:
        if rank == 5:
            return await of.g_five
        elif rank == 4:
            return await of.g_four
        elif rank == 3:
            return await of.g_three
        elif rank == 2:
            return await of.g_two
        else:
            return await of.g_one

