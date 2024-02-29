# GenshinPyRail
A module that allows you to create cards for your projects based on the games Honkai Star Rail and Genshin Impact

### Install:
```
pip install genshinpyrail
```

### Usage example:
``` python
from genshinpyrail import genshinpyrail
import asyncio

cookie = {"ltuid_v2": YOU_ltuid_v2, "ltoken_v2": "YOU_ltoken_v2", "ltmid_v2": "YOU_ltmid_v2"}
module = genshinpyrail.GenPyRail(cookie, "en")

async def main():
    client = await module.set_by_uid(700649319)
    print(client.game)
    print(client.uid)
    print(client.hoyolab_id)
    help = await client.get_ascension(character_id= 1306)
    help.card.show()


asyncio.run(main())
```

> [!WARNING]
> The module is still in development and beta testing, there is no normal documentation, so if you want to find out what this module can do, open this file: [HELP](https://github.com/DEViantUA/GenshinPyRail/blob/main/genshinpyrail/src/data/help.json) Well, or open the code: [genshinpyrail.py](https://github.com/DEViantUA/GenshinPyRail/blob/main/genshinpyrail/genshinpyrail.py)
