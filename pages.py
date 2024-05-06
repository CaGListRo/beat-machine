from elements import WindowButton

import pygame as pg


class Page:
    def __init__(self, program: object) -> None:
        self.prog: object = program
        self.surface: pg.surface = pg.Surface((800, 600))
        self.pos: tuple = (self.prog.main_window.get_width() // 2 - self.surface.get_width() // 2,
                           self.prog.main_window.get_height() // 2 - self.surface.get_height() // 2)
        close_button_pos = (self.prog.images["window"].get_width() - self.prog.images["close button"].get_width(), 0)
        self.close_button = WindowButton(prog=self.prog, button_type="close button", pos=close_button_pos)

class SavePage(Page):
    def __init__(self) -> None:
        super().__init__(SavePage.prog)
    

    def render(self, surf) -> None:
        self.surface.blit(self.prog.images["window"], (0, 0))
        self.close_button.render(self.surface)
        surf.blit(self.surface)