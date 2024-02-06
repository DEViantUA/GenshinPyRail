# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.


import json
import asyncio

from PIL import Image,ImageDraw
from ...tools import utility, pill, git_file, update_data
from pathlib import Path

git = git_file.ImageCache()

_DATA =  Path(__file__).parent.parent.parent

positionMarker = [120, 202, 277, 359]

positionsProf = [283, 866, 1492, 2078]

positionsUsing = [436, 1025, 1643, 2229]

positionsCards = [(115, 442), (699, 442), (1328, 442), (1926, 442)]

class Creat:
    def __init__(self, data, info, uid) -> None:
        self.info = info
        self.data = data
        self.uid = uid
        self.result = {
            "action_card": {"value": info.action_cards, "max": info.total_action_cards},
            "character_card": {"value": info.character_cards, "max": info.total_character_cards},
            "information": {"uid": uid, "name": info.nickname, "lvl": info.level, "lang": utility.convertor_lang_swapped.get(info.lang, "en")},
            "win": 0,
            "card": None
        }
    
    async def creat_background(self):
        
        uid = f"UID: {self.uid}"
        name = self.info.nickname
        lvl = self.info.level
        
        cc = self.info.character_cards
        ccm = self.info.total_character_cards
        
        ac = self.info.action_cards
        acm = self.info.total_action_cards
        
        
        background = await git.bg_tcg
        self.background = background.copy()
        
        draw = ImageDraw.Draw(self.background)
        
        x = self.t69.getlength(name)
        draw.text((int(542 - x / 2), 75), name, font= self.t69 , fill=(238, 230, 212, 255))
        
        x = self.t28.getlength(uid)
        draw.text((int(543 - x / 2), 153), uid, font=self.t28, fill=(255, 238, 201, 255))

        x = self.t115.getlength(str(lvl))
        draw.text((int(215 - x / 2), 75),str(lvl),font=self.t115,fill=(100, 76, 62, 255))
        draw.text((int(216 - x / 2), 75),str(lvl),font=self.t115,fill=(255, 238, 201, 255))

        draw.text((1763, 125), f"{cc}/{ccm}", font=self.t22, fill=(97, 93, 102, 255))

        draw.text((2303, 125), f"{ac}/{acm}", font= self.t22, fill=(97, 93, 102, 255))

    async def generate_card(self,link, types, skills, health=0):
        bgAll = Image.new("RGBA", (450,772), (0,0,0,0))

        if types == "CardTypeCharacter":
            frame = await git.frame_charters_tcg
        else:
            frame = await git.frame_others_tcg

        image = await pill.get_dowload_img(link, size= (412, 712))
        i = 0
        for key in skills:
            marker = await git.icons_stats_tcg
            marker = marker.copy()
            icons = await pill.get_dowload_img(key, (26, 30))
            marker.alpha_composite(icons, (22, 18))
            bgAll.alpha_composite(marker, (positionMarker[i], 702))
            i += 1
        bgAll.alpha_composite(image, (32, 0))
        bgAll.alpha_composite(frame, (0, 0))
        if health == 0:
            pass
        else:
            text = ImageDraw.Draw(bgAll)
            x = self.t67.getlength(str(health))
            text.text((int(58 - x / 2), 647),str(health),font=self.t67,fill=(255, 255, 255, 255))

        return bgAll
    
    async def add_cards(self):
        showsId = [key.id for key in self.info.cards]
        winsList,countWins,v = 0,0,0
       
        draw = ImageDraw.Draw(self.background)
        
        for key in self.data:
            if key.proficiency != 0:
                winsList += key.proficiency
                countWins += 1
            if key.id in showsId:
                usages = str(key.usages)
                proficiency = str(key.proficiency)
                if hasattr(key, "health"):
                    card = await self.generate_card(key.image, key.type.value, key.image_tags, key.health)
                else:
                    card = await self.generate_card(key.image, key.type.value, key.image_tags)

                x = self.t22.getlength(proficiency)
                draw.text((int(positionsProf[v] - x / 2), 371),proficiency,font=self.t22,fill=(204, 219, 239, 255))

                x = self.t22.getlength(usages)
                draw.text((int(positionsUsing[v] - x / 2), 371),usages,font=self.t22,fill=(192, 173, 141, 255))
                
                self.background.alpha_composite(card, positionsCards[v])
                
                v += 1
        wins = int(winsList / 3)
        x = self.t22.getlength(str(wins))
        draw.text((int(1297 - x / 2), 125),str(wins),font=self.t22,fill=(97, 93, 102, 255))
        
        self.result["win"] = wins
        self.result["card"] = self.background

    async def start(self):
        await git_file.change_Font(0)
        self.t67 = await pill.get_font(67)
        self.t69 = await pill.get_font(69)
        self.t28 = await pill.get_font(28)
        self.t22 = await pill.get_font(22)
        self.t115 = await pill.get_font(115)

        await self.creat_background()
        await self.add_cards()
                
        return self.result