from elements import WindowButton

import pygame as pg


class Page:
    def __init__(self, program: object) -> None:
        self.prog: object = program

        self.surface: pg.surface = pg.Surface((800, 600))
        self.surface.fill((111, 111, 111))
        self.surface.set_colorkey((111, 111, 111))

        self.pos: tuple = (self.prog.main_window.get_width() // 2 - self.surface.get_width() // 2,
                           self.prog.main_window.get_height() // 2 - self.surface.get_height() // 2)
        
        close_button_pos = (self.prog.images["window"].get_width() - self.prog.images["close button"].get_width(), 0)
        self.close_button = WindowButton(prog=self.prog, button_type="close button", pos=close_button_pos)

        self.font = pg.font.SysFont("arial", 32)
        

class SavePage(Page):
    def __init__(self, program: object) -> None:
        super().__init__(program=program)
        self.save_string: str = ""
        self.save_button = WindowButton(prog=self.prog, button_type="save button", pos=(234, 502))
        self.cancel_button = WindowButton(prog=self.prog, button_type="cancel button", pos=(450, 502))
        self.entry_rect = pg.Rect(234, 280, 332, 40)

    def handle_events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.run = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    self.save_string = self.save_string[:-1]
                else:
                    if len(self.save_string) < 13:
                        self.save_string += event.unicode

    def check_collisions(self) -> None:
        if self.close_button.check_collision():
            self.prog.state = "stop"

    def update(self) -> None:
        self.handle_events()
        self.check_collisions()

    def render(self, surf) -> None:
        self.surface.blit(self.prog.images["window"], (0, 0))
        self.close_button.render(self.surface)
        self.save_button.render(self.surface)
        self.cancel_button.render(self.surface)
        pg.draw.rect(self.surface, "black", self.entry_rect, width=2, border_radius=3)
        text_to_blit = self.font.render(self.save_string, True, "black")
        self.surface.blit(text_to_blit, (240, 280))

        surf.blit(self.surface, self.pos)