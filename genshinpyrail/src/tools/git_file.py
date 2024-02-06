# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.
from PIL import Image
import threading
from pathlib import Path
import aiohttp
from io import BytesIO
from cachetools import TTLCache

lock = threading.Lock()

_cache = TTLCache(maxsize=1000, ttl=300)

assets = Path(__file__).parent.parent
_BASE_URL = 'https://raw.githubusercontent.com/DEViantUA/GenshinPyRailAssets/main/'

font = str(assets /'font' / 'Genshin_Impact.ttf')
fontH = str(assets / 'font' / 'comforta.ttf')

async def change_Font(x):
    global font
    if x == 0:
        font = str(assets / 'font' / 'Genshin_Impact.ttf')
    else:
        font = str(assets / 'font' / 'comforta.ttf')

mapping = {
    "logo": "assets/LOGO.png",
    "ascension_bg_wind": "assets/matterial/bg/ANEMO.png",
    "ascension_bg_ice": "assets/matterial/bg/CRYO.png",
    "ascension_bg_electro": "assets/matterial/bg/ELECTRO.png",
    "ascension_bg_rock": "assets/matterial/bg/GEO.png",
    "ascension_bg_water": "assets/matterial/bg/GYDRO.png",
    "ascension_bg_fire": "assets/matterial/bg/PYRO.png",
    "ascension_bg_grass": "assets/matterial/bg/DENDRO.png",
    "ascension_frames": "assets/matterial/frame/ANEMO.png",
    "ascension_mask_boss": "assets/matterial/frame/FRAME_DAY_BOSS.png",
    "ascension_mob": "assets/matterial/bg/BG_MOB.png",
    
    'background_frame': 'assets/matterial_star_raill/background_frame.png',
    'background': 'assets/matterial_star_raill/background.png',
    'desc_frame': 'assets/matterial_star_raill/desc_frame.png',
    'github_logo': 'assets/matterial_star_raill/github_logo.png',
    'm_logo': 'assets/matterial_star_raill/m_logo.png',
    'maska': 'assets/matterial_star_raill/maska.png',
    'material_1': 'assets/matterial_star_raill/material_1.png',
    'material_2': 'assets/matterial_star_raill/material_2.png',
    'material_3': 'assets/matterial_star_raill/material_3.png',
    'material_4': 'assets/matterial_star_raill/material_4.png',
    'material_5': 'assets/matterial_star_raill/material_5.png',
    'matterial_frame': 'assets/matterial_star_raill/matterial_frame.png',
    'path_frame': 'assets/matterial_star_raill/path_frame.png',
    'shadow': 'assets/matterial_star_raill/shadow.png',
    'stars_4': 'assets/matterial_star_raill/stars_4.png',
    'stars_5': 'assets/matterial_star_raill/stars_5.png',
    'text_charter': 'assets/matterial_star_raill/text_charter.png',

    'charter_list_stars_5': 'assets/genshin_charter_list/5_stars.png',
    'charter_list_stars_4': 'assets/genshin_charter_list/4_stars.png',
    'charter_list_stars_3': 'assets/genshin_charter_list/3_stars.png',
    'charter_list_stars_2': 'assets/genshin_charter_list/2_stars.png',
    'charter_list_stars_1': 'assets/genshin_charter_list/1_stars.png',
    
    'bg_charter_list': 'assets/genshin_charter_list/bg_charter_list.png',
    'frame_charter_list': 'assets/genshin_charter_list/frame_charter_list.png',
    'info_frame_charter_list': 'assets/genshin_charter_list/info_frame_charter_list.png',
    'maska_charter_list': 'assets/genshin_charter_list/maska_charter.png',
    'maska_weapon_list': 'assets/genshin_charter_list/maska_weapon.png',


    'background_raill_charter_list': 'assets/raill_charter_list/background_raill_charter_list.png',
    'maska_raill_charter_list_lc': 'assets/raill_charter_list/maska_raill_charter_list_lc.png',
    'maska_raill_charter_list_left': 'assets/raill_charter_list/maska_raill_charter_list_left.png',
    'maska_raill_charter_list_right': 'assets/raill_charter_list/maska_raill_charter_list_right.png',
    'raill_shadow_charter_list': 'assets/raill_charter_list/raill_shadow_charter_list.png',
    'raill_up_charter_list': 'assets/raill_charter_list/raill_up_charter_list.png',
    'level_frame_charter_list': 'assets/raill_charter_list/level_frame_charter_list.png',
    
    "bg_tcg":'assets/tcg/bg_tcg.png',
    "frame_charters_tcg":'assets/tcg/frame_charters.png',
    "frame_others_tcg":'assets/tcg/frame_others.png',
    "icons_stats_tcg":'assets/tcg/icons_stats.png',
    
    
    "CostTypeAnemo":'assets/tcgInfo/CostTypeAnemo.png',
    "CostTypeArcane":'assets/tcgInfo/CostTypeArcane.png',
    "CostTypeCryo":'assets/tcgInfo/CostTypeCryo.png',
    "CostTypeDenro":'assets/tcgInfo/CostTypeDenro.png',
    "CostTypeElectro":'assets/tcgInfo/CostTypeElectro.png',
    "CostTypeGeo":'assets/tcgInfo/CostTypeGeo.png',
    "CostTypeHydro":'assets/tcgInfo/CostTypeHydro.png',
    "CostTypePyro":'assets/tcgInfo/CostTypePyro.png',
    "CostTypeSame":'assets/tcgInfo/CostTypeSame.png',
    "CostTypeVoid":'assets/tcgInfo/CostTypeVoid.png',
    
    
    "hp_icon":'assets/tcgInfo/hp_icon.png',
    "name_tcg_tags":'assets/tcgInfo/name_tcg_tags.png',
    "big_talant_bacgkround_tcg": 'assets/tcgInfo/big_talant_bacgkround_tcg.png',
    "big_tcg_background_info": 'assets/tcgInfo/big_tcg_background_info.png',
    "frame_tcg_card":'assets/tcgInfo/frame_tcg_card.png',
    "talant_bacgkround_tcg":'assets/tcgInfo/talant_bacgkround_tcg.png',
    "tcg_background_card":'assets/tcgInfo/tcg_background_card.png',
    "tcg_background_info":'assets/tcgInfo/tcg_background_info.png',
    "tcg_stars_1":'assets/tcgInfo/tcg_stars_1.png',
    "tcg_stars_2":'assets/tcgInfo/tcg_stars_2.png',
    "tcg_stars_3":'assets/tcgInfo/tcg_stars_3.png',
    "tcg_cost_icon":'assets/tcgInfo/cost_icon.png',
    
    'g_five': 'assets/raill/stars/g_five.png',
    'g_four': 'assets/raill/stars/g_four.png',
    'g_three': 'assets/raill/stars/g_three.png',
    'g_two': 'assets/raill/stars/g_two.png',
    'g_one': 'assets/raill/stars/g_one.png',
    

    "fire":'assets/element/IconAttributeFire.png',
    "ice":'assets/element/IconAttributeIce.png',
    "imaginary":'assets/element/IconAttributeImaginary.png',
    "physical":'assets/element/IconAttributePhysical.png',
    "quantum":'assets/element/IconAttributeQuantum.png',
    "thunder":'assets/element/IconAttributeThunder.png',
    "wind":'assets/element/IconAttributeWind.png',
    
    
    "anemo":'assets/element/anemo.png',
    "cryo":'assets/element/cryo.png',
    "electro":'assets/element/electro.png',
    "dendro":'assets/element/dendro.png',
    "geo":'assets/element/geo.png',
    "gydro":'assets/element/gydro.png',
    "pyro":'assets/element/pyro.png',
    
    
    "abundance":'assets/path/Abundance.png',
    "destruction":'assets/path/Destruction.png',
    "erudition":'assets/path/Erudition.png',
    "explore":'assets/path/Explore.png',
    "harmony":'assets/path/Harmony.png',
    "hunt":'assets/path/Hunt.png',
    "joy":'assets/path/Joy.png',
    "memory":'assets/path/Memory.png',
    "nihility":'assets/path/Nihility.png',
    "preservation":'assets/path/Preservation.png',
    
    
}

class ImageCache:
    @classmethod
    async def download_image(cls, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                try:
                    image = await response.read()
                finally:
                    await session.close()
                    
        return BytesIO(image)

    @classmethod
    async def _load_image(cls, name):
        url = _BASE_URL + name
        if url in _cache:
            return _cache[url]
        else:
            image_data = await cls.download_image(url)
            image = Image.open(image_data)
            _cache[url] = image
        return image

    async def __getattr__(self, name):
        if name in mapping:
            return await self._load_image(mapping[name])
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        
    async def download_icon_stats(self, prop_id):
        if 'icon_stats' in mapping:
            url = mapping['icon_stats'].format(prop_id=prop_id)
            full_url = _BASE_URL + url
            if full_url in _cache:
                return _cache[full_url].copy()
            else:
                image_data = await self.download_image(full_url)
                image = Image.open(image_data)
                _cache[full_url] = image
                return image.copy()
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute 'icon_stats'")

    async def download_icon_constant(self, element, unlock, resizes = None):
        if 'icon_const_unlock' in mapping and "icon_const_lock" in mapping:
            if unlock:
                url = mapping['icon_const_unlock'].format(element=element.upper())
            else:
                url = mapping['icon_const_lock'].format(element=element.upper())
            full_url = _BASE_URL + url
            key = (full_url, resizes, unlock)
            if key in _cache:
                return _cache[key].copy()
            else:
                image_data = await self.download_image(full_url)
                image = Image.open(image_data)
                if not resizes is None:
                    image = image.resize(resizes)
                    
                _cache[full_url] = image
                return image.copy()
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute 'icon_stats'")