from utils import load_image, scale_image, create_beat_button_pattern, create_slot_light_list, Button

import pygame as pg
from time import time

class BeatMachine:
    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode((1280, 720))
        self.fps: int = 0
        self.run: bool = True

        self.bpm: int = 120
        self.number_of_beats: int = 16
        self.active_instrument_slot: int = 0
        self.beat_duration: float = self.calculate_beat_times()
        self.beat_time: float = 0
        self.state: str = "stop"
        self.shift: bool = False
        self.font = pg.font.SysFont("arial", 40)

        self.dt: float = 0
        self.last_time: float = time()
        self.frames: int = 0
        self.frames_timer: float = 0
        self.instruments: list = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],]        
        
        self.assets: dict = {
            "body": scale_image(load_image(img_name="body"), scalefactor=0.55),
            "bpm +- 1": scale_image(load_image(img_name="bpm plus minus 1"), scalefactor=0.36),
            "bpm +- 10": scale_image(load_image(img_name="bpm plus minus 10"), scalefactor=0.36),
            "button1/active": scale_image(load_image(img_name="button 1 active"), scalefactor=0.42),
            "button1/inactive": scale_image(load_image(img_name="button 1 inactive"), scalefactor=0.42),
            "button234/active": scale_image(load_image(img_name="button 234 active"), scalefactor=0.42),
            "button234/inactive": scale_image(load_image(img_name="button 234 inactive"), scalefactor=0.42),
            "pause/active": scale_image(load_image(img_name="button pause active"), scalefactor=0.36),
            "pause/inactive": scale_image(load_image(img_name="button pause inactive"), scalefactor=0.36),
            "play/active": scale_image(load_image(img_name="button play active"), scalefactor=0.36),
            "play/inactive": scale_image(load_image(img_name="button play inactive"), scalefactor=0.36),
            "stop/active": scale_image(load_image(img_name="button stop active"), scalefactor=0.36),
            "stop/inactive": scale_image(load_image(img_name="button stop inactive"), scalefactor=0.36),
            "slider knob": scale_image(load_image(img_name="slider knob"), scalefactor=0.49),
            "slot light/active": scale_image(load_image(img_name="slot indicator active"), scalefactor=0.36),
            "slot light/inactive": scale_image(load_image(img_name="slot indicator inactive"), scalefactor=0.36),
            "display_glas": scale_image(load_image(img_name="display glas"), scalefactor=0.44),
        }

        self.beat_buttons = create_beat_button_pattern(self)
        self.slot_lights = create_slot_light_list(self)

        self.play_button = Button(prog=self, button_type="play", pos=(988, 31), activatable=True)
        self.pause_button = Button(prog=self, button_type="pause", pos=(931, 31), activatable=True)
        self.stop_button = Button(prog=self, button_type="stop", pos=(882, 31), activatable=True)
        self.bpm_minus_ten_button = Button(prog=self, button_type="bpm +- 10", pos=(470, 31), mirror=True)
        self.bpm_minus_one_button = Button(prog=self, button_type="bpm +- 1", pos=(519, 31), mirror=True)
        self.bpm_plus_ten_button = Button(prog=self, button_type="bpm +- 10", pos=(735, 31))
        self.bpm_plus_one_button = Button(prog=self, button_type="bpm +- 1", pos=(697, 31))
        
    def calculate_beat_times(self) -> float:
        return 60 / (self.bpm * 4)
    
    def de_activate_slot_lights(self) -> None:
        self.slot_lights[self.active_instrument_slot].update(activated=True)

    def slot_shifter(self) -> None:
        if self.shift:
            self.active_instrument_slot += 1
            self.shift = False
            if self.active_instrument_slot > self.number_of_beats - 1:
                self.active_instrument_slot = 0

    def play_instruments(self) -> None:
        pass

    def sum_beat_time(self) -> bool:
        self.beat_time += self.dt
        if self.beat_time >= self.beat_duration:
            self.beat_time = 0
            return True
        else:
            return False
        
    def calculate_fps(self) -> None:
        self.frames += 1
        self.frames_timer += self.dt
        if self.frames_timer >= 1:
            self.fps = self.frames
            self.frames, self.frames_timer = 0, 0

    def calculate_delta_time(self) -> None:
        self.dt = time() - self.last_time
        self.last_time = time()

    def check_button_collisions(self):
        for button_list in self.beat_buttons:
            for btn in button_list:
                btn.check_collision()
        if self.play_button.check_collision():
            if self.pause_button.is_active(): self.pause_button.switch_state()
            if self.stop_button.is_active(): self.stop_button.switch_state()
            self.state = "play"
        if self.pause_button.check_collision():
            if self.play_button.is_active(): self.play_button.switch_state()
            if self.stop_button.is_active(): self.stop_button.switch_state()
            self.state = "pause"
        if self.stop_button.check_collision():
            if self.pause_button.is_active(): self.pause_button.switch_state()
            if self.play_button.is_active(): self.play_button.switch_state()
            self.state = "stop"
            self.active_instrument_slot = 0
        if self.bpm_minus_ten_button.check_collision(): self.bpm -= 10
        if self.bpm_minus_one_button.check_collision(): self.bpm -= 1
        if self.bpm_plus_ten_button.check_collision(): self.bpm += 10
        if self.bpm_plus_one_button.check_collision(): self.bpm += 1

    def render_buttons(self):
        for button_list in self.beat_buttons:
            for btn in button_list:
                btn.render(self.screen)
        for light in self.slot_lights:
            light.render(self.screen)
        self.play_button.render(self.screen)
        self.pause_button.render(self.screen)
        self.stop_button.render(self.screen)
        self.bpm_minus_ten_button.render(self.screen)
        self.bpm_minus_one_button.render(self.screen)
        self.bpm_plus_ten_button.render(self.screen)
        self.bpm_plus_one_button.render(self.screen)

    def draw_window(self) -> None:
        pg.display.set_caption(f"     Beat Machine     FPS: {self.fps}")
        self.screen.blit(self.assets["body"], (0,0))
        self.render_buttons()
        
        bpm_to_blit = self.font.render(str(self.bpm), False, "green")
        self.screen.blit(bpm_to_blit, (680 - bpm_to_blit.get_width(), 23))
        self.screen.blit(self.assets["display_glas"], (557, 26))
        pg.display.update()

    def main(self) -> None:   
        while self.run:
            self.calculate_delta_time()
            self.calculate_fps()
            self.beat_duration = self.calculate_beat_times()
            self.check_button_collisions()
            for light in self.slot_lights:
                light.update()
            
            
            if self.state == "play" or self.state == "pause":                
                self.de_activate_slot_lights()

            if self.state == "play":
                self.play_instruments()
                self.shift = self.sum_beat_time()
                self.slot_shifter()

            
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False

            self.draw_window()

        pg.quit()


if __name__ == "__main__":
    bm = BeatMachine()
    bm.main()