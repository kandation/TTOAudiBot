import json


class SongManager:
    def __init__(self):
        self.song_entry = {}
        self.current_select_index = 0
        self.__current_song = {}
        self.__song_entry_filename = 'song_entry.json'
        self.initialize()

    def reload(self):
        self.initialize()

    def initialize(self):
        self.song_entry = self.__load_song_entry()
        self.__current_song = self.song_entry[0]

    def parse_song(self, txt):
        index = str(txt).strip().split('-')[0]
        index = int(index)
        print(f'parse_index={txt}')
        self.current_select_index = index - 1
        print(f'Current Index={self.current_select_index}')
        self.__current_song = self.song_entry[self.current_select_index]
        # print(self.song_entry)
        print(f'current_song={self.__current_song}')
        return index

    def __load_song_entry(self):
        with open(self.__song_entry_filename, mode='r') as fo:
            data = json.loads(fo.read())
        return data

    def get_current(self):
        return self.__current_song

    def get_current_title(self):
        return self.get_current().get('name', '-no-title-')

    @staticmethod
    def __get_song_notes_path(data):
        files = []
        for i, s in enumerate(data):
            name = str(s.get('name')).lower().replace(' ', '_').replace('\'', '')
            index = str(i + 1).zfill(2)
            file_name = f'./notes/{index}_{name}.txt'
            files.append(file_name)
        return files

    def get_path_of_note_files(self):
        return SongManager.__get_song_notes_path(self.song_entry)

    def get_current_path_of_note(self):
        return self.get_path_of_note_files()[self.current_select_index]

    def convert_time2sec(self, txt):
        t = str(txt).split(':')
        sec = float(t[0]) * 60.0 + float(t[1])
        return sec

    def get_dlilation(self):
        return self.convert_time2sec(self.__current_song.get('time', '0:1'))

    @staticmethod
    def getkey(code: str):
        key = []
        if bool(int(code[1])): key.append('a')
        if bool(int(code[2])): key.append('s')
        if bool(int(code[3])): key.append('d')
        return key

    def get_current_time_readable(self):
        return self.__current_song.get('time', '0:1')

    def set_sec(self, sec=0):
        if sec > 0:
            self.__current_song['sec'] = sec
            self.__current_song['time'] = self.convert_sec_to_time(self.__current_song.get('sec', 0))

    def set_time(self, tm='0:0'):
        self.__current_song['sec'] = self.convert_time2sec(tm)
        self.__current_song['time'] = tm

    def save(self):
        self.song_entry[self.current_select_index] = self.__current_song
        with open(self.__song_entry_filename, mode='w') as fo:
            fo.write(json.dumps(self.song_entry))
        print('Save Entry OK')
        return True

    def convert_sec_to_time(self, sec):
        mn = sec // 60
        sc = (sec - (mn * 60))
        return f'{int(mn)}:{sc}'
