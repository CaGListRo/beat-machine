from elements import WindowButton, FileButton

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
        self.close_button = WindowButton(prog=self.prog, button_type="close button", pos=close_button_pos, offset=(240, 60))

        self.font = pg.font.SysFont("arial", 32)
        self.header_font = pg.font.SysFont("arial bold", 42)
        

class SavePage(Page):
    def __init__(self, program: object) -> None:
        super().__init__(program=program)
        self.save_string: str = ""
        self.save_button: object = WindowButton(prog=self.prog, button_type="save button", pos=(234, 502), offset=(240, 60))
        self.cancel_button: object = WindowButton(prog=self.prog, button_type="cancel button", pos=(450, 502), offset=(240, 60))
        self.entry_rect: pg.rect = pg.Rect(234, 280, 332, 40)
        explain_text: str = "Enter at least one character to name your beat."
        self.explain_text_to_blit = self.font.render(explain_text, True, "black")
        self.explain_text_pos = (self.surface.get_width() // 2 - self.explain_text_to_blit.get_width() // 2, 150)
        self.error = False

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
            self.error_page = ErrorPage(program=self.prog, error="FileExistsError")
            self.error = True

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

        if self.error:
            self.error_page.render(self.surface)

        surf.blit(self.surface, self.pos)


class LoadPage(Page):
    def __init__(self, program: object) -> None:
        super().__init__(program=program)
        self.load_button: object = WindowButton(prog=self.prog, button_type="load button", pos=(100, 150), offset=(240, 60))
        self.cancel_button: object = WindowButton(prog=self.prog, button_type="cancel button", pos=(100, 350), offset=(240, 60))
        header_text: str = "Load beat."
        self.header_text_to_blit: pg.surface = self.header_font.render(header_text, True, "black")
        self.header_text_pos: tuple = (self.surface.get_width() // 2 - self.header_text_to_blit.get_width() // 2, 20)
        self.file_strings: list = []
        self.file_buttons: list = []
        self.collision_rects: list = []
        self.active_one: int = None
        self.surf_difference: int = 0
        self.scroll_offset: int = 0
        self.old_offset: int = self.scroll_offset
        
        self.display_surf: pg.surface = pg.Surface((300, 400))
        self.display_surf.fill((247, 247, 247))
        self.list_directory()
    
    def load_beat(self) -> None:
        file_to_load: str = "saved beats/" + str(self.file_strings[self.active_one]) + ".bmsf"
        with open(file_to_load, "r") as file:
            data = file.read()
            data = data.split("\n")
            self.prog.bpm = int(data[0])
            tones = data[1].strip().split(",")
            del tones[-1]
            self.prog.sounds_to_use = [tone.strip() for tone in tones]
            for i in range(4):
                self.prog.channels[i] = self.prog.sounds[self.prog.sounds_to_use[i]]
            beat_button_list = []
            for i in range(2, 6):
                data[i] = data[i].strip().split(",")
                del data[i][-1]
                beat_button_list.append([state.strip() for state in data[i]])
        for i, row in enumerate(beat_button_list):
            for j, state in enumerate(row):
                if state == "True":
                    self.prog.beat_buttons[i][j].set_state(True)
                if state == "False":
                    self.prog.beat_buttons[i][j].set_state(False)
        self.prog.state = "stop"

    def handle_events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.run = False
            if self.surf_difference > 0:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        if self.scroll_offset > 0:
                            self.scroll_offset -= 20
                    if event.button == 5:
                        if self.scroll_offset < self.surf_difference:
                            self.scroll_offset += 20

    def list_directory(self) -> None:
        for file in os.listdir(self.PATH):
            if os.path.isfile(os.path.join(self.PATH, file)):
                file_name, extension = os.path.splitext(file)
                self.file_strings.append(file_name)       
        if len(self.file_strings) > 0:
            self.create_file_surface()

    def create_file_surface(self) -> None:
            self.listed_files_surf: pg.surface = pg.Surface((300, 10 + 40 * len(self.file_strings)))
            self.listed_files_surf.fill((247, 247, 247))
            for i, string in enumerate(self.file_strings):
                self.file_buttons.append(FileButton(file_name=string, pos=(10, 10 + 40 * i), offset=(640, 160), rect_size=(280, 40)))
            if self.listed_files_surf.get_height() > self.display_surf.get_height():
                self.surf_difference = self.listed_files_surf.get_height() - self.display_surf.get_height()

    def check_collisions(self) -> None:
        if self.close_button.check_collision() or self.cancel_button.check_collision():
            self.prog.state = "stop"
        if self.load_button.check_collision() and self.active_one != None:
            self.load_beat()
        if len(self.file_strings) > 0:
            for i, button in enumerate(self.file_buttons):
                if button.check_collision():
                    if button.is_active():
                        self.active_one = i
            if self.active_one != None:
                for i, button in enumerate(self.file_buttons):
                    if i != self.active_one:
                        button.set_inactive()

    def update(self) -> None:
        self.handle_events()
        if self.scroll_offset < 0:
            self.scroll_offset = 0
        if self.scroll_offset > self.surf_difference:                 
            self.scroll_offset = self.surf_difference

        if self.old_offset != self.scroll_offset:
            print(self.scroll_offset)
            for button in self.file_buttons:
                button.update_offset(scroll_offset=self.scroll_offset - self.old_offset)
                pg.display.flip()
        self.old_offset = self.scroll_offset
        self.check_collisions()

    def render(self, surf) -> None:
        self.surface.blit(self.prog.images["window"], (0, 0))

        self.surface.blit(self.header_text_to_blit, self.header_text_pos)

        self.close_button.render(self.surface)
        self.load_button.render(self.surface)
        self.cancel_button.render(self.surface)
       
        if len(self.file_strings) > 0:
            for button in self.file_buttons:
                button.render(self.listed_files_surf)
        self.display_surf.blit(self.listed_files_surf, (0, 0 - self.scroll_offset))
        self.surface.blit(self.display_surf, (400, 100))

        surf.blit(self.surface, self.pos)


class ErrorPage:
    def __init__(self, program: object, error: str) -> None:
        self.prog: object = program

        self.surface: pg.surface = pg.Surface(self.prog.images["small window"].get_size())
        self.surface.fill((111, 111, 111))
        self.surface.set_colorkey((111, 111, 111))

        self.pos: tuple = (self.prog.main_window.get_width() // 2 - self.surface.get_width() // 2,
                           self.prog.main_window.get_height() // 2 - self.surface.get_height() // 2)
        
        close_button_pos = (self.surface.get_width() - self.prog.images["close button"].get_width(), 0)
        self.close_button = WindowButton(prog=self.prog, button_type="close button", pos=close_button_pos, offset=(280, 224))

        self.font = pg.font.SysFont("arial", 32)

        self.error: str = error
        if self.error == "FileExistsError":
            self.file_exists_text1: str = "This file name already exists,"
            self.file_exists_text2: str = "choose another one."
            self.file_exists_surf1: pg.surface = self.font.render(self.file_exists_text1, True, "darkred")
            self.file_exists_surf2: pg.surface = self.font.render(self.file_exists_text2, True, "darkred")

    def check_collisions(self) -> None:
        if self.close_button.check_collision():
            self.prog.save_page.error = False

    def render(self, surf) -> None:
        self.check_collisions()
        if self.error == "FileExistsError":
            self.surface.blit(self.prog.images["small window"], (0, 0))
            self.surface.blit(self.file_exists_surf1, 
                     (self.surface.get_width() // 2 - self.file_exists_surf1.get_width() // 2, 
                      self.prog.images["small window"].get_height() // 2 - self.file_exists_surf1.get_height()))
            self.surface.blit(self.file_exists_surf2, 
                     (self.surface.get_width() // 2 - self.file_exists_surf2.get_width() // 2, 
                      self.prog.images["small window"].get_height() // 2 + self.file_exists_surf2.get_height() - 30))
        
        self.close_button.render(self.surface)
        surf.blit(self.surface, (surf.get_width() // 2 - self.prog.images["small window"].get_width() // 2, 
                      surf.get_height() // 2 - self.prog.images["small window"].get_height() // 2))


class SoundSelectPage:
    def __init__(self, program: object) -> None:
        self.prog: object = program
        self.tone_surf: pg.surface = pg.Surface((250, 50 + 40 * len(self.prog.all_sound_names)))
        self.tone_surf.fill((247, 247, 247))
        self.sound_file_buttons: list = []
        self.collision_rects: list = []
        self.active_one: int = None

        self.close_button_pos = (self.tone_surf.get_width() // 2 + 5, self.tone_surf.get_height() - self.prog.images["close button"].get_height())
        self.close_button = WindowButton(prog=self.prog, button_type="close button", pos=self.close_button_pos, offset=(0, 0))
        accept_button_pos = (self.tone_surf.get_width() // 2 - self.prog.images["accept button"].get_width() - 5, self.tone_surf.get_height() - self.prog.images["accept button"].get_height())
        self.accept_button = WindowButton(prog=self.prog, button_type="accept button", pos=accept_button_pos, offset=(0, 0))
        self.create_sound_buttons()
    
    def handle_events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.run = False

    def create_sound_buttons(self) -> None:
        for i, soundname in enumerate(self.prog.all_sound_names):
            self.sound_file_buttons.append(FileButton(file_name=soundname, pos=(10, 10 + 40 * i), offset=(0, 0), rect_size=(240, 40)))            

    def check_collisions(self) -> None:
        if self.close_button.check_collision():
            self.prog.state = "stop"
        if self.accept_button.check_collision():
            if self.active_one != None:
                self.prog.sounds_to_use[self.prog.sound_slot_to_change] = self.prog.all_sound_names[self.active_one]
                self.prog.channels[self.prog.sound_slot_to_change] = self.prog.sounds[self.prog.sounds_to_use[self.prog.sound_slot_to_change]]
                self.active_one = None
            self.prog.sound_slot_to_change = None
            self.prog.state = "stop"

        for i, button in enumerate(self.sound_file_buttons):
            if button.check_collision():
                if button.is_active():
                    self.active_one = i
        if self.active_one != None:
            for i, button in enumerate(self.sound_file_buttons):
                if i != self.active_one:
                    button.set_inactive()

    def update(self) -> None:
        self.handle_events()
        self.check_collisions()

    def render(self, surf) -> None: 
        for button in self.sound_file_buttons:
            button.render(self.tone_surf)

        self.accept_button.render(self.tone_surf)
        self.close_button.render(self.tone_surf)

        surf.blit(self.tone_surf, (0, 0))
        



    