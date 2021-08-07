import cv2
import numpy as np
import mss
import win32con
import win32gui


class TailsVision:
    def __init__(self, wnd_x, wnd_y, wnd_w, wnd_h, cropbox):
        self.wnd_x = wnd_x
        self.wnd_y = wnd_y
        self.wnd_w = wnd_w
        self.wnd_h = wnd_h

        self.crop = cropbox

        self.__cv_wnd_tiltes = []
        self.__cv_wnd_imgs = []
        self.__cv_wnd_names = []

        self.last_frame = None

    def update_wind_info(self, wnd_x, wnd_y, wnd_w, wnd_h):
        self.wnd_x = wnd_x
        self.wnd_y = wnd_y
        self.wnd_w = wnd_w
        self.wnd_h = wnd_h

    def __show_cv_wnd(self, name, img):
        if name not in self.__cv_wnd_names:
            self.__cv_wnd_names.append(f'CVWND:{name}')
            self.__cv_wnd_imgs.append(img)

    def sort_vis_wnd(self):
        w_names = self.__cv_wnd_names
        w_imgs = self.__cv_wnd_imgs
        iw, ih, ic = (0, 0, 0)
        for ind, img in enumerate(w_imgs):
            w = img.shape[0]
            h = img.shape[1]
            cv2.moveWindow(w_names[ind], iw, ih)
            iw += w

    def __list_cv_wnd(self):
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                # print(hex(hwnd), win32gui.GetWindowText(hwnd))
                if 'CV:' in win32gui.GetWindowText(hwnd):
                    self.__cv_wnd_tiltes.append([hwnd, win32gui.GetWindowText(hwnd)])

        win32gui.EnumWindows(winEnumHandler, None)
        return self.__cv_wnd_tiltes

    def __find_wnd(self):
        hwnds = self.__list_cv_wnd()
        for hwnd in hwnds:
            hwnd = hwnd[0]
            win32gui.ShowWindow(hwnd, 5)
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                  win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

    def testcap(self):
        diff = False
        try:
            frame, diff = self.run_diff()

            cv2image = cv2.resize(frame, dsize=(150, 140), interpolation=cv2.INTER_CUBIC)
            cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGB)

        except:
            cv2image = np.random.randint(low=0, high=255, size=(32, 32, 1), dtype=np.uint8)
        return cv2image, diff

    def get_crop_img(self):
        wx, wy = self.wnd_x, self.wnd_y
        wh, ww = self.wnd_h, self.wnd_w
        crop = self.crop

        monitor = {"top": wy + crop[1], "left": wx + crop[0], "width": crop[2], "height": crop[3]}

        with mss.mss() as sct:
            frame = np.array(sct.grab(monitor))
        return frame

    def run_diff(self):
        img = self.get_crop_img()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if self.last_frame is None:
            self.last_frame = gray
        x = cv2.absdiff(self.last_frame, gray)
        av = np.average(x) > 1
        if av:
            self.last_frame = gray
        # print(np.average(x) )
        return x, av
