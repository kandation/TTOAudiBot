import json
from typing import List, Union

from tkinter import Tk, Label, Button, Listbox, Frame, Toplevel, Canvas, StringVar

from WndMusicbar import WindowMusicBar
from song_manager import SongManager
from TaskAutoPlay import TaskAutoPlay
from WindowEditTime import WindowEditTime


class MyFirstGUI(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry("+0+0")
        self.protocol("WM_DELETE_WINDOW", self.USER_HAS_CLOSED_WINDOW)
        self._song_manager = SongManager()
        # self._game_wnd = WindowCapture('12TailsTH')
        self.child_windows: List[Toplevel] = []

        self.song_is_running = False

        self.config = {}

        # self.overrideredirect(True)
        # master.attributes('-topmost', True)
        self.bind('<Button-1>', self.SaveLastClickPos)
        self.bind('<B1-Motion>', self.Dragging)
        # self.bind('p', lambda d: print('aaa'))

        ## [CV REGION]
        self.frame = None

        self.title("A simple GUI")

        self.label = Label(self, text="Select Song")
        self.label.pack()

        self.panel = None
        self.queue = []

        self.thread = None

        self.list_music = Listbox(border=3)
        self.gui_create_music_list()

        self.list_music.bind('<Double-Button>', self.__list_music_double_click)
        self.list_music.bind("<<ListboxSelect>>", self.callback)

        self.list_music.pack(side="top", fill="both", expand=True)

        self.greet_button = Button(self, text="Kill", command=self.kill_img)
        self.greet_button.pack()

        self.greet_button = Button(self, text="Auto Detect (p)", command=self.greet)
        self.greet_button.pack()

        self.greet_button = Button(self, text="Edit Time", command=self.open_wnd_edittime)
        self.greet_button.pack()

        self.close_button = Button(self, text="Close", command=self.quit)
        self.close_button.pack()
        self.list_music.selection_set(first=0)
        self.load_config()

        self.player_thread = None

    def callback(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            self._song_manager.parse_song(data)
        else:
            pass

    def __list_music_double_click(self, event):
        selection = event.widget.curselection()
        if selection:
            self.open_wnd_edittime()

    def key_run_listener(self):
        if not self.song_is_running:
            self.song_is_running = True
            self.player_thread: TaskAutoPlay = TaskAutoPlay(self._song_manager)
            self.player_thread.daemon = True
            self.player_thread.start()
            print('-' * 50)

    def key_run_stop(self):
        if self.player_thread:
            self.player_thread.join()
        self.configure(bg='pink')
        self.song_is_running = False

    def load_config(self):
        try:
            with open('config.json', mode='r+') as fo:
                x = fo.read()
                if str(x).strip() == '':
                    x = "{}"
                self.config = json.loads(str(x))
        except FileNotFoundError:
            with open('config.json', mode='w') as fo:
                fo.write('{}')

    def save_config(self):
        with open('config.json', mode='r+') as fo:
            fo.write(json.dumps(self.config))

    def USER_HAS_CLOSED_WINDOW(self, callback=None):
        print("attempting to end thread")
        # end the running thread
        if self.thread:
            self.thread.join()
        print("deyrp")
        self.destroy()

    def kill_img(self):
        self.thread.join()
        self.update()

    def data_show_config(self):
        print(self.config)

    def openNewWindow(self, WINDOW, **kwargs):

        print(f'> Open Window: {WINDOW.__name__}, {self.child_windows}')
        hasWnd = [ch.__class__.__name__ == WINDOW.__name__ for ch in self.winfo_children()]
        if not any(hasWnd):
            newWnd = WINDOW(self, **kwargs) if kwargs else WINDOW(self)
            self.child_windows.append(newWnd)

    def gui_create_music_list(self):
        for i, song in enumerate(self._song_manager.song_entry):
            txt = f"{str(i + 1).zfill(2)}-{song.get('name')} ({song.get('time')})"
            self.list_music.insert(i, txt)

    def reload_list(self):
        self.list_music.delete(0, 'end')
        self.gui_create_music_list()

    def SaveLastClickPos(self, event):
        global lastClickX, lastClickY
        lastClickX = event.x
        lastClickY = event.y

    def Dragging(self, event):
        x, y = event.x - lastClickX + self.winfo_x(), event.y - lastClickY + self.winfo_y()
        self.geometry("+%s+%s" % (x, y))

    def greet(self):
        self.openNewWindow(WindowMusicBar)
        print("Greetings!")

    def open_wnd_edittime(self):
        self.openNewWindow(WindowEditTime, song_mng=self._song_manager)
        print("OpenWND: Editt")


try:
    my_gui = MyFirstGUI()
    my_gui.mainloop()
except:
    print('error1')
finally:
    exit()
