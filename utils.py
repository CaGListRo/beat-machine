import os
import pygame as pg


def load_image(img_name: str) -> pg.Surface:
    return pg.image.load("images/" + img_name + ".png")


def scale_image(image: str, scalefactor: float) -> pg.Surface:
    return pg.transform.scale(image, (int(image.get_width() * scalefactor), int(image.get_height() * scalefactor)))

def create_beat_button_pattern(program: object):
    beat_button_pattern = []
    for i in range(4):
        help_list = []
        for j in range(4):
            for k in range(4):
                b_type = "button1" if k == 0 else "button234"
                help_list.append(Button(prog=program, button_type=b_type, pos=(i, j + k), mirror=False, activatable=True))
        beat_button_pattern.append(help_list)
    return beat_button_pattern

class Button:
    def __init__(self, prog: object, button_type: str, pos: tuple, mirror: bool = False, activatable: bool = False) -> None:
        self.prog: object = prog
        self.button_type: str = button_type
        self.pos: tuple = pos
        self.active: bool = True if self.button_type == "stop" else False
        self.activatable = activatable
        if self.activatable:
            if not self.active:
                asset_string = f"{self.button_type}/inactive"
            else:
                asset_string = f"{self.button_type}/active"
        else:
            asset_string = self.button_type
        self.image: pg.image = self.prog.assets[asset_string]
        self.rect: pg.rect = self.image.get_rect(center=self.pos)
        self.clicked: bool = False

    def is_active(self) -> bool:
        return self.active
    
    def check_collision(self):
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[0]:
                self.clicked = True
            else:
                self.clicked = False
            if not pg.mouse.get_pressed()[0] and self.clicked:
                if self.activatable:
                    self.active = not self.active
                else:
                    return True
                self.clicked = False
                
        else:
            self.clicked = False

    def render(self, surf) -> None:
        surf.blit(self.image, self.pos)

        