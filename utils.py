import os
import pygame as pg


def load_image(img_name: str) -> pg.Surface:
    return pg.image.load("images/" + img_name + ".png")


def scale_image(image: str, scalefactor: float) -> pg.Surface:
    return pg.transform.scale(image, (int(image.get_width() * scalefactor), int(image.get_height() * scalefactor)))


class Button:
    def __init__(self, prog: object, type: str, mirror: bool = False, activatable: bool = False) -> None:
        self.prog = prog
        self.type = type
        self.active = True if self.type == "stop" else False
        if activatable:
            if not self.active:
                asset_string = f"{self.type}/inactive"
        # self.image = self.prog.assets[]