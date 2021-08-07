"""
This File archive because we has gui
"""

# import json
# from time import sleep, time
#
# import pyautogui
# from pynput.keyboard import Key, Listener, KeyCode
#
# import keyboard
#
# isrunning = False
# is_quit = False
#
# def load_song_entry():
#     with open('song_entry.json', mode='r') as fo:
#         data = json.loads(fo.read())
#     return data
#
#
# def loadLevelIndex():
#     with open('song_level.txt', mode='r') as fo:
#         data = int(fo.read())
#     return data
#
#
# def get_song_notes_path(data):
#     files = []
#     for i, s in enumerate(data):
#         name = str(s.get('name')).lower().replace(' ', '_').replace('\'', '')
#         index = str(i + 1).zfill(2)
#         file_name = f'./notes/{index}_{name}.txt'
#         files.append(file_name)
#     return files
#
#
# def on_key_press(event):
#     global isrunning,is_quit
#     key_name = str(event.name).lower()
#     if key_name == 'p':
#         print('start-capture')
#         if not isrunning:
#             isrunning = True
#
#
#     if key_name == 'o':
#         print('stop-bot')
#         isrunning = False
#         is_quit = True
#
#
#
#
# def getkey(code: str):
#     key = []
#     if bool(int(code[1])): key.append('a')
#     if bool(int(code[2])): key.append('s')
#     if bool(int(code[3])): key.append('d')
#     return key
#
#
# def getDlilation(txt):
#     t = str(txt).split(':')
#     sec = int(t[0]) * 60 + int(t[1])
#     return sec
#
#
# def runsong():
#     global isrunning
#     pyautogui.PAUSE = 0
#     song_index = loadLevelIndex()
#     song_entry = load_song_entry()
#     song_files = get_song_notes_path(song_entry)
#
#     # print(song_entry)
#
#     current_song_info = song_entry[song_index-1]
#     # print(current_song_info)
#
#     time_init = 0
#     timeline = []
#
#     with open(song_files[song_index-1], mode='r') as fo:
#         data = fo.readlines()
#
#     bpm = current_song_info.get('bpm')
#     dilation = getDlilation(current_song_info.get('time'))
#     delay = dilation / len(data)
#     print(dilation, delay)
#
#     for d in data:
#         keycone = getkey(d.strip())
#         if len(keycone):
#             timeline.append((time_init, getkey(d.strip())))
#         time_init += delay
#
#     print(timeline)
#
#     game_time = time()
#     note_current = timeline[0]
#     time_error = 0
#     sum_error = 0
#     print(note_current)
#     ix = 1
#     tick = 0
#     while True:
#         now_time = time() - (game_time)
#         if now_time >= note_current[0]:
#             print(tick, [sum_error], now_time, note_current, 'ERR={0:10.4}'.format(note_current[0] - now_time))
#             tick += 1
#             time_error = note_current[0] - now_time
#             sum_error += time_error
#             for key in note_current[1]:
#                 try:
#                     pass
#                     pyautogui.press(key)
#                     # keyboard.press_and_release(u"{0}".format(key))
#                 except:
#                     pass
#             try:
#                 note_current = timeline[ix]
#                 ix += 1
#             except:
#                 break
#
#     print(f'total={now_time}, Dilation={dilation}, err={now_time - dilation}')
#
#     isrunning = False
#
#     start_time = 5.8
#
#     # for i, d in enumerate(data):
#     #     print(i, d, getkey(d))
#     #     for key in getkey(d):
#     #         pass
#     #         keyboard.press_and_release(u"{0}".format(key))
#     #     sleep(delay)
#     # isrunning = False
#
#
# keyboard.on_press(on_key_press)
# while True:
#     if isrunning:
#         runsong()
# print('end_song')
