# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

import genshin

from abc import ABCMeta
from .src.tools.genryrail_error import GenRailError
from .src.tools.utility import convertor_lang
from .src.tools import model


from .src.generation.genshin import generator_tcg_info
from .src.generation.genshin import generator_tcg as genshin_tcg
from .src.generation.genshin import generator_ascension as genshin_ascension
from .src.generation.genshin import generator_character_list as genshin_character_list

from .src.generation.honkai import generator_ascension as honkai_ascension
from .src.generation.honkai import generator_character_list as honkai_character_list

class GenPyRail(metaclass=ABCMeta):
        
    def __init__(self,cookies,lang = "en",**kwargs) -> None:
        
        """The main class that sets the basic settings

        Args:
            cookies (dict): Your Cookies
            lang (str): The language you want to use. Defaults to "en".
        """
        
        self.lang = convertor_lang.get(lang,lang)
        self.cookies = cookies
        self.client = genshin.Client(self.cookies, lang = self.lang)
        self.hoyolab_id = self.cookies.get("ltuid_v2", self.cookies.get("ltuid", None))
    
    
    async def help(self):
        """Returns a list of available functions for a given class and their descriptions

        Returns:
            BaseModel: Return BaseModel pydantic with function information
        """
        if self.game:
            data =  [
                {"function": "get_user", "desc": "Вернет инфомацию о юзере"},
            ]
            return model.HelpGenPyRail(help = data)
    
    async def set_lang(self,lang):
        
        """Changes/Sets client language

        Args:
            lang (str): The language you want to use.
        """
        
        self.lang = convertor_lang.get(lang,lang)
    
    async def setting_client(self,cookies):
        
        """Changing the client with new parameters

        Args:
            cookies (dict): Your Cookies
            lang (str): The language you want to use.
        """
        
        if not cookies is None:
            if lang is None:
                lang = convertor_lang.get(self.lang,self.lang)
            else:
                self.lang = convertor_lang.get(lang,lang)
                
            self.client = genshin.Client(cookies, lang = lang)
        
    async def set_by_uid(self, uid, cookies = None, lang = None):
        
        """Returns classes for working with generations depending on the game in which the UID is used

        Args:
            uid (int): uid of the user in the game
            cookies (dict, optional): Use if you want to change cookies. Defaults to None.
            lang (str, optional): The language you want to use. Defaults to None.

        Raises:
            GenRailError: Returns an error

        Returns:
            Class GenshinUser: Class for working with generations belonging to the category of the game Genshin
            Class StarRaillUser: Class for working with generations belonging to the category of the game Star Rail
        """
        
        await self.setting_client(cookies,lang)
            
        accounts = await self.client.get_game_accounts()
        
        for key in accounts:
            if key.uid == uid:
                if "hk4e" in key.game_biz:
                    class_data =  GenshinUser(cookies=self.cookies, lang=self.lang, game = genshin.Game.GENSHIN, uid = key.uid)
                elif "hkrpg" in key.game_biz:
                    class_data =  StarRaillUser(cookies=self.cookies, lang=self.lang, game = genshin.Game.STARRAIL, uid = key.uid)
                else:
                    raise GenRailError("1008", "This game is not supported.")

                break
            
        class_data.uid = key.uid
        
        return class_data
        
    async def full_set_account(self, cookies = None, lang = None):
        
        """Returns all user accounts

        Args:
            cookies (dict, optional): Use if you want to change cookies. Defaults to None.
            lang (str, optional): The language you want to use. Defaults to None.

        Yields:
            Class GenshinUser: Class for working with generations belonging to the category of the game Genshin
            Class StarRaillUser: Class for working with generations belonging to the category of the game Star Rail
        """
        
        await self.setting_client(cookies,lang)
        accounts = await self.client.get_game_accounts()
        for key in accounts:
            if "hkrpg" in key.game_biz or "hk4e" in key.game_biz:
                if "hk4e" in key.game_biz:
                    yield GenshinUser(cookies=self.cookies, lang=self.lang, game = genshin.Game.GENSHIN, uid = key.uid)
                elif "hkrpg"in key.game_biz:
                    self.client.game = genshin.Game.GENSHIN
                    yield StarRaillUser(cookies=self.cookies, lang=self.lang, game = genshin.Game.STARRAIL, uid = key.uid)
                    
    async def set_left_user(self, uid, hoyolab_id = 0, games = "genshin"):
        """If you want to get information about another user without his cookie

        Args:
            uid (int): uid of the user in the game
            hoyolab_id (int, optional): user ID on HoYoLab. Defaults to 0.
            games (str, optional): the game to which uid, genshin or star rail belongs. Defaults to "genshin".

        Returns:
            Class GenshinUser: Class for working with generations belonging to the category of the game Genshin
            Class StarRaillUser: Class for working with generations belonging to the category of the game Star Rail
        """
        
        self.hoyolab_id = hoyolab_id
        if games == "genshin":
            return GenshinUser(cookies=self.cookies, lang=self.lang, game = genshin.Game.GENSHIN, uid = int(uid))
        else:
            return StarRaillUser(cookies=self.cookies, lang=self.lang, game = genshin.Game.STARRAIL, uid = int(uid))


class GenshinUser(GenPyRail):
    def __init__(self, game, uid, **kwargs) -> None:
        super().__init__(**kwargs)
        self.game = game
        self.uid = uid
        self.client.game = game
    
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, *args):
        pass
    
    async def get_character_list(self, uid = None, character_id = None):
        """Creates an image with all of the player's Genshin characters

        Args:
            uid (str, optional): Player UID To get information about another account. Defaults to None.
            character_id (int, optional): Character ID Specify if you want to receive only 1 character card. Defaults to None.

        Returns:
            GenshinCharterList: Class containing information about the quantity and finished cards
        """
        
        if uid is None:
            uid = self.uid
        data = await self.client.get_genshin_characters(uid)
        
        data = await genshin_character_list.Creat(data).start(character_id)
        
        return model.GenshinCharterList(**data)
    
        
    async def get_ascension(self, character_id):
        """Generates a card with materials for character elevation

        Args:
            character_id (int): Character ID

        Returns:
            GenshinAscension: Model: Genshin Ascension containing information and finished image
        """
        data = await genshin_ascension.Creat(character_id, self.lang).start()
        
        return model.GenshinAscension(**data)
    
    async def get_tcg(self):
        """Generates a card with a view of the user's TCG cards and his statistics

        Returns:
            GenshinTCG Model: Contains information about statistics and cards
        """
        
        info = await self.client.get_genshin_tcg_preview(self.uid)
        data = await self.client.genshin_tcg(self.uid)
        data = await genshin_tcg.Creat(data,info, self.uid).start()
        
        return model.GenshinTCG(**data)
    
    async def get_tcg_info(self, сard_id):
        """Generates an image with TCG card information

        Args:
            сard_id (int): TCG Card ID

        Returns:
            GenshinInfoTCG Model: Contains information and card
        """
        data = await generator_tcg_info.Creat(сard_id, self.lang).start()
        
        return model.GenshinInfoTCG(**data)
        

class StarRaillUser(GenPyRail):
    def __init__(self, game, uid,  **kwargs) -> None:
        super().__init__(**kwargs)
        self.game = game
        self.uid = uid
        self.client.game = game
    
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, *args):
        pass
    
    
    async def get_character_list(self, uid = None, character_id = None):
        """Creates an image with all of the player's Star Rail characters

        Args:
            uid (str, optional): Player UID To get information about another account. Defaults to None.
            character_id (int, optional): Character ID Specify if you want to receive only 1 character card. Defaults to None.

        Returns:
            StarRaillCharterList: Class containing information about the quantity and finished cards
        """
        
        if uid is None:
            uid = self.uid
        data = await self.client.get_starrail_characters(uid)
        data = await honkai_character_list.Creat(data.avatar_list).start(character_id)
        return model.StarRaillCharterList(**data)
    
    async def get_ascension(self, character_id):
        """Generates a card with materials for character elevation

        Args:
            character_id (int): Character ID

        Returns:
            StarRaillAscension: Model: StarRaill Ascension containing information and finished image
        """
        data = await honkai_ascension.Material(character_id, self.lang).collection()
        
        return model.StarRaillAscension(**data)