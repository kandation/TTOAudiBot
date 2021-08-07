import datetime
import re
import tkinter as tk
from typing import TYPE_CHECKING, Union

from song_manager import SongManager
import re as regex

if TYPE_CHECKING:
    from main import MyFirstGUI


class WindowEditTime(tk.Toplevel):

    def __init__(self, master: 'MyFirstGUI', **kwargs):
        self.master = master
        super().__init__(master=master)

        self.geometry('+0+250')
        self.song_mng: SongManager = kwargs.get('song_mng', None)
        self.lb_frame: tk.LabelFrame = None
        self.lb_time_old: tk.Label = None
        self.lb_time: tk.Label = None
        self.tx_time: tk.Entry = None
        self.tx_time_colon: tk.Entry = None
        self.btn_save: tk.Button = None
        self.lb_frame_cal: tk.LabelFrame = None
        self.lb_start_time: tk.Label = None
        self.tx_start_time: tk.Entry = None
        self.tx_end_time: tk.Entry = None
        self.lb_time_diff: tk.Label = None
        self.btn_cal: tk.Button = None
        self.time_diff: datetime.timedelta = datetime.time()
        self.__time_type_used = 0

        self.initialize()

    def initialize(self):

        vcmd = (self.register(self.__sec_validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        vcmd2 = (self.register(self.__time_validate),
                 '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        current_song_text = self.song_mng.get_current_title()
        self.lb_frame = tk.LabelFrame(self, text=f'Edit:{current_song_text}')
        self.lb_frame.pack(fill=tk.BOTH, padx=5, pady=5)

        current_song_time_d_txt = self.song_mng.get_dlilation()
        current_song_time_txt = self.song_mng.get_current_time_readable()
        self.lb_time_old = tk.Label(self.lb_frame, text=f'{current_song_time_txt} OR {current_song_time_d_txt}')
        self.lb_time_old.pack(fill=tk.BOTH, expand=tk.YES)

        self.lb_time = tk.Label(self.lb_frame, text='Time (sec):')
        self.lb_time.pack(fill=tk.BOTH, expand=tk.YES)

        self.tx_time = tk.Entry(self.lb_frame, validate='all', validatecommand=vcmd)
        self.tx_time.bind('<KeyPress>', self.remove_time_colon)
        self.tx_time.pack(fill=tk.BOTH, expand=tk.YES)
        # self.tx_time.pack(fill='both', expand='yes')

        self.lb_time = tk.Label(self.lb_frame, text='Or Time (5+1.3):')
        self.lb_time.pack(fill=tk.BOTH, expand=tk.YES)

        self.tx_time_colon = tk.Entry(self.lb_frame, validate='all', validatecommand=vcmd2)
        self.tx_time_colon.bind('<KeyPress>', self.remove_time_sec)
        self.tx_time_colon.pack(fill=tk.BOTH, expand=tk.YES)

        self.btn_save = tk.Button(self.lb_frame, text='Save', command=self.save_time)
        self.btn_save.pack()

        self.lb_frame_cal = tk.LabelFrame(self, text='calculate')
        self.lb_frame_cal.pack()

        self.lb_start_time = tk.Label(self.lb_frame_cal, text='Example\n2+51.3')
        self.lb_start_time.pack()

        self.tx_start_time = tk.Entry(self.lb_frame_cal, validate='all', validatecommand=vcmd2)
        self.tx_start_time.bind('<KeyRelease>', self.__cal_time_event)
        self.tx_start_time.pack()

        self.tx_end_time = tk.Entry(self.lb_frame_cal, validate='all', validatecommand=vcmd2)
        self.tx_end_time.bind('<KeyRelease>', self.__cal_time_event)
        self.tx_end_time.pack()

        self.lb_time_diff = tk.Label(self.lb_frame_cal, text='TimeDiff=:NaN')
        self.lb_time_diff.pack()

        self.btn_cal = tk.Button(self.lb_frame_cal, text='SendToTop', command=self.send2top)
        self.btn_cal.pack()

    def __cal_time_event(self, evetn):
        self.__cal_time()

    def send2top(self):
        self.tx_time.delete(0, tk.END)
        self.tx_time_colon.delete(0, tk.END)

        self.time_diffL: datetime.timedelta
        print('offset', self.time_diff.total_seconds())
        if self.__cal_time():
            self.tx_time.insert(0, self.time_diff.total_seconds())
            self.__time_type_used = 0

    def remove_time_sec(self, event):
        self.tx_time.delete(0, tk.END)
        self.__time_type_used = 1

    def remove_time_colon(self, event):
        self.tx_time_colon.delete(0, tk.END)
        self.__time_type_used = 0

    def __cal_time(self):
        try:
            arr = [
                self.__check_time(self.tx_start_time.get()),
                self.__check_time(self.tx_end_time.get())]
            print('maxmin=', max(arr), min(arr))
            diff = max(arr) - min(arr)
            print(f'time_diff={diff}')
            self.time_diff = diff
            self.lb_time_diff.config(text=f'{diff}')
        except ValueError:
            print('Error Time value')
            self.lb_time_diff.config(text=f'Error')
            return False
        return True

    def __check_time(self, txt: str) -> Union[datetime.timedelta, datetime.datetime]:
        val = txt.strip()
        val = val or '0'
        print(val)
        sec = 0
        has_colon = str(val).count('+') == 1
        has_dot = str(val).count('.') == 1

        if has_colon and has_dot:
            tm = datetime.datetime.strptime(val, '%M+%S.%f')
        elif has_colon and not has_dot:
            tm = datetime.datetime.strptime(val, '%M+%S')
        else:
            tm = datetime.datetime(1900, 1, 1) + datetime.timedelta(seconds=float(val))

        print(type(tm))
        return tm

    def __convert2timediff(self, dt: datetime.datetime) -> datetime.timedelta:
        return dt - datetime.datetime(1900, 1, 1)

    def __time_validate(self, action, index, value_if_allowed,
                        prior_value, text, validation_type, trigger_type, widget_name):
        rg = r'[0-9.+]'
        fin = regex.search(rg, text, re.IGNORECASE)
        case_1 = text.strip() != ''
        case_2 = str(value_if_allowed).count('+') <= 1
        case_3 = str(value_if_allowed).count('.') <= 1

        if not fin: return False

        if all([case_1, case_2, case_3]):
            return True
        else:
            return False

    def __sec_validate(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        if value_if_allowed and text.strip() != '' or value_if_allowed == '':
            try:
                tx = value_if_allowed if value_if_allowed else '0'
                float(tx)
                return True
            except ValueError:
                return False
        else:
            return False

    def check_input_and_remove(self):
        if 0:
            pass

    def save_time(self):
        print(self.tx_time.get())
        try:
            if self.__time_type_used == 0:
                tx = float(self.tx_time.get()) if self.tx_time.get().strip() else 0
            else:
                tdiff = self.__check_time(str(self.tx_time_colon.get()).strip())
                tx = self.__convert2timediff(tdiff).total_seconds()
        except:
            self.lb_time.config(text='Error')
        print(f'new_save_sec={tx}')
        self.song_mng.set_sec(tx)
        self.song_mng.save()
        self.master.reload_list()
        self.refresh()

    def refresh(self):
        current_song_time_d_txt = self.song_mng.get_dlilation()
        current_song_time_txt = self.song_mng.get_current_time_readable()
        self.lb_time_old.config(text=f'{current_song_time_txt} OR {current_song_time_d_txt}')
        self.lb_time.config(text='Or Time (5+1.3)')
