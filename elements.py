import pygame as pg


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
        self.rect: pg.rect = self.image.get_rect(topleft=(self.prog.body_surf_pos[0] + self.pos[0], self.prog.body_surf_pos[1] + self.pos[1]))
        self.clicked: bool = False

    def set_state(self, set_to) -> None:
        self.active = set_to
        self.state = "active" if set_to else "inactive"
        self.image: pg.image = self.prog.images[self.button_type + "/" + self.state]

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
        self.rect: pg.rect = self.image.get_rect(topleft=(self.pos[0], self.y_pos))
        self.collide: bool = False

    def check_collision(self) -> None:
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.collide = True
        if pg.mouse.get_pressed()[0] and self.collide:
            self.pos[0] = mouse_pos[0] - self.prog.body_surf_pos[0] - self.image.get_width() // 2
            if self.pos[0] < self.min:
                self.pos[0] = self.min
            elif self.pos[0] > self.max - self.image.get_width() // 2:
                self.pos[0] = self.max - self.image.get_width() // 2
            self.rect.topleft = (self.prog.body_surf_pos[0] + self.pos[0], self.prog.body_surf_pos[1] + self.y_pos)
            self.val = (self.pos[0] - self.min) / self.range
        if not pg.mouse.get_pressed()[0]:
            self.collide = False
            self.rect.topleft = (self.prog.body_surf_pos[0] + self.pos[0], self.prog.body_surf_pos[1] + self.pos[1])

    def get_value(self) -> float:
        return round(self.val, 2)

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


class WindowButton:
    def __init__(self, prog: object, button_type: str, pos: tuple, offset: tuple, rotate: bool=False) -> None:
        self.prog: object = prog
        self.button_type: str = button_type
        self.pos: tuple = pos     
        self.image: pg.image = self.prog.images[button_type]
        rect_pos: tuple = (self.pos[0] + offset[0], self.pos[1] + offset[1])
        self.rect: pg.rect = self.image.get_rect(topleft=rect_pos)
        self.clicked: bool = False
        if rotate:
            self.image = pg.transform.rotate(self.image, 180)
    
    def check_collision(self) -> bool:
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[0]:
                self.clicked = True
            if not pg.mouse.get_pressed()[0] and self.clicked:
                self.clicked = False
                return True           
        else:
            self.clicked = False

    def render(self, surf: pg.surface) -> None:
        surf.blit(self.image, self.pos)


class FileButton:
    def __init__(self, file_name: str, pos: tuple, offset: tuple, rect_size: tuple) -> None:
        self.file_name: str = str(file_name)
        self.font = pg.font.SysFont("arial", 32)      

        self.rect_colors: dict = {"inactive": (247, 247, 247), "hover": "lightgray", "active": "black"}
        self.text_colors: dict = {"inactive": "black", "hover": "black", "active": "white"} 

        rect_pos: tuple = (pos[0] + offset[0], pos[1] + offset[1])
        self.rect: pg.rect = pg.Rect(rect_pos, rect_size)
        self.clicked: bool = False
        self.state: str = "inactive"
        self.offset: tuple = offset

    def set_inactive(self):
        self.state = "inactive"

    def is_active(self) -> bool:
        return self.state == "active"
    
    def update_offset(self, scroll_offset):
        self.rect[1] = self.rect[1] - scroll_offset
        self.offset = (self.offset[0], self.offset[1] - scroll_offset)
    
    def check_collision(self) -> bool:
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if self.state == "inactive":
                self.state = "hover"
            if pg.mouse.get_pressed()[0]:
                self.clicked = True
            if not pg.mouse.get_pressed()[0] and self.clicked and self.state == "hover":
                self.state = "active"
                self.clicked = False
                return True           
        else:
            if self.state == "hover":
                self.state = "inactive"
            self.clicked = False

    def render(self, surf: pg.surface) -> None:
        position = (self.rect[0] - self.offset[0], self.rect[1] - self.offset[1])
        pg.draw.rect(surf, self.rect_colors[self.state], (position, (self.rect[2], self.rect[3])))
        text_to_blit = self.font.render(self.file_name, True, self.text_colors[self.state])
        surf.blit(text_to_blit, position)


class FileSlider:
    def __init__(self, program: object, pos: tuple, max_pos: int, height: int, offset: tuple) -> None:
        self.prog: object = program
        self.pos: list = list(pos)
        self.min: int = self.pos[1]
        self.max: int = max_pos
        self.height: int = height
        self.range: int = self.max - self.min - self.height
        self.val: float = (self.pos[1] - self.min) / self.range
        self.offset: tuple = offset
        self.slider: pg.surface = pg.Surface((30, self.height))
        self.slider.fill((180, 180, 180))
        pg.draw.rect(self.slider, (150, 150, 150), (0, 0, 30, self.height), width=1)
        self.rect: pg.rect = pg.Rect(self.offset, (30, self.height))
        self.collide: bool = False
        self.click_offset = 0

    def check_collision(self) -> None:
        mouse_pos = pg.mouse.get_pos()
        self.collide = self.rect.collidepoint(mouse_pos)

        if pg.mouse.get_pressed()[0]:  
            if self.collide and self.click_offset == 0:
                self.click_offset = mouse_pos[1] - self.rect.top

            if self.click_offset != 0:
                new_y_pos = mouse_pos[1] - self.click_offset

                if new_y_pos < self.min:
                    new_y_pos = self.min
                if new_y_pos > self.max - self.height:
                    new_y_pos = self.max - self.height

                self.pos[1] = new_y_pos
                self.rect.topleft = (self.pos[0] + self.offset[0], self.pos[1] + self.offset[1])
                self.val = (self.pos[1] - self.min) / self.range
                print(f"Value: {self.val}, Slider Pos: {self.pos}")

        else:
            self.click_offset = 0
            self.rect.topleft = (self.pos[0] + self.offset[0], self.pos[1] + self.offset[1])

    def get_value(self) -> float:
        return self.val

    def render(self, surf: pg.surface) -> None:
        surf.blit(self.slider, self.pos)
        # pg.draw.rect(self.prog.main_window, "red", self.rect)
