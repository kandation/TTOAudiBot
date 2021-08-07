import threading
from time import time
from typing import Optional

import keyboard
import pyautogui

from song_manager import SongManager


class TaskAutoPlay(threading.Thread):
    def __init__(self, song_mng: SongManager):
        self.song_manager = song_mng

        self.stopEvent = threading.Event()
        threading.Thread.__init__(self)

    def re_cal_time(self, timeline, err):
        new_timeline = []
        for i in timeline:
            new_timeline.append((i[0] + err, i[1]))
        return new_timeline

    def run(self):
        pyautogui.PAUSE = 0
        current_song_info = self.song_manager.get_current()
        print(current_song_info)

        current_song_path = self.song_manager.get_current_path_of_note()

        time_init = 0
        timeline = []

        with open(current_song_path, mode='r') as fo:
            data = fo.readlines()

        bpm = current_song_info.get('bpm')
        dilation = self.song_manager.get_dlilation()
        delay = dilation / (len(data))
        print(dilation, delay)

        for d in data:
            keycone = self.song_manager.getkey(d.strip())
            # if len(keycone):
            timeline.append((time_init, keycone))
            time_init += delay
        print(timeline)

        note_current = timeline[0]
        time_error = 0
        sum_error = 0
        ix = 1
        tick = 0
        now_time = time()
        game_time = time()
        retry_num = 0
        while not self.stopEvent.is_set():
            # while True:
            now_time = time() - game_time
            if now_time >= note_current[0]:
                time_error = abs(note_current[0] - now_time)
                print(retry_num,tick, [sum_error], now_time, note_current, 'ERR={0:10.4}'.format(time_error))
                tick += 1
                sum_error += time_error

                # if sum_error > 0.5:
                #     timeline = self.re_cal_time(timeline, sum_error)
                #     sum_error = 0
                #     retry_num += 1

                for key in note_current[1]:
                    try:
                        pass
                        pyautogui.press(key)
                        # keyboard.press_and_release(u"{0}".format(key))
                    except:
                        pass

                try:
                    note_current = timeline[ix]
                    ix += 1
                except:
                    break

        print(f'total={now_time}, Dilation={dilation}, err={now_time - dilation}')
        self.stopEvent.set()

    def join(self, timeout: Optional[float] = None) -> None:
        try:
            self.stopEvent.set()
            threading.Thread.join(self, 0)
        except:
            pass
