# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from ...tools import utility, pill, git_file
from PIL import Image,ImageDraw

import asyncio


git = git_file.ImageCache()

class Creat:
    def __init__(self, data) -> None:
        self.data = data
        self.charter_info = {}
        self.count = {
            "five": 0,
            "four": 0,
            "ice": 0,
            "imaginary": 0,
            "physical": 0,
            "quantum": 0,
            "lightning": 0,
            "wind": 0,
            "fire": 0,
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
        
    
    async def edit_lc(self, icon):
        background = Image.new("RGBA", (139,200), color = (0,0,0,0))
        background_delete_frame = Image.new("RGBA", (221,313), color = (0,0,0,0))
        background_delete_frame.alpha_composite(icon,(-3,-3))
        maska = await git.maska_raill_charter_list_right
        background.paste(background_delete_frame.resize((139,200)),maska.convert("L"))

        return background
        
        
    async def edit_avatar(self,icon):
        background = Image.new("RGBA", (177,200), color = (0,0,0,0))
        background_delete_frame = Image.new("RGBA", (177,200), color = (0,0,0,0))
        background_delete_frame.alpha_composite(icon)
        
        maska = await git.maska_raill_charter_list_left
        background.paste(background_delete_frame,(0,0),maska.convert("L"))
        
        return background
    
    async def creat_rank(self, rank):
        name = await utility.ups(rank)
        background = await git.raill_up_charter_list
        background = background.copy()
        
        draw = ImageDraw.Draw(background)
        x = self.t16.getlength(name)
        draw.text((int(10-x/2),1), name, font= self.t16, fill=(255,201,132,255))
        
        return background
    
    async def creat_cards(self,data):
        name = data.name
        level = data.level
        element = data.element
        rarity = data.rarity
        element_icon = await utility.get_element_img(element.capitalize())
        rank = await self.creat_rank(data.rank)
        icon = await pill.get_dowload_img(f"https://api.yatta.top/hsr/assets/UI/avatar/medium/{data.id}.png", size= (177,241))
        self.charter_info[data.id] = {"id": data.id, "name": data.name, "icon": f"https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/icon/avatar/{data.id}.png"}
        background = await git.background_raill_charter_list
        background = background.copy()
        
        if not data.equip is None:
            eqip_level = data.equip.level
            eqip_rank = await self.creat_rank(data.equip.rank) 
            eqip_icon = await pill.get_dowload_img(f"https://api.yatta.top/hsr/assets/UI/equipment/large/{data.equip.id}.png", size= (228,319))
            eqip_rarity = await utility.get_data_charter(f"https://api.yatta.top/hsr/v2/en/equipment/{data.equip.id}")
            lc = await self.edit_lc(eqip_icon)
            level_frame = await git.level_frame_charter_list
            stars_lc = await utility.get_stars_raill(eqip_rarity["rank"])
            background.alpha_composite(lc,(176,24))

        stars_avatar = await utility.get_stars_raill(rarity)
        avatar, shadow = await asyncio.gather(self.edit_avatar(icon), git.raill_shadow_charter_list)

        background.alpha_composite(avatar,(0,24))
        background.alpha_composite(rank,(3,154))
        background.alpha_composite(stars_avatar,(1,197))
        background.alpha_composite(shadow,(176,24))
        background.alpha_composite(element_icon.resize((36,36)),(0,24))
        
        
        
        draw = ImageDraw.Draw(background)
        x = self.t16.getlength(name)
        draw.text((int(158-x/2),3), name, font= self.t16, fill=(255,255,255,255))
        
        draw.text((5,178), f"LVL: {level}", font= self.t18, fill=(0,0,0,0))
        draw.text((6,178), f"LVL: {level}", font= self.t18, fill=(255,255,255,255))
        if not data.equip is None:
            
            background.alpha_composite(eqip_rank,(182,154))
            background.alpha_composite(stars_lc,(182,197))
            background.alpha_composite(level_frame,(180,176))
            draw.text((181,178), f"LVL: {eqip_level}", font= self.t18, fill=(0,0,0,0))
            draw.text((182,178), f"LVL: {eqip_level}", font= self.t18, fill=(255,255,255,255))
        
        self.count[element.lower()] += 1
        if rarity == 5:
            rarity = "five"
        else:
            rarity = "four"
            
        self.count[rarity] += 1
        
        
        return {"id": data.id, "card": background}
        
        
    
    async def start(self, character_id = None):   
        await git_file.change_Font(1)
        self.t16 = await pill.get_font(16)
        self.t18 = await pill.get_font(18)
        if character_id is None:
            card = await asyncio.gather(*[self.creat_cards(key) for key in self.data])
        else:
            for key in self.data:
                if key.id == int(character_id):
                    card = await self.creat_cards(key)
                    return {"count": self.count, "card": card["card"], "icon": [card], "character": self.charter_info}
        
        images_per_row = 6
        spacing = 20
        image_size = (225, 160)

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

            background.alpha_composite(image["card"].copy().resize((225,160)), (x, y))
                
        return {"count": self.count, "card": background, "icon": card, "character": self.charter_info}