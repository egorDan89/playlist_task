import threading
import time
from typing import Union
from logger import log


class SongNode:
    def __init__(self, duration_sec: int):
        self.duration_sec = duration_sec
        self.next_node = None
        self.prev_node = None


class Playlist:
    def __init__(self):
        self.head_node = None
        self.cur: Union[SongNode, None] = None
        self.is_playing: bool = False
        self.count: int = 0
        self.is_paused = False
        self.event = threading.Event()
        self.t = None
        self.new_head = None
        self.sec_start = 1

    def add_song(self, data):
        if self.head_node is None:
            new_node = SongNode(data)
            new_node.prev_node = None
            self.head_node = new_node

        else:
            new_node = SongNode(data)
            cur = self.head_node
            while cur.next_node:
                cur = cur.next_node

            cur.next_node = new_node
            new_node.prev_node = cur
            new_node.next_node = None

    def play_song(self):
        self.is_playing = True
        t = threading.current_thread()
        log.info(f'Новый поток {t}')
        for sec in range(self.sec_start, (self.cur.duration_sec - self.count) + 1):

            time.sleep(1)
            if self.is_playing is True and self.is_paused is False:
                self.count += 1
                log.info(f'Продолжительность текущей песни {self.cur.duration_sec}. '
                         f'Сейчас воспроизводится секунда {str(self.count)}')
            else:
                self.head_node = self.cur
                self.sec_start = self.count
                break

    def pause(self):
        if self.cur is not None:
            self.is_paused = True
            self.is_playing = False

    def _play_playlist(self):
        self.cur = self.head_node
        while self.cur:
            self.sec_start = 1
            if self.is_paused is True:
                break
            log.info(f'Воспроизведение песни с продолжительностью {self.cur.duration_sec}.')
            self.play_song()
            if self.is_playing is True:
                self.is_playing = False
                self.count = 0
                self.cur = self.cur.next_node
            else:
                break

    def play(self):
        self.is_paused = False
        if self.t is not None:
            self.t.join()
        self.t = threading.Thread(target=pl._play_playlist)
        self.t.start()

    def next(self):
        log.info(f'Переключено на воспроизведение следующей песни')
        if self.cur is None:
            return
        if self.cur.next_node is None:
            log.info(f'Следующая песня не может быть воспроизведена. '
                     f'Текущая песня с продолжительностью {self.cur.duration_sec} является последней в плейлисте.')
            return
        if self.is_playing is True:
            self.pause()
            self.cur = self.cur.next_node
            self.count = 0
            if self.t is not None:
                self.t.join()
            self.play()

    def prev(self):
        log.info(f'Переключено на воспроизведение предыдущей песни')

        if self.cur is None:
            return
        if self.cur.prev_node is None:
            log.info(f'Предыдущая песня не может быть воспроизведена. '
                     f'Текущая песня с продолжительностью {self.cur.duration_sec} является первой в плейлисте.')
            return

        if self.is_playing is True:
            self.pause()
            self.cur = self.cur.prev_node
            self.count = 0
            if self.t is not None:
                self.t.join()
            self.play()


pl = Playlist()

pl.add_song(5)
pl.add_song(2)
pl.add_song(3)
pl.play()

time.sleep(3)

pl.pause()
pl.prev()
time.sleep(3)
pl.play()
time.sleep(3)

pl.next()
time.sleep(2)
pl.next()
time.sleep(1)
pl.add_song(9)
pl.prev()
time.sleep(10)
pl.next()