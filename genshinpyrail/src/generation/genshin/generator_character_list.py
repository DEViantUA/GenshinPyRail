# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

import asyncio

from ...tools import utility, pill, git_file
from PIL import Image,ImageDraw

git = git_file.ImageCache()

class Creat:
    def __init__(self, data) -> None:
        self.data = data
        self.character_info = {}
        self.count = {
            "five": 0,
            "four": 0,
            "pyro": 0,
            "cryo": 0,
            "dendro": 0,
            "electro": 0,
            "geo": 0,
            "anemo": 0,
            "hydro": 0,
        }
    
    async def open_bacground(self, rarity):
        if rarity == 5:
            return await git.charter_list_stars_5
        elif rarity == 4:
            return await git.charter_list_stars_4
        elif rarity == 3:
            return await git.charter_list_stars_3
        elif rarity == 2:
            return await git.charter_list_stars_2
        else:
            return await git.charter_list_stars_1
    
    async def creat_background_card(self,rarity,weapon_rarity):
        bacground = await git.bg_charter_list
        bacground = bacground.copy().convert("RGBA")
        bacground_character = await self.open_bacground(rarity)
        bacground_weapon = await self.open_bacground(weapon_rarity)
        
        bacground.paste(bacground_character.convert("RGBA").resize((106,110)),(0,0), self.maska_character.convert("L"))
        bacground.paste(bacground_weapon.convert("RGBA").resize((109,110)),(110,0), self.maska_weapon.convert("L"))
        
        return bacground
        
    
    async def creat_cards(self,data):
        name = data.name
        element = data.element
        element_icon = await utility.get_element_genshin_img(element)
        element_icon = await pill.recolor_image(element_icon.copy().resize((30,30)),(255,255,255,255))
        
        rarity = data.rarity
        icon = await pill.get_dowload_img(f"https://api.ambr.top/assets/UI/{data.icon.split('character_icon/')[1]}", size = (106,110))
        level = data.level
        friendship = data.friendship
        constellation = data.constellation
        
        weapon_rarity = data.weapon.rarity
        weapon_level = data.weapon.level
        weapon_refinement = data.weapon.refinement
        weapon_icon = await pill.get_dowload_img(data.weapon.icon, size = (109,110))
        
        background = await self.creat_background_card(rarity,weapon_rarity)      
        background_icon = Image.new("RGBA", (109,110), color = (0,0,0,0))
        background_icon.paste(weapon_icon,(0,0),self.maska_weapon.convert("L"))
        background.alpha_composite(background_icon,(117,0))

        background_icon = Image.new("RGBA", (106,110), color = (0,0,0,0))
        background_icon.paste(icon,(0,0),self.maska_character.convert("L"))
        background.alpha_composite(background_icon,(0,0))
        background.alpha_composite(self.frame)
        background.alpha_composite(element_icon,(2,4))
        
        draw = ImageDraw.Draw(background)
        x = self.t18.getlength(name)
        draw.text((int(108-x/2),109), name, font= self.t18, fill=(255,255,255,255))
        draw.text((113,5), f"LVL: {level}", font= self.t14, fill=(255,255,255,255))
        draw.text((136,26), str(friendship), font= self.t14, fill=(255,255,255,255))
        draw.text((113,47), f"C{constellation}", font= self.t14, fill=(255,255,255,255))
        
        draw.text((171,79), f"LVL: {weapon_level}", font= self.t11, fill=utility.element_genshin_color.get(element, (255,255,255,255)))
        draw.text((199,59), f"R{weapon_refinement}", font= self.t11, fill= utility.element_genshin_color.get(element, (255,255,255,255)))
        
        self.count[element.lower()] += 1
        if rarity == 5:
            rarity = "five"
        else:
            rarity = "four"
        
        self.character_info[data.id] = {"id": data.id, "name": data.name, "rarity": data.rarity, "icon": f"https://api.ambr.top/assets/UI/{data.icon.split('character_icon/')[1]}"}
        
        self.count[str(rarity)] += 1
        
        return {"id": data.id, "card": background}
    
    async def start(self, character_id = None):
        await git_file.change_Font(0)
        self.maska_character = await git.maska_charter_list
        self.maska_weapon = await git.maska_weapon_list
        self.frame = await git.frame_charter_list
        self.t18 = await pill.get_font(18)
        self.t14 = await pill.get_font(14)
        self.t11 = await pill.get_font(11)
        
        if character_id is None:
            card = await asyncio.gather(*[self.creat_cards(key) for key in self.data])
        else:
            for key in self.data:
                if key.id == int(character_id):
                    card = await self.creat_cards(key)
                    return {"count": self.count, "card": card["card"], "icon": [card], "character": self.character_info}
        
        images_per_row = 6
        spacing = 10
        image_size = (219, 131)

        # Вычисляем размер фона
        num_images = len(card)
        num_rows = (num_images + images_per_row - 1) // images_per_row
        width = images_per_row * (image_size[0] + spacing) + 20
        height = num_rows * (image_size[1] + spacing) + 16

        background = Image.new('RGBA', (width-2, height), color= (0,0,0,0))

        for i, image in enumerate(card):
            row = i // images_per_row
            col = i % images_per_row
            x = 10 + col * (image_size[0] + spacing)
            y = 8 + row * (image_size[1] + spacing)

            background.alpha_composite(image["card"], (x, y))
            
        return {"count": self.count, "card": background, "icon": card, "character": self.character_info}