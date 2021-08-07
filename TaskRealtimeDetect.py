import threading

import numpy as np
from PIL import ImageTk, Image
from tkinter import Tk, Label, Button, Listbox, Frame, Toplevel, Canvas, StringVar

from pynput import keyboard

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import MyFirstGUI


class TaskRealtimeDetect(threading.Thread):
    def __init__(self, vision, gui: 'MyFirstGUI'):
        self.vision = vision
        self.gui = gui

        self.stopEvent = threading.Event()
        self._sleepperiod = 1.0

        self.panel = None
        self.frame = None
        threading.Thread.__init__(self)
        # self.daemon = True
        self.is_diff_first = False

    def run(self):
        try:
            # keep looping over frames until we are instructed to stop
            while not self.stopEvent.is_set():
                if self.is_diff_first:
                    break

                self.frame, diff = self.vision.testcap()
                # self.frame = imutils.resize(self.frame, width=300)

                image = self.frame

                # np_img = np.squeeze(image, axis=2)
                image = Image.fromarray(image)
                imx = image.copy()
                image = ImageTk.PhotoImage(image)

                if diff and not self.is_diff_first:

                    self.is_diff_first = True
                    imx.save('first.png')

                    self.gui.configure(bg='red')
                    self.gui.key_run_listener()
                    # print('-'*50)
                else:
                    self.gui.configure(bg='gray')

                if self.panel is None:
                    self.panel = Label(self.gui, image=image)
                    self.panel.image = image
                    self.panel.pack(side="left", padx=10, pady=10)
                else:
                    self.panel.configure(image=image)
                    self.panel.image = image
            if self.panel:
                self.panel.image = None
                self.panel.destroy()

        except RuntimeError as e:
            print("[INFO] caught a RuntimeError")

        # self.lmain.imgtk = imgtk
        # self.lmain.configure(image=imgtk)
        # self.lmain.after(1, self.testcap)

    def join(self, timeout=None):
        """ Stop the thread. """
        try:
            self.stopEvent.set()
            # threading.Thread.join(self,5)
            self.gui.key_run_stop()
        except Exception as e:
            print(e)
            print("StopEvent Error")
            pass
