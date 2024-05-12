from elements import WindowButton

import pygame as pg
import os


class Page:
    def __init__(self, program: object) -> None:
        self.prog: object = program

        self.PATH = "saved beats/"

        self.surface: pg.surface = pg.Surface((800, 600))
        self.surface.fill((111, 111, 111))
        self.surface.set_colorkey((111, 111, 111))

        self.pos: tuple = (self.prog.main_window.get_width() // 2 - self.surface.get_width() // 2,
                           self.prog.main_window.get_height() // 2 - self.surface.get_height() // 2)
        
        close_button_pos = (self.prog.images["window"].get_width() - self.prog.images["close button"].get_width(), 0)
        self.close_button = WindowButton(prog=self.prog, button_type="close button", pos=close_button_pos)

        self.font = pg.font.SysFont("arial", 32)
        self.header_font = pg.font.SysFont("arial bold", 42)
        

class SavePage(Page):
    def __init__(self, program: object) -> None:
        super().__init__(program=program)
        self.save_string: str = ""
        self.save_button: object = WindowButton(prog=self.prog, button_type="save button", pos=(234, 502))
        self.cancel_button: object = WindowButton(prog=self.prog, button_type="cancel button", pos=(450, 502))
        self.entry_rect: pg.rect = pg.Rect(234, 280, 332, 40)
        explain_text: str = "Enter at least one character to name your beat."
        self.explain_text_to_blit = self.font.render(explain_text, True, "black")
        self.explain_text_pos = (self.surface.get_width() // 2 - self.explain_text_to_blit.get_width() // 2, 150)

    def handle_events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.run = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    self.save_string = self.save_string[:-1]
                elif event.key == pg.K_RETURN and len(self.save_string) > 0:
                    self.save_beat()
                else:
                    if len(self.save_string) < 13:
                        self.save_string += event.unicode

    def save_beat(self) -> None:
        file_name: str = self.PATH + self.save_string + ".bmsf"
        try:
            with open(file_name, "x") as file:
                file.write(str(self.prog.bpm))
                file.write("\n")
                for channel in self.prog.sounds_to_use:
                    file.write(str(channel))
                    file.write(", ")
                for row in self.prog.beat_buttons:
                    file.write("\n")
                    for btn in row:
                        file.write(str(btn.is_active()))
                        file.write(", ")
            self.save_string = ""
            self.prog.state = "stop"

        except FileExistsError:
            self.prog.file_exists_error = True

    def check_collisions(self) -> None:
        if self.close_button.check_collision() or self.cancel_button.check_collision():
            self.save_string = ""
            self.prog.state = "stop"
        if self.save_button.check_collision() and len(self.save_string) > 0:
            self.save_beat()

    def update(self) -> None:
        self.handle_events()
        self.check_collisions()

    def render(self, surf) -> None:
        self.surface.blit(self.prog.images["window"], (0, 0))

        self.close_button.render(self.surface)
        self.save_button.render(self.surface)
        self.cancel_button.render(self.surface)

        self.surface.blit(self.explain_text_to_blit, self.explain_text_pos)
        pg.draw.rect(self.surface, (200, 200, 200), self.entry_rect, border_radius=3)
        pg.draw.rect(self.surface, "black", self.entry_rect, width=2, border_radius=3)     
        save_string_to_blit = self.font.render(self.save_string, True, "black")
        self.surface.blit(save_string_to_blit, (240, 280))

        surf.blit(self.surface, self.pos)


class LoadPage(Page):
    def __init__(self, program: object) -> None:
        super().__init__(program=program)
        self.load_button: object = WindowButton(prog=self.prog, button_type="load button", pos=(100, 150))
        self.cancel_button: object = WindowButton(prog=self.prog, button_type="cancel button", pos=(100, 350))
        header_text: str = "Load beat."
        self.header_text_to_blit: pg.surface = self.header_font.render(header_text, True, "black")
        self.header_text_pos: tuple = (self.surface.get_width() // 2 - self.header_text_to_blit.get_width() // 2, 20)
        self.file_strings: list = []
        self.display_surf: pg.surface = pg.Surface((300, 400))
        self.display_surf.fill((247, 247, 247))
        self.list_directory()
    
    def handle_events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.run = False


    def list_directory(self) -> None:
        for file in os.listdir(self.PATH):
            if os.path.isfile(os.path.join(self.PATH, file)):
                file_name, extension = os.path.splitext(file)
                self.file_strings.append(file_name)       
        if len(self.file_strings) > 0:
            self.file_surf: pg.surface = pg.Surface((300, 10 + 40 * len(self.file_strings)))
            self.file_surf.fill((247, 247, 247))
            for i, string in enumerate(self.file_strings):
                text_to_blit = self.font.render(str(string), True, "black")
                self.file_surf.blit(text_to_blit, (10, 10 + 40 * i))
            self.display_surf.blit(self.file_surf, (0, 0))

    def check_collisions(self) -> None:
        if self.close_button.check_collision() or self.cancel_button.check_collision():
            self.save_string = ""
            self.prog.state = "stop"
        if self.load_button.check_collision() and len(self.save_string) > 0:
            self.load_beat()

    def update(self) -> None:
        self.handle_events()
        self.check_collisions()

    def render(self, surf) -> None:
        self.surface.blit(self.prog.images["window"], (0, 0))

        self.surface.blit(self.header_text_to_blit, self.header_text_pos)

        self.close_button.render(self.surface)
        self.load_button.render(self.surface)
        self.cancel_button.render(self.surface)

        self.surface.blit(self.display_surf, (400, 100))
        # pg.draw.rect(self.surface, (200, 200, 200), self.entry_rect, border_radius=3)
        # pg.draw.rect(self.surface, "black", self.entry_rect, width=2, border_radius=3)     
        

        surf.blit(self.surface, self.pos)