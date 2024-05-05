from elements import Button, SlotLight, Slider
import pygame as pg


def load_image(img_name: str) -> pg.Surface:
    return pg.image.load("images/" + img_name + ".png")

def scale_image(image: str, scalefactor: float) -> pg.Surface:
    return pg.transform.scale(image, (int(image.get_width() * scalefactor), int(image.get_height() * scalefactor)))

def load_sound(file_path: str, sound_name: str) -> pg.mixer:
    return pg.mixer.Sound("sounds/" + file_path + "/" + sound_name + ".wav")

def create_beat_button_pattern(program: object) -> list:
    beat_button_pattern = []
    for i in range(4):
        help_list = []
        for j in range(4):
            for k in range(4):
                b_type = "button1" if k == 0 else "button234"
                help_list.append(Button(prog=program, button_type=b_type, pos=(222 + k * 51 + j * 202 , 119 + i * 97), mirror=False, activatable=True))
        beat_button_pattern.append(help_list)
    return beat_button_pattern

def create_slot_light_list(program: object) -> list:
    slot_light_list: list = []
    for i in range(16):
        slot_light_list.append(SlotLight(program=program, pos=(225 + i * 51, 78)))
    return slot_light_list

def create_sliders(program: object) -> list:
    slider_list: list = []
    slider_list.append(Slider(program=program, min=110, max=344, current_value_in_percent=80, y_pos=47))
    for i in range(4):
        slider_list.append(Slider(program=program, min=75, max=190, current_value_in_percent=80, y_pos=163 + i * 97))
    return slider_list
