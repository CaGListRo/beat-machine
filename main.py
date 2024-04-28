import pygame as pg
from time import time

class BeatMachine:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((1280, 720))
        self.fps = 0
        self.run = True

        self.bpm = 120
        self.number_of_beats = 16
        self.active_instrument_slot = 0
        self.beat_duration = self.calculate_beat_times()
        self.beat_time = 0
        self.play = False
        self.shift = False

        self.dt = 0
        self.last_time = time()
        self.frames = 0
        self.frames_timer = 0
        self.instruments = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],]
        
    def calculate_beat_times(self):
        return 60 / (self.bpm * 4)
    
    def slot_shifter(self):
        if self.shift:
            print(self.active_instrument_slot)
            self.active_instrument_slot += 1
            self.shift = False
            if self.active_instrument_slot > self.number_of_beats - 1:
                self.active_instrument_slot = 0

    def play_instruments(self):
        pass

    def sum_beat_time(self):
        self.beat_time += self.dt
        if self.beat_time >= self.beat_duration:
            self.beat_time = 0
            return True
        else:
            return False
        
    def calculate_fps(self):
        self.frames += 1
        self.frames_timer += self.dt
        if self.frames_timer >= 1:
            self.fps = self.frames
            self.frames, self.frames_timer = 0, 0

    def calculate_delta_time(self):
        self.dt = time() - self.last_time
        self.last_time = time()

    def draw_window(self):
        pg.display.set_caption(f"     Beat Maschine     FPS: {self.fps}")

        pg.display.update()

    def main(self):       
        while self.run:
            self.calculate_delta_time()
            self.calculate_fps()
            self.beat_duration = self.calculate_beat_times()
            
            if self.play:
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