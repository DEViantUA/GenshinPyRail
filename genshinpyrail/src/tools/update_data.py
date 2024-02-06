# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

import aiohttp
import json

from pathlib import Path

_PATH = Path(__file__).parent.parent

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def fetch_monster_info(lang, key):
    url = f"https://api.ambr.top/v2/{lang}/monster/{key}"
    return await fetch_data(url)

async def process_and_save_to_json(lang):

    print(f"Start creating/updating monster_{lang}.json file")
    main_url = f"https://api.ambr.top/v2/{lang}/monster"
    data = await fetch_data(main_url)

    result = {}

    try:
        with open(f"{_PATH}/data/ascension/monster_{lang}.json", "r", encoding="utf-8") as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = {}
    
    entry_keys = None
    for key in data["data"]["items"]:
        if key not in existing_data:
            monster_info = await fetch_monster_info(lang, key)
            for entr in monster_info["data"]["entries"]:
                if monster_info["data"]["entries"][entr]["reward"]:
                    entry_keys = monster_info["data"]["entries"][entr]["reward"]
                    break

        if entry_keys: 
            monster_dict = {
                key: {
                    "id": key,
                    "name": data["data"]["items"][key]["name"],
                    "icon": f"https://api.ambr.top/assets/UI/monster/{data['data']['items'][key]['icon']}.png",
                    "reward": [entry for entry in entry_keys]
                }
            }
            result.update(monster_dict)

    existing_data.update(result)

    with open(f"{_PATH}/data/ascension/monster_{lang}.json", "w", encoding="utf-8") as file:
        json.dump(existing_data, file, indent=2, ensure_ascii = False)

    print(f"End creating/updating monster_{lang}.json file")