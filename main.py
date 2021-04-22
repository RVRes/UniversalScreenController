import sys
import sysm
import time
from pyscreeze import Box
import keyboard
import threading
from multiprocessing import Process, Queue, current_process, freeze_support


class MFW():
    def __init__(self):
        self.cpu_specs_func = {
            'high_cpu': {
                'pull_bobber': self.pull_bobber_highload
            },
            'weak_cpu': {
                'pull_bobber': self.pull_bobber_weakload
            },
        }
        self.cpu_specs = 'weak_cpu'
        self.pull_bobber = self.cpu_specs_func[self.cpu_specs]['pull_bobber']
        self.imgdir = 'IMG'
        self.sceenshotsdir = 'SCREENSHOTS'
        self.bobber_img_prefix = 'bobber_'
        self.throw_rod_img = self.imgdir + '/' + 'throw_rod.png'
        self.fish_cought_img = self.imgdir + '/' + 'fish_cought.png'
        self.grab_fish_img = self.imgdir + '/' + 'grab_fish.png'
        self.close_quest_img = self.imgdir + '/' + 'close_quest_completed.png'
        self.overextension_img = self.imgdir + '/' + 'overextension.png'
        self.count = {'hard': 0, 'success': 0, 'fail': 0, 'skip': 0}
        # self.game_size = {'x': 640, 'y': 360}
        self.game_size = {'x': 400, 'y': 300}
        self.start_time = time.monotonic()
        self.game_area = None
        self.throw_rod_region = None
        self.push_rod_region = None
        self.bobber_region = None
        self.extension_region = None
        self.bobber_img = None
        self.bobbers_list = None
        self.sysexit_flag = False

    def start(self):
        sysm.set_console_size_and_color(50, 20, 'color 0A')
        sysm.clearscreen()
        t = self._start_keyboard_listener()
        print(sysm.get_time() + '  Starting the MFW game.')
        print(f'{sysm.get_time()}  {t}')
        deadline = time.monotonic() + 2 * 60 * 60
        while time.monotonic() < deadline:
            self._game_exit_check()
            fish_on_hook = False
            rod_throwed = self.throw_rod()
            if self.throw_rod_region and rod_throwed:
                fish_on_hook = self.pull_bobber()
            if fish_on_hook:
                self.pull_fish()
            time.sleep(1)
            if self.throw_rod_region and sysm.findpiconregion(self.close_quest_img, self.game_area):
                sysm.clickonpic(self.close_quest_img, self.game_area)
                time.sleep(1)
            if self.throw_rod_region and sysm.findpiconregion(self.grab_fish_img, self.game_area):
                sysm.clickonpic(self.grab_fish_img, self.game_area)
                time.sleep(1)

    def _start_keyboard_listener(self):
        # keyboard.add_hotkey('Ctrl + e', lambda: print('Hello'))
        keyboard.add_hotkey('Ctrl + e', self._game_exit_flag_on)
        keyboard.add_hotkey('Ctrl + p', sysm.game_pause)
        text = 'CTL+E to Exit, CTL+P to Pause'
        return text

    def _game_exit_flag_on(self):
        print('exiting..')
        self.sysexit_flag = True

    def _game_exit_check(self):
        if self.sysexit_flag:
            sys.exit()

    def _init_400x300(self):
        # кнопка подъема удочки (равна кнопке заброса)
        s = self.throw_rod_region
        # sysm.screenshot_with_region(self.sceenshotsdir + '/scr_throw_rod_region.png', s)
        self.push_rod_region = Box(left=s.left, top=s.top, width=s.width, height=s.height)
        # экран игры
        l = self.throw_rod_region.left - self.game_size['x'] + 60
        t = self.throw_rod_region.top + self.throw_rod_region.height - self.game_size['y'] + 20
        w = self.game_size['x'] - 4
        h = self.game_size['y']
        self.game_area = Box(left=l, top=t, width=w, height=h)
        # sysm.screenshot_with_region(self.sceenshotsdir + '/scr_gamearea.png', self.game_area)
        # зона погруженного поплавка
        self.bobber_region = Box(left=s.left + 10, top=s.top - 124, width=31, height=29)
        # sysm.screenshot_with_region(self.sceenshotsdir + '/scr_bobber_region.png', self.bobber_region)
        # Составляем список поплавков
        self.bobbers_list = sysm.find_files_list(self.bobber_img_prefix, self.imgdir)
        # зона проверки натяжения удочки
        self.extension_region = Box(left=s.left - 26, top=s.top - 117, width=80, height=44)
        # sysm.screenshot_with_region(self.sceenshotsdir + '/scr_extension_region.png', self.extension_region)

    def _init_640x360(self):
        # кнопка подъема удочки (равна кнопке заброса)
        s = self.throw_rod_region
        self.push_rod_region = Box(left=s.left, top=s.top, width=s.width, height=s.height)
        # экран игры
        l = self.throw_rod_region.left - self.game_size['x'] + 85
        t = self.throw_rod_region.top + self.throw_rod_region.height - self.game_size['y'] + 30
        w = self.game_size['x'] - 5
        h = self.game_size['y']
        self.game_area = Box(left=l, top=t, width=w, height=h)
        # sysm.screenshot_with_region(self.sceenshotsdir + '/scr_region_1.png', self.game_area)
        # зона погруженного поплавка
        self.bobber_region = Box(left=s.left + 12, top=s.top - 183, width=53, height=47)
        # sysm.screenshot_with_region(self.sceenshotsdir + '/scr_region_2.png', self.bobber_region)
        # Составляем список поплавков
        self.bobbers_list = sysm.find_files_list(self.bobber_img_prefix, self.imgdir)
        # зона проверки натяжения удочки
        self.extension_region = Box(left=s.left - 31, top=s.top - 181, width=105, height=76)
        # sysm.screenshot_with_region(self.sceenshotsdir + '/scr_region_4.png', self.extension_region)

    def init_regions(self):
        self._init_400x300()
        # sys.exit(0)

    def throw_rod(self):
        if not self.throw_rod_region:
            self.throw_rod_region = sysm.findpiconscreen(self.throw_rod_img)
            if self.throw_rod_region:
                self.init_regions()
                print(sysm.get_time() + '  Game regions init completed.')
            else:
                return False
        if self.throw_rod_region:
            res = sysm.clickonpic(self.throw_rod_img, self.throw_rod_region)
            if not res:
                res = sysm.clickonpic(self.throw_rod_img, self.throw_rod_region)
            time.sleep(5)
            if res:
                return True
            else:
                return False

    def make_screenshot(self):
        t = time.localtime()
        ts = str(time.strftime("%H%M%S", t))
        sysm.makescreenshot(self.sceenshotsdir + '/' + ts + '.png')

    def print_status(self):
        timedelta = (time.monotonic() - self.start_time) / 60
        fish_per_minute = str(int((self.count['success'] / timedelta) * 10) / 10)
        print(f"{sysm.get_time()}  Fishing. speed: {fish_per_minute} f/m  miss: {self.count['fail']}"
              f"\n          hard: {self.count['hard']}  success: {self.count['success']}  skip: {self.count['skip']}")

    def _pull_bobber_thread(self, input, output):
        for args in iter(input.get, 'STOP'):
            bobber, bobber_region = args
            ans = sysm.check_bobber(bobber, bobber_region)
            if ans:
                output.put(bobber)

    def _bobber_is_eaten(self, deltatime):
        print(sysm.get_time() + '  ..pulling')
        sysm.clickoncoord(self.push_rod_region)
        catch_timer = time.monotonic() + deltatime

        while time.monotonic() < catch_timer:
            fish_cought = sysm.findpiconregion(self.fish_cought_img, self.game_area)
            if fish_cought:
                # print('поймана')
                self.count['success'] += 1
                print(sysm.get_time() + '  ..success')
                return True
        # не поймали
        self.count['fail'] += 1
        print(sysm.get_time() + '  ..fail')
        return False

    def _update_bobber_img(self, bobber_img):
        if self.bobber_img != bobber_img:
            print(f'{sysm.get_time()}  ..new bobber:  {bobber_img}')
            self.bobber_img = bobber_img

    def _drop_wrong_bobbers(self):
        # прибиваем поплавки, которые срабатывают не в нужный момент
        for i in range(2):
            for bobber_img in self.bobbers_list:
                if sysm.check_bobber(f'{self.imgdir}/{bobber_img}', self.bobber_region):
                    self.bobbers_list.remove(bobber_img)
                    # print(f'.. убрали {bobber_img}')

    def pull_bobber_highload(self):

        NUMBER_OF_PROCESSES = 2
        task_queue = Queue()
        done_queue = Queue()
        delta_timer_catch = 7
        self.print_status()

        bobber_last_seen_timer = time.monotonic() + 60  # если за 30 секунд не найдем поплавок, начнем перебор всех заново

        self._drop_wrong_bobbers()

        # print('запускаем процесс')
        for i in range(NUMBER_OF_PROCESSES):
            Process(target=self._pull_bobber_thread, args=(task_queue, done_queue)).start()

        while True:
            while done_queue.qsize() > 0:
                done_queue.get()

            # ищем поплавок под водой. когда найдем, выходим
            while done_queue.qsize() == 0:
                self._game_exit_check()
                if task_queue.qsize() < NUMBER_OF_PROCESSES:
                    for bobber_img in self.bobbers_list:
                        if self.bobber_img:
                            task = (self.imgdir + '/' + self.bobber_img, self.bobber_region)
                        else:
                            task = (self.imgdir + '/' + bobber_img, self.bobber_region)
                        task_queue.put(task)
                if time.monotonic() > bobber_last_seen_timer and self.bobber_img:
                    self.bobber_img = None  # print ('сброслили поплавок')

            # проверяем смену поплавка
            bobber_last_seen_timer = time.monotonic() + 60
            bobber_img = done_queue.get().split('/')[1]
            self._update_bobber_img(bobber_img)

            # проверяем поймана ли рыба
            if self._bobber_is_eaten(delta_timer_catch):
                for i in range(NUMBER_OF_PROCESSES):
                    task_queue.put('STOP')
                return True

    def pull_bobber_weakload(self):
        def get_next_bobber(bobber=None):
            if self.bobber_img:
                return self.bobber_img
            count = (len(self.bobbers_list) - 1 if not bobber else self.bobbers_list.index(bobber))
            count = (count + 1, 0)[count == len(self.bobbers_list) - 1]
            return self.bobbers_list[count]

        delta_timer_catch = 7
        delta_timer = 60
        bobber_last_seen_timer = time.monotonic() + delta_timer
        bobber_img = self.bobber_img
        bobber_found = False

        self._drop_wrong_bobbers()
        self.print_status()
        while True:
            while not bobber_found:
                self._game_exit_check()
                bobber_img = get_next_bobber(bobber_img)
                bobber_found = sysm.check_bobber(f'{self.imgdir}/{bobber_img}', self.bobber_region)
                # print(f'{self.imgdir}/{bobber_img}')
                if time.monotonic() > bobber_last_seen_timer and self.bobber_img:
                    self.bobber_img = None

            # print(f'{self.imgdir}/{bobber_img}')
            bobber_last_seen_timer = time.monotonic() + delta_timer
            self._update_bobber_img(bobber_img)

            # проверяем поймана ли рыба
            if self._bobber_is_eaten(delta_timer_catch):
                return True
            bobber_found = False

    def close_buttons(self):
        a = False
        if sysm.findpiconregion(self.close_quest_img, self.game_area):
            sysm.mouseup()
            sysm.clickonpic(self.close_quest_img, self.game_area)
            time.sleep(1)
            a = True
        if sysm.findpiconregion(self.grab_fish_img, self.game_area):
            sysm.mouseup()
            sysm.clickonpic(self.grab_fish_img, self.game_area)
            time.sleep(1)
            a = True
        return a

    def pull_fish(self):
        def test_fish_strenght():
            time.sleep(0.5)
            overextension = 0
            for i in range(1, 5):
                sysm.clickandholdoncoord(self.push_rod_region, i / 3 - 0.1)
                if sysm.findpiconregion(self.overextension_img, self.extension_region):
                    overextension = 6 - i  # 0 1 проставляется в след цикле, цем выше, тем быстрее реакция
                    print(sysm.get_time() + '  ..fish power:', overextension)
                    time.sleep(0.6)
                    return overextension
                time.sleep(0.2)
            print(sysm.get_time() + '  ..fish power:', overextension)
            time.sleep(0.2)
            return overextension

        def weakening_fish(overextension):
            work_time = 0.50
            if overextension < 3:
                work_time = 0.60
            sleep_time = work_time - 0.05
            print(sysm.get_time() + '  ..weakening')
            timelimit = 35
            deadline = time.monotonic() + timelimit
            while time.monotonic() < deadline:
                print(int(deadline - time.monotonic()))
                sysm.mousedownoncoord(self.push_rod_region)
                time.sleep(work_time)
                sysm.mouseup()
                time.sleep(sleep_time)
            work_time += 0.2
            sleep_time += 0.1
            deadline = time.monotonic() + timelimit
            print(sysm.get_time() + '  ..catch hard')
            while time.monotonic() < deadline:
                print(int(deadline - time.monotonic()))
                sysm.mousedownoncoord(self.push_rod_region)
                time.sleep(work_time)
                sysm.mouseup()
                time.sleep(sleep_time)

        overextension = test_fish_strenght()
        if 0 < overextension < 4:
            weakening_fish(overextension)
            if self.close_buttons():
                print(sysm.get_time() + '  ..success')
                self.count['success'] -= 1
                self.count['hard'] += 1
                return True
            else:
                print(sysm.get_time() + '  ..too hard')
                self.count['success'] -= 1
                self.count['skip'] += 1
                return False
        elif overextension >= 4:
            print(sysm.get_time() + '  ..too hard')
            self.count['success'] -= 1
            self.count['skip'] += 1
            return False
        timelimit = 30
        starttime = time.monotonic()
        deadline = starttime + timelimit
        mouseup = True
        plug_in = 0
        plug_in_increament = 0.1

        print(sysm.get_time() + '  ..catch weak')
        while time.monotonic() < deadline:

            if mouseup and time.monotonic() > plug_in:
                sysm.mousedownoncoord(self.push_rod_region)
                mouseup = False
            if not mouseup and sysm.findpiconregion(self.overextension_img, self.extension_region):
                sysm.mouseup()
                mouseup = True

                if plug_in_increament < 0.8: plug_in_increament += 0.1
                if time.monotonic() - starttime < 2: plug_in_increament += 0.5
                plug_in = time.monotonic() + plug_in_increament
                # print(int(deadline - time.monotonic()), '..overextension, wait:', int((plug_in - time.monotonic())*100)/100)
            if time.monotonic() - starttime > 8:
                # print('..searching exit')
                if self.close_buttons():
                    return True

        # sysm.screenshot_with_region(self.sceenshotsdir + '/scr_region_3.png', self.push_rod_region)


if __name__ == '__main__':
    freeze_support()
    game = MFW()
    game.start()

# game.make_screenshot()
