# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

import aiohttp
import asyncio
import re

from ...tools import utility, model, git_file, pill
from PIL import ImageDraw,Image


cashe = {}

charter_url = "https://api.yatta.top/hsr/v2/{lang}/avatar/{ids}"
charter_url_icon = "https://api.yatta.top/hsr/assets/UI/avatar/large/{ids}.png"

items_link = "https://api.yatta.top/hsr/v2/{lang}/item/{ids}"
items_link_icon = "https://api.yatta.top/hsr/assets/UI/item/{ids}.png"

of = git_file.ImageCache()


async def name_edit(text):
    replaced_text = re.sub(r'\{F#[^}]*\}', ' Hero', text)
    replaced_text = re.sub(r'\{M#[^}]*\}', '', replaced_text)
    replaced_text = re.sub(r'\{M#[^}]*\}', '', replaced_text)    
    replaced_text = replaced_text.replace('\\n', '')
    replaced_text = replaced_text.format(NICKNAME = "Trailblazer")

    return await utility.remove_html_tags(replaced_text)


async def material_icon(x):
    if x == 1:
        icon = await of.material_1
    elif x == 2:
        icon = await of.material_2
    elif x == 3:
        icon = await of.material_3
    elif x == 4:
        icon = await of.material_4
    else:
        icon = await of.material_5
    
    return icon.copy()


async def creat_matterial(data):
    icon = await pill.get_dowload_img(data.icon)
    bg = await material_icon(data.rank)
    bg.alpha_composite(icon,(0,7))
    font = await pill.get_font(25)
    d = ImageDraw.Draw(bg)
    x = int(font.getlength(str(data.value))/2)
    d.text((64- x, 153), str(data.value), font=font, fill=(255,255,255,255))
    
    return bg


class Creat:
    def __init__(self, data) -> None:
        self.data = data
        
    
    async def creat_background(self):
        bg = await of.background
        shadow = await of.shadow
        frame = await of.background_frame
        logo = await of.logo
        mask = await of.maska
        bg = bg.copy().convert("RGBA")
        bg_image = Image.new('RGBA', (1588,1272), color=(0, 0, 0, 0))
        bg_image_two = bg_image.copy()
        image = await pill.get_dowload_img(self.data.icon, size= (1860,1860))
        bg_image.alpha_composite(image,(-550,-294))
        bg_image_two.paste(bg_image.convert("RGBA"),(0,0),mask.convert("L"))
        bg.alpha_composite(bg_image_two)
        bg.alpha_composite(shadow)
        bg.alpha_composite(frame,(580,0))
        bg.alpha_composite(logo)
        
        self.bg = bg
        
    async def creat_description(self):
        bg_description = await of.desc_frame
        bg_description = bg_description.copy()
        desc_text = await pill.create_image_text(await name_edit(self.data.description), 20, max_width=496, color=(255, 255, 255, 255))
        if desc_text.size[1] > 151:
            new_height = 151
            width_percent = (new_height / float(desc_text.size[1]))
            new_width = int((float(desc_text.size[0]) * float(width_percent)))
            desc_text = desc_text.resize((new_width, new_height))
        y = int(89-desc_text.size[1]/2)
        bg_description.alpha_composite(desc_text,(13,y))
        self.bg_description = bg_description
    
    async def creat_stats(self):
        self.name = await pill.create_image_text(self.data.name, 42, max_width=474, max_height=66, color=(255, 255, 255, 255))
    
    async def creat_path(self):
        icon = await utility.get_path_img(self.data.path)
        bg_path = await of.path_frame
        bg_path = bg_path.copy()
        bg_path.alpha_composite(icon.resize((56,57)),(10,9))

        self.path = bg_path
        
    async def creat_element(self):
        icon = await utility.get_element_img(self.data.element)
        bg_element = await of.path_frame
        bg_element = bg_element.copy()
        bg_element.alpha_composite(icon.resize((56,57)),(10,9))

        self.element = bg_element
        
    async def get_stars_icon(self):
        if self.data.rank == 4:
            self.stars =  await of.stars_4
        else:
            self.stars =  await of.stars_5
    
    async def creat_matterial(self):
        bg_stats = await of.matterial_frame
        bg_stats = bg_stats.copy()
        
        x = 23   
        for key in self.data.charter_upgrade:
            icon = await creat_matterial(self.data.charter_upgrade[key])
            bg_stats.alpha_composite(icon,(x,94))
            x += 173
            
        x = 23
        y = 401
        for i, key in enumerate(self.data.skills):
            icon = await creat_matterial(self.data.skills[key])
            bg_stats.alpha_composite(icon,(x,y))
            x += 173
            if i == 4:
                x = 23
                y = 653
            
        
        self.bg_stats = bg_stats
    
    async def build(self):
        text_charter = await of.text_charter
        self.bg.alpha_composite(self.bg_description, (0,1051))
        y = int(1009-self.name.size[1]/2)
        name_recolor_image = await pill.recolor_image(self.name,(0,0,0))
        self.bg.alpha_composite(name_recolor_image, (14,y+1))
        self.bg.alpha_composite(self.name, (15,y))
        self.bg.alpha_composite(self.stars, (276,893))
        self.bg.alpha_composite(self.path, (468,877))
        self.bg.alpha_composite(self.element, (468,964))
        self.bg.alpha_composite(text_charter, (797,59))
        self.bg.alpha_composite(self.bg_stats, (657,217))
        
        return self.bg
        
    async def start(self):
        task = [
            self.creat_background(),
            self.creat_description(),
            self.creat_stats(),
            self.creat_path(),
            self.creat_element(),
            self.get_stars_icon(),
            self.creat_matterial(),
        ]
        await asyncio.gather(*task)
        
        return await self.build()
        
async def get_data(url):
    async with aiohttp.ClientSession() as session:
        if not url in cashe:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        cashe[url] = data
                        return data
                    else:
                        print(f"Error: {response.status}")
                        return None
            except aiohttp.ClientError as e:
                print(f"Error: {e}")
                return None
        else:
            return cashe[url]

class Material:
    def __init__(self,ch_id, lang):
        self.ch_id = ch_id
        self.lang = utility.convertor_lang_swapped.get(lang, "en")
        self.charter_traces = {"mainSkills": {}, "subSkills": {}}
        self.full_skills = {}
        self.data_cards = {"name": "",
                      "id": "",
                      "rank": "",
                      "description": "",
                      "icon":"",
                      "path": "",
                      "element": "",
                      "charter_upgrade": {},
                      "skills": {},
                      "card": None
                      }

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass
    
    async def collection(self):
        await git_file.change_Font(1)
        data = await get_data(charter_url.format(lang = self.lang,ids = self.ch_id))
        if data is None:
            return None
               
        self.data_cards["id"] = data["data"]["id"]
        self.data_cards["rank"] = data["data"]["rank"]
        self.data_cards["name"] = data["data"]["name"]
        self.data_cards["path"] = data["data"]["types"]["pathType"]["id"] 
        self.data_cards["element"] = data["data"]["types"]["combatType"]["id"] 
        self.data_cards["description"] = data["data"]["fetter"]["description"]
        self.data_cards["icon"] = charter_url_icon.format(ids = data["data"]["icon"])


        for key in data["data"]["upgrade"]:
            if key["level"] != 6:
                for keys in key["costItems"]:
                    if not keys in self.data_cards["charter_upgrade"]:
                        data_items = await get_data(items_link.format(lang = self.lang,ids = keys))
                        self.data_cards["charter_upgrade"][keys] = {"value": key["costItems"][keys], "icon": items_link_icon.format(ids = data_items["data"]["icon"]), "rank": data_items["data"]["rank"]}
                    else:
                        self.data_cards["charter_upgrade"][keys]["value"] += key["costItems"][keys]

        mainSkills = data["data"]["traces"]["mainSkills"]
        subSkills = data["data"]["traces"]["subSkills"]
        
        for key in mainSkills:
            for index in mainSkills[key]["promote"]:
                if mainSkills[key]["promote"][index]["costItems"] is None:
                    continue
                else:
                    for z in mainSkills[key]["promote"][index]["costItems"]:
                        if not z in self.data_cards["skills"]:
                            data_items = await get_data(items_link.format(lang = self.lang,ids = z))
                            self.data_cards["skills"][z] = {"value": mainSkills[key]["promote"][index]["costItems"][z], "icon": items_link_icon.format(ids = data_items["data"]["icon"]), "rank": data_items["data"]["rank"]}
                        else:
                            self.data_cards["skills"][z]["value"] += mainSkills[key]["promote"][index]["costItems"][z]
                          
        for key in subSkills:
            for index in subSkills[key]["promote"]:
                if subSkills[key]["promote"][index]["costItems"] is None:
                    continue
                else:
                    for z in subSkills[key]["promote"][index]["costItems"]:
                        if not z in self.data_cards["skills"]:
                            data_items = await get_data(items_link.format(lang = self.lang, ids = z))
                            self.data_cards["skills"][z] = {"value": subSkills[key]["promote"][index]["costItems"][z], "icon": items_link_icon.format(ids = data_items["data"]["icon"]), "rank": data_items["data"]["rank"]}
                        else:
                            self.data_cards["skills"][z]["value"] += subSkills[key]["promote"][index]["costItems"][z]
                            
        sorted_items =  sorted(self.data_cards["skills"].items(), key=lambda x: int(x[0]) if x[0].isdigit() else 10**6)
        self.data_cards["skills"] = {key: value for key, value in sorted_items}

        sorted_items =  sorted(self.data_cards["charter_upgrade"].items(), key=lambda x: int(x[0]) if x[0].isdigit() else 10**6)
        self.data_cards["charter_upgrade"] = {key: value for key, value in sorted_items}
        
        self.data_cards = model.StarRaillAscensionInfo(**self.data_cards)
        
        card = await Creat(self.data_cards).start()
            
        
        return {"lang": self.lang, "id": self.ch_id, "card": card, "data": self.data_cards}