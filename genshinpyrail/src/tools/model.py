# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from typing import List
from pydantic import BaseModel,root_validator
from typing import List ,Optional,Union,Dict
from PIL import Image
from .utility import get_data_charter

class FunctionInfo(BaseModel):
    function: str
    desc: str

class HelpGenPyRail(BaseModel):
    help: List[FunctionInfo]


class GenshinAscension(BaseModel):
    lang: Optional[str]
    id: Optional[int]
    card: Optional[Image.Image]
    class Config:
        arbitrary_types_allowed = True
        
    async def get_info(self):
        data = await get_data_charter(f"https://api.ambr.top/v2/{self.lang}/avatar/{self.id}")
        
        return data



class CharterUpgradeItem(BaseModel):
    value: Optional[int]
    icon: Optional[str]
    rank: Optional[int]

class SkillItem(BaseModel):
    value: Optional[int]
    icon: Optional[str]
    rank: Optional[int]

class StarRaillAscensionInfo(BaseModel):
    name: Optional[str]
    id: Optional[str]
    rank: Optional[int]
    description: Optional[str]
    icon: Optional[str]
    path: Optional[str]
    element: Optional[str]
    charter_upgrade: Optional[Dict[str, CharterUpgradeItem]]
    skills: Optional[Dict[str, SkillItem]]

class StarRaillAscension(BaseModel):
    lang: Optional[str]
    id: Optional[int]
    card: Optional[Image.Image]
    data: Optional[StarRaillAscensionInfo]

    class Config:
        arbitrary_types_allowed = True
    
    def __str__(self):
        return f"lang='{self.lang}' id={self.id} card={self.card}"
        
    async def get_info(self):
        return self.data
    

class Icon(BaseModel):
    id: Optional[int]
    card: Optional[Image.Image]
    class Config:
        arbitrary_types_allowed = True

class CountCharterList(BaseModel):
    name: Optional[str]
    value: Optional[int]

class GenshinCharterList(BaseModel):
    count: Dict[str, int]
    card: Optional[Image.Image]
    icon: List[Icon]
    character: Optional[Dict[int,dict]]
    class Config:
        arbitrary_types_allowed = True
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.count = [CountCharterList(name=key, value=value) for key, value in self.count.items()]
    
    
    def __str__(self):
        return f"count={self.count} card={self.card}"
    
    def get_info_character(self, character_id = None):
        if character_id is None:
            return self.character
        
        for key in self.character:
            if int(key.id) == int(character_id):
                return self.character[key]
    
    def get_card(self, character_id):
        for key in self.icon:
            if int(key.id) == int(character_id):
                return key
            
class StarRaillCharterList(BaseModel):
    count: Dict[str, int]
    card: Optional[Image.Image]
    icon: List[Icon]
    character: Optional[Dict[int,dict]]

    class Config:
        arbitrary_types_allowed = True
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.count = [CountCharterList(name=key, value=value) for key, value in self.count.items()]
    
    
    def __str__(self):
        return f"count={self.count} card={self.card}"
    
    def get_info_character(self, character_id = None):
        if character_id is None:
            return self.character
        
        for key in self.character:
            if int(key.id) == int(character_id):
                return self.character[key]
            
     
    def get_card(self, character_id):
        for key in self.icon:
            if int(key.id) == int(character_id):
                return key

class ActionCard(BaseModel):
    value: Optional[int]
    max: Optional[int]

class CharacterCard(BaseModel):
    value: Optional[int]
    max: Optional[int]

class Information(BaseModel):
    uid: Optional[int]
    name: Optional[str]
    lvl: Optional[int]
    lang: Optional[str]

class GenshinTCG(BaseModel):
    action_card: Optional[ActionCard]
    character_card: Optional[CharacterCard]
    information: Optional[Information]
    win: Optional[int]
    card: Optional[Image.Image]
    class Config:
        arbitrary_types_allowed = True
    
    async def get_info_tcg(self,tcg_id):
        data = await get_data_charter(f"https://api.ambr.top/v2/{self.information.lang}/gcg/{tcg_id}")
        return data

class GenshinInfoTCG(BaseModel):
    id: Optional[int]
    icon: Optional[str]
    type: Optional[str]
    card: Optional[Image.Image]
    class Config:
        arbitrary_types_allowed = True