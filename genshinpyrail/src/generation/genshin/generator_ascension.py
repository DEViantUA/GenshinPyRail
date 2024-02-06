# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.


import json
import asyncio

from PIL import Image,ImageDraw
from ...tools import utility, pill, git_file, update_data
from pathlib import Path

git = git_file.ImageCache()

_DATA =  Path(__file__).parent.parent.parent


color = {
    "Ice": (0, 211, 212, 255),
    "Grass": (0, 212, 0, 255),
    "Wind": (0, 212, 124, 255),
    "Electric": (176, 49, 220, 255),
    "Water": (0, 99, 218, 255) ,
    "Fire": (243, 52, 54, 255),
    "Rock": (245, 170, 0, 255)
}


async def background_ascension(element):
    if element == "Ice":
        return await git.ascension_bg_ice
    elif element == "Grass":
        return await git.ascension_bg_grass
    elif element == "Wind":
        return await git.ascension_bg_wind
    elif element == "Electric":
        return await git.ascension_bg_electric
    elif element == "Water":
        return await git.ascension_bg_water
    elif element == "Fire":
        return await git.ascension_bg_fire
    else:
        return await git.ascension_bg_rock


class Creat:
    def __init__(self, charter_id, lang) -> None:
        self.charter_id = int(charter_id)
        self.lang = utility.convertor_lang_swapped.get(lang, "en")
        self.element = None
        
    async def get_info(self,idC, mobs=False):
        url = f"https://api.ambr.top/v2/{self.lang}/avatar/{idC}"
        if mobs:
            url = f"https://api.ambr.top/v2/{self.lang}/material/{idC}"
        
        return await utility.get_data_charter(url)       

    async def get_mobs(self,idM, ignore = 0):
        file_path = Path(_DATA) / "data" / "ascension" / f"monster_{self.lang}.json"
        data = {}
        if file_path.exists():
            with open(str(_DATA  / "data" / "ascension" / f"monster_{self.lang}.json"), "r", encoding="utf-8") as file:
                data = json.load(file)          
                
        info = {}
        for key in data:
            if key == ignore:
                continue
            if idM in data[key]["reward"]:
                info = data.get(key)
        
        if info == {}:
            await update_data.process_and_save_to_json(lang=self.lang)
            
            with open(str(_DATA  / "data" / "ascension" / f"monster_{self.lang}.json"), "r", encoding="utf-8") as file:
                data = json.load(file)
                
            for key in data:
                if key == ignore:
                    continue
                if idM in data[key]["reward"]:
                    return data.get(key)

        return info
    
    async def creat_background(self):
        splash = await pill.get_dowload_img(utility.AMBR_LINK_IMAGE.format(splash = self.data_charter["icon"].replace("UI_AvatarIcon", "UI_Gacha_AvatarImg")), size= (1692, 838))
        background = await background_ascension(self.element)
        self.background = background.convert("RGBA").copy()
        charter_name = self.data_charter["name"]
        
        d = ImageDraw.Draw(self.background)
        d.text((0, 171), charter_name, font=self.t134, fill= self.color)
        d.text((59, 362), charter_name, font=self.t90, fill=(255, 255, 255, 255))
        d.text((-215, 515), charter_name, font=self.t134, fill= self.color)
        self.background.alpha_composite(splash, (-27, 0))

    async def creat_info(self):
        self.info_background = Image.new("RGBA", (2077,838))
        frames = await git.ascension_frames
        frames = await pill.recolor_image(frames,self.color)
        maska = await git.ascension_mask_boss
        
        d = ImageDraw.Draw(self.info_background)
        i = 0
        
        for inx, key in enumerate(self.data_charter["ascension"]):
            if inx in [0, 5, 6, 7, 8, 9, 10, 11, 12, 13]:
                if int(key) in [202, 104319]:
                    continue
                icons = await pill.get_dowload_img(f"https://api.ambr.top/assets/UI/UI_ItemIcon_{key}.png", thumbnail_size= ((73, 74)))
                if i < 4:
                    if self.data_charter["ascension"][key] == 1:
                        self.info_background.alpha_composite(icons, (1629, 113))
                    elif self.data_charter["ascension"][key] == 2:
                        self.info_background.alpha_composite(icons, (1568, 552))
                    elif self.data_charter["ascension"][key] == 3:
                        self.info_background.alpha_composite(icons, (1676, 552))
                    elif self.data_charter["ascension"][key] == 4:
                        self.info_background.alpha_composite(icons, (1777, 552))
                    i += 1
                else:
                    if self.data_charter["ascension"][key] == 1:
                        self.info_background.alpha_composite(icons, (1583, 247))
                        self.info_background.alpha_composite(icons, (1557, 667))
                    elif self.data_charter["ascension"][key] == 2:
                        self.info_background.alpha_composite(icons, (1700, 247))
                        self.info_background.alpha_composite(icons, (1674, 667))
                    elif self.data_charter["ascension"][key] == 3:
                        self.info_background.alpha_composite(icons, (1806, 247))
                        self.info_background.alpha_composite(icons, (1780, 667))
                    elif self.data_charter["ascension"][key] == 4:
                        self.info_background.alpha_composite(icons, (1435, 424))
                        info_monster = await self.get_mobs(key)
                        icon = await pill.get_dowload_img(info_monster.get("icon"), size= (127, 130))
                        self.info_background.alpha_composite(icon, (1423, 252))
                        self.info_background.alpha_composite(frames, (1423, 252))
                        name = await pill.create_image_text(info_monster["name"], 18, max_width= 206, max_height = 37)
                        self.info_background.alpha_composite(name, (int(1486 - name.size[0]/2), 387))
                    elif self.data_charter["ascension"][key] == 5:
                        self.info_background.alpha_composite(icons, (1418, 666))
                        info_monster = await self.get_mobs(key)
                        maska = await git.ascension_mask_boss
                        icon = await pill.get_dowload_img(info_monster.get("icon"), size= (93, 92))
                        self.info_background.paste(icon, (1406, 581), maska.convert("L"))
            else:
                if self.data_charter["ascension"][key] == 3:
                    x = 1910
                    text = 387
                    half = "left"
                    ignore = 0
                    text_add = 0
                    for keys in range(0,2):
                        info_monster = await self.get_mobs(key, ignore= ignore)
                        icon = await pill.get_dowload_img(info_monster.get("icon"), size= (127, 130))
                        width, height = icon.size
                        if half == "left":
                            region = (0, 0, width // 2, height)
                        elif half == "right":
                            region = (width // 2, 0, width, height)
                            
                        self.info_background.alpha_composite(icon.crop(region), (x, 252))
                        name = await pill.create_image_text(info_monster["name"], 14, max_width= 188, max_height = 37)
                        self.info_background.alpha_composite(name, (int(1977 - name.size[0]/2), text))
                        ignore = info_monster["id"]
                        x += 64
                        text = 441
                        half = "right"
                        if text_add == 0:
                            text_add = name.size[1]
                    d.text((1969, 375 + text_add), "+", font=self.t30, fill= self.color)    
                    self.info_background.alpha_composite(frames, (1910, 252))

    async def build(self):
        self.background.alpha_composite(self.info_background)
        logo = await git.logo
        self.background.alpha_composite(logo)

    async def start(self):
        await git_file.change_Font(0)
        self.t19 = await pill.get_font(19)
        self.t30 = await pill.get_font(30)
        self.t134 = await pill.get_font(134)
        self.t90 = await pill.get_font(90)
        
        
        self.data_charter = await self.get_info(self.charter_id)
        self.element = self.data_charter["element"]
        self.color = color.get(self.element)
        
        await asyncio.gather(self.creat_background(), self.creat_info())
        await self.build()
                
        return {"lang": self.lang, "id": self.charter_id, "card": self.background}