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


class Button:
    def __init__(self, prog: object, button_type: str, pos: tuple, mirror: bool = False, activatable: bool = False) -> None:
        self.prog: object = prog
        self.button_type: str = button_type
        self.pos: tuple = pos
        self.active: bool = True if self.button_type == "stop" else False
        self.state: str = "active" if self.button_type == "stop" else "inactive"
        self.activatable = activatable       
        asset_string = f"{self.button_type}/{self.state}" if self.activatable else self.button_type
        self.image: pg.image = pg.transform.flip(self.prog.images[asset_string], mirror, False)
        self.rect: pg.rect = self.image.get_rect(topleft=self.pos)
        self.clicked: bool = False

    def is_active(self) -> bool:
        return self.active
    
    def switch_state(self) -> None:
        self.active = not self.active
        self.state = "active" if self.active else "inactive"
        self.image: pg.image = self.prog.images[self.button_type + "/" + self.state]
    
    def check_collision(self) -> bool:
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[0]:
                self.clicked = True

            if not pg.mouse.get_pressed()[0] and self.clicked:
                if self.activatable:          
                    self.switch_state()
                self.clicked = False
                return True           
        else:
            self.clicked = False

    def render(self, surf: pg.surface) -> None:
        surf.blit(self.image, self.pos)


class Slider:
    def __init__(self, program: object, min: int, max: int, current_value_in_percent: int, y_pos: int) -> None:
        self.prog: object = program
        self.min: int = min
        self.max: int = max
        self.range: int = self.max - self.min
        self.val: int = current_value_in_percent * self.range / 100
        self.image: pg.surface = self.prog.images["slider knob"]        
        self.y_pos: int = y_pos - self.image.get_height() // 2
        self.pos: list = [self.min + self.val - self.image.get_width() // 2, self.y_pos]
        self.rect: pg.rect = self.image.get_rect(topleft=self.pos)
        self.collide: bool = False

    def check_collision(self) -> None:
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.collide = True
        if pg.mouse.get_pressed()[0] and self.collide:
            self.pos[0] = mouse_pos[0] + self.image.get_width() // 2
            if self.pos[0] < self.min:
                self.pos[0] = self.min
            elif self.pos[0] > self.max - self.image.get_width() // 2:
                self.pos[0] = self.max - self.image.get_width() // 2
            self.rect: pg.rect = self.image.get_rect(topleft=self.pos)
        if not pg.mouse.get_pressed()[0]:
            self.collide = False

    def get_value(self) -> float:
        return round((self.pos[0] - self.min) / self.range, 2)

    def render(self, surf: pg.surface) -> None:
        surf.blit(self.image, self.pos)


class SlotLight:
    def __init__(self, program: object, pos: tuple) -> None:
        self.prog: object = program
        self.pos: tuple = pos
        self.active: bool = False
        self.state: str = "inactive"
        self.image: pg.surface = self.prog.images[f"slot light/{self.state}"]

    def update(self, activated: bool=False) -> None:
        self.active = True if activated else False
        self.state = "active" if activated else "inactive"   
        self.image = self.prog.images[f"slot light/{self.state}"]

    def render(self, surf: pg.Surface) -> None:
        surf.blit(self.image, self.pos)