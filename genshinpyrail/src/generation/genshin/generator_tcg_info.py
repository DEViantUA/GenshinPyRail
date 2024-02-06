# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

import asyncio

from ...tools import utility, pill, git_file
from PIL import Image,ImageDraw

git = git_file.ImageCache()


async def open_energy(x):
    if x == 1:
        return await git.tcg_stars_1
    elif x == 2:
        return await git.tcg_stars_2
    else:
        return await git.tcg_stars_3


async def open_dice(element):
    if element == "cryo":
        return await git.CostTypeCryo
    elif element == "dendro":
        return await git.CostTypeDenro
    elif element == "anemo":
        return await git.CostTypeAnemo
    elif element == "electro":
        return await git.CostTypeElectro
    elif element == "hydro":
        return await git.CostTypeHydro
    elif element == "pyro":
        return await git.CostTypePyro
    elif element == "geo":
        return await git.CostTypeGeo
    elif element == "void":
        return await git.CostTypeVoid
    elif element == "same":
        return await git.CostTypeSame
    else:
        return await git.CostTypeArcane

class Creat:
    def __init__(self, character_id, lang) -> None:
        self.character_id = character_id
        self.lang = utility.convertor_lang_swapped.get(lang)
    
    async def dice_creat(self,icon,key,color):
        if key != "GCG_COST_DICE_LEGEND":
            draw = ImageDraw.Draw(icon)
            x = self.t48.getlength(str(self.data["props"][key]))
            draw.text((int(52-x/2),27), str(self.data["props"][key]), font= self.t48, fill = color)
            
        self.background_card.alpha_composite(icon,(0,543))
        
    async def dice_const_creat(self,value,icon,key,color):
        if key != "GCG_COST_DICE_LEGEND":
            draw = ImageDraw.Draw(icon)
            x = self.t48.getlength(str(value))
            draw.text((int(52-x/2),27), str(value), font= self.t48, fill = color)
        
        return icon
    
    async def creat_props(self):
        for key in self.data["props"]:
            if key == "GCG_PROP_HP":
                icon = await git.hp_icon
                icon = icon.copy()
                draw = ImageDraw.Draw(icon)
                x = self.t48.getlength(str(self.data["props"][key]))
                draw.text((int(52-x/2),37), str(self.data["props"][key]), font= self.t48, fill=(247,236,217,255))
                self.background_card.alpha_composite(icon,(17,0))
            elif key in ["GCG_PROP_ENERGY","GCG_COST_ENERGY"]:
                icon = await open_energy(self.data["props"][key])
                self.background_card.alpha_composite(icon,(13,227))
            elif "GCG_COST_DICE_" in key:
                DICE = key.replace("GCG_COST_DICE_","")
                icon = await open_dice(DICE.lower())
                icon = icon.resize((104,104)).convert("RGBA").copy()
                if key == "GCG_COST_DICE_SAME":
                    await self.dice_creat(icon,key,(39,41,46,255))
                else:
                    await self.dice_creat(icon,key,(239,230,216,255))
                    
    async def creat_cost(self,data):
        icons = []
        if data:
            for key in data:
                if key in ["GCG_PROP_ENERGY","GCG_COST_ENERGY"]:
                    icon = await git.tcg_cost_icon
                    icon = icon.copy()
                    draw = ImageDraw.Draw(icon)
                    x = self.t48.getlength(str(data[key]))
                    draw.text((int(34-x/2),8), str(data[key]), font= self.t42, fill = (39,41,46,255))
                    #draw.text((int(36-x/2),8), str(data[key]), font= self.t42, fill = (39,41,46,255))
                    #draw.text((int(34-x/2),8), str(data[key]), font= self.t42, fill = (255,255,255,255))
                    icons.append(icon)
                elif "GCG_COST_DICE_" in key:
                    DICE = key.replace("GCG_COST_DICE_","")
                    icon = await open_dice(DICE.lower())
                    icon = icon.resize((104,104)).convert("RGBA").copy()
                    if key == "GCG_COST_DICE_SAME":
                       icons.append(await self.dice_const_creat(data[key],icon,key,(39,41,46,255))) 
                    else:
                        icons.append(await self.dice_const_creat(data[key],icon,key,(239,230,216,255)))
        
        return icons
    
    async def creat_cards(self):
        background_card = await git.tcg_background_card
        frame = await git.frame_tcg_card
        self.background_card = background_card.copy()
        icon = await pill.get_dowload_img(f'https://api.ambr.top/assets/UI/gcg/{self.data["icon"]}.png', size= (345,589))
        self.background_card.alpha_composite(icon,(45,32))
        self.background_card.alpha_composite(frame)
        
        if self.data["props"]:
            await self.creat_props()
    
    async def creat_talant(self, data):
        
        if not data["icon"] is None:
            background = await git.talant_bacgkround_tcg
            background = background.copy()
            if data["icon"] == "Skill_E_Alhatham_01_HD":
                data["icon"] = "UI_Icon_Item_Temp"
            icon = await pill.get_dowload_img(f'https://api.ambr.top/assets/UI/{data["icon"]}.png', size=(79,79))
            background.alpha_composite(icon,(19,5))
            x = 106
            y = 38
            max_widtg = 697
            max_height = 55
        else:
            background = await git.big_talant_bacgkround_tcg
            background = background.copy()
            x = 19
            y = 38
            max_height = None
            max_widtg = 784

        draw = ImageDraw.Draw(background)
        draw.text((x,9), data["name"], font= self.t20, fill=(239,230,216,255))
        
        text = await utility.remove_html_tags(utility.replace_values(data["description"], data.get("params", {}), data.get("keywords", {})))
        text = utility.remove_brackets_content(text)
        
        text = await pill.create_image_text(text,14,max_width=max_widtg, max_height = max_height ,color=(255,255,255,255))
        background.alpha_composite(text, (x,y))
        
        cost = await self.creat_cost(data["cost"])
        
        tags_bg = await git.name_tcg_tags
        tags_bg = tags_bg.copy()
        text = ""
        if data["tags"]:
            for i, key in enumerate(data["tags"]):
                if i == 0:
                    text += data["tags"][key]
                else:
                    text += f'/{data["tags"][key]}'
            
            draw_tags = ImageDraw.Draw(tags_bg)
            x = self.t14.getlength(text)
            draw_tags.text((int(96-x/2),0), text, font= self.t14, fill=(198,163,112,255))

            x_name = self.t20.getlength(data["name"])
            if x_name <= 290:
                background.alpha_composite(tags_bg,(340,5))
            else:
                if x_name < 580:
                    background.alpha_composite(tags_bg,(580,5))
        position = [(823,5),(823,48)]
        if len(cost) == 1:
            position = [(823,26)]
        for i,key in enumerate(cost):
            background.alpha_composite(key.resize((36,36)),position[i])
        
        
        return background
    
    async def creat_background(self):
        if len(self.data["talent"]) > 4:
            background = await git.big_tcg_background_info
        else:
            background = await git.tcg_background_info
        self.tcg_background_info = background.copy()
        draw = ImageDraw.Draw(self.tcg_background_info)
        element = False
        
        tags_position = [(857,113),(857,141),(857,169)]
        i = 0
        
        if self.data["tags"]:
            for index, key in enumerate(self.data["tags"]):
                if "GCG_TAG_ELEMENT_" in key:
                    icon = await utility.get_element_genshin_img(key.replace("GCG_TAG_ELEMENT_","").title())
                    self.tcg_background_info.alpha_composite(icon.resize((75,75)),(46,120))
                    element = True
                else:
                    key_title = key.title()
                    if not "Gcg_Tag_Weapon_" in key_title:
                        name = key_title.replace("Slowly", "Card_CombatAction") \
                                        .replace("Nation", "Faction") \
                                        .replace("Talent", "Card_Talent") \
                                        .replace("Artifact", "Card_Relic") \
                                        .replace("Item", "Card_Item") \
                                        .replace("Gcg_Tag_Resonance", "Icon_Item_Temp") \
                                        .replace("Legend", "Card_Legend") \
                                        .replace("Weapon", "Card_Weapon") \
                                        .replace("Camp", "Faction") \
                                        .replace("Place", "Card_Location") \
                                        .replace("Ally","Card_Ally") \
                                        .replace("Food","Card_Food") \
                                        .replace("Gcg_Tag_Faction_Hilichurl", "Icon_Item_Temp")
                                        
                                        
                    else:
                        name = key_title.replace("Pole", "Polearm")
                    icon = await pill.get_dowload_img(f'https://api.ambr.top/assets/UI/UI_{name}.png', size= (26,26))
                    self.tcg_background_info.alpha_composite(icon,tags_position[i])
                    x = self.t20.getlength(str(self.data["tags"][key]))
                    draw.text((int(849-x),tags_position[i][1]), str(self.data["tags"][key]), font= self.t20, fill=(255,255,255,255))
                    i += 1
                if index == 3:
                    break
        
        
                
        if element:
            name = await pill.create_image_text(self.data["name"], 41, max_width= 590,color= (239,230,216,255))
            if name.size[1] > 75:
                name.thumbnail((name.size[0],75))
                self.tcg_background_info.alpha_composite(name,(123,int(190-name.size[1])))
            else:
                self.tcg_background_info.alpha_composite(name,(123,int(175-name.size[1]/2)))
        else:
            name = await pill.create_image_text(self.data["name"], 41, max_width= 590, color= (239,230,216,255))
            if name.size[1] > 75:
                name.thumbnail((name.size[0],75))
                self.tcg_background_info.alpha_composite(name,(46,int(190-name.size[1])))
            else:
                self.tcg_background_info.alpha_composite(name,(46,int(175-name.size[1]/2)))
        
        talent = await asyncio.gather(*[self.creat_talant(self.data["talent"][key]) for index, key in enumerate(self.data["talent"]) if index < 5])
        y = 224
        for key in talent:
            self.tcg_background_info.alpha_composite(key,(30,y))
            y += 106
            
    
    async def build(self):
        if len(self.data["talent"]) > 4:
            self.background = Image.new("RGBA", (1382,877), (0,0,0,0))
            self.background.alpha_composite(self.tcg_background_info,(402,54))
            self.background.alpha_composite(self.background_card,(7,116))
        else:
            self.background = Image.new("RGBA", (1382,782), (0,0,0,0))
            self.background.alpha_composite(self.tcg_background_info,(402,54))
            self.background.alpha_composite(self.background_card,(7,47))
        
    async def start(self):
        self.data = await utility.get_data_charter(f"https://api.ambr.top/v2/{self.lang}/gcg/{self.character_id}")
        self.t48 = await pill.get_font(48)
        self.t42 = await pill.get_font(42)
        self.t20 = await pill.get_font(20)
        self.t14 = await pill.get_font(14)
        await self.creat_cards()
        await self.creat_background()
        await self.build()
        
        return {"id": self.data["id"],  "icon": f'https://api.ambr.top/assets/UI/gcg/{self.data["icon"]}.png', "type": self.data["type"], "card": self.background}