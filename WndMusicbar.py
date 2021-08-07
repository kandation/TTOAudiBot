from typing import Union

from pynput import keyboard

from TaskRealtimeDetect import TaskRealtimeDetect
from TailsVision import TailsVision
from tkinter import Tk, Label, Button, Listbox, Frame, Toplevel, Canvas, StringVar


class WindowMusicBar(Toplevel):
    def __init__(self, master=None):
        self._wnd_is_close = False
        self.key_hook = keyboard.Listener(on_press=self.on_key_press, )
        # suppress = True
        self.key_hook.start()

        super().__init__(master=master)
        self.protocol("WM_DELETE_WINDOW", self.USER_HAS_CLOSED_WINDOW)
        self.wnd_width = 200
        self.wnd_height = 200

        self.thread: Union[None or TaskRealtimeDetect] = None
        self.vision: Union[None or TailsVision] = None

        self.pos_x, self.pos_y = self.master.config.get('wnd_detector', [0, 0])

        self._cv_is_running = False

        self.attributes('-topmost', True)
        self.attributes('-alpha', 0.5)
        self.overrideredirect(True)
        self.title("Detector")

        self.config(bg='#add123')

        # Create a transparent window
        self.wm_attributes('-transparentcolor', '#add123')

        self.geometry(f"{self.wnd_width}x{self.wnd_height}+{self.pos_x}+{self.pos_y}")
        label = Label(self, text="This is a new Window")

        self.bind('<Button-1>', self.SaveLastClickPos)
        self.bind('<B1-Motion>', self.Dragging)

        self.canvas = Canvas(self, width=300, height=300)

        self.btn_text_detect = StringVar()
        self.btn_text_detect.set('Start (P)')

        # c.create_rectangle(20,150,250,50,fill="blue")
        btn_close = Button(self, text='X', command=self.USER_HAS_CLOSED_WINDOW)
        btn_remmember = Button(self, text='Remember', command=self.data_remember)
        self.btn_detect = Button(self, text='Start (P)', command=self.btn_click_detect)
        label.place(x=0, y=0)
        btn_close.place(x=0, y=0)
        btn_remmember.place(x=20, y=0)
        self.btn_detect.place(x=0, y=25)
        self.canvas.pack()

        self.draw_crossing_line(self.canvas, width=3, fill='#00ff00')
        self.draw_rectangle_center(self.canvas, 100, 40, fill='#add123')

        self.cal_vision()

    def USER_HAS_CLOSED_WINDOW(self, callback=None):
        self._wnd_is_close = True
        self.key_hook.stop()
        if self.thread:
            self.thread.join()

        # keyboard.clear_all_hotkeys()
        self.destroy()

    def on_key_press(self, key):
        if self._wnd_is_close:
            return
        if key == keyboard.KeyCode.from_char('o'):
            if self._cv_is_running:
                self._cv_is_running = False
                self.btn_click_detect_stop()

        if key == keyboard.KeyCode.from_char('p'):
            if not self._cv_is_running:
                self._cv_is_running = True
                self.btn_click_detect()

    def cal_vision(self):
        cropbox = self.get_box_center(100, 40)
        self.vision = TailsVision(
            self.pos_x,
            self.pos_y,
            self.wnd_width,
            self.wnd_height,
            cropbox)

    def btn_click_detect(self):
        self._cv_is_running = True
        self.thread = TaskRealtimeDetect(self.vision, self.master)
        self.thread.start()
        self.canvas.configure(bg='cyan')
        self.btn_detect.configure(text="Stop (O)", command=self.btn_click_detect_stop)
        self.key_hook.stop()

    def btn_click_detect_stop(self):
        self._cv_is_running = False
        self.canvas.configure(bg='gray')
        self.btn_detect.configure(text='Start (P)', command=self.btn_click_detect)
        if self.thread:
            self.thread.join()

    def data_remember(self):
        print(self.winfo_x(), self.winfo_y())
        self.master.config['wnd_detector'] = [self.winfo_x(), self.winfo_y()]
        self.master.save_config()

    def draw_crossing_line(self, canvas: Canvas, **kwargs):
        ww, wh = self.wnd_width, self.wnd_height
        canvas.create_line((ww // 2), 0, (ww // 2), wh, kwargs)
        canvas.create_line(0, (wh // 2), ww, wh // 2, kwargs)

    def draw_rectangle(self, canvas: Canvas, x: int, y: int, w: int, h: int, **kwargs):
        canvas.create_rectangle(x, y, x + w, y + h, kwargs)

    def get_box_center(self, w: int, h: int):
        ww, wh = self.wnd_width, self.wnd_height
        return (ww // 2) - (w // 2), (wh // 2) - (h // 2), w, h,

    def draw_rectangle_center(self, canvas: Canvas, w: int, h: int, **kwargs):
        ww, wh = self.wnd_width, self.wnd_height
        self.draw_rectangle(canvas, (ww // 2) - (w // 2), (wh // 2) - (h // 2), w, h, **kwargs)

    def change_window(self):
        # remove the other window entirely
        self.destroy()

        # make root visible again
        self.master.iconify()
        self.master.deiconify()

    def SaveLastClickPos(self, event):
        global lastClickX, lastClickY
        lastClickX = event.x
        lastClickY = event.y

    def Dragging(self, event):
        x, y = event.x - lastClickX + self.winfo_x(), event.y - lastClickY + self.winfo_y()
        self.geometry("+%s+%s" % (x, y))
