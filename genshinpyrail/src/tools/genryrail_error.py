# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

class Error(BaseException):
    def __init__(self, code, message):
        super().__init__(f"[{code}] {message}")
        self.code = code
        self.message = message

class GenRailError(Error):
    pass