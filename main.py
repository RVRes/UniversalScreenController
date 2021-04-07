import sys
import sysm
import time
from pyscreeze import Box
import threading


class MFW():
    def __init__(self):
        self.imgdir = 'IMG'
        self.sceenshotsdir = 'SCREENSHOTS'
        self.bobber_img_prefix = 'bobber_'
        self.throw_rod_img = self.imgdir + '/' + 'throw_rod.png'
        self.fish_cought_img = self.imgdir + '/' + 'fish_cought.png'
        self.grab_fish_img = self.imgdir + '/' + 'grab_fish.png'
        self.close_quest_img = self.imgdir + '/' + 'close_quest_completed.png'
        self.overextension_img = self.imgdir + '/' + 'overextension.png'
        self.count = {'hard': 0, 'success': 0, 'fail': 0, 'skip': 0}
        self.game_size = {'x': 640, 'y': 360}
        self.start_time = time.monotonic()
        self.game_area = None
        self.throw_rod_region = None
        self.push_rod_region = None
        self.bobber_region = None
        self.extension_region = None
        self.bobber_img = None
        self.bobbers_list = None

    def start(self):
        sysm.clearscreen()
        print(sysm.get_time() + '  Starting the MFW game.')
        deadline = time.monotonic() + 2 * 60 * 60
        while time.monotonic() < deadline:
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

    def init_regions(self):
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
        print(sysm.get_time() +
              '  Fishing. speed: ' + fish_per_minute +
              ' f/m  ', 'hard:', self.count['hard'],
              'success:', self.count['success'],
              'fail:', self.count['fail'],
              'skip', self.count['skip'])

    def pull_bobber(self):

        def _pull_bobber_thread(bobber):
            nonlocal bobber_found
            nonlocal bobber_candidate
            nonlocal stop_threads
            while not stop_threads:
                # print(sysm.get_time() + '  ' + bobber)
                ans = sysm.check_bobber(self.imgdir + '/' + bobber, self.bobber_region)
                if ans:
                    # print(sysm.get_time() + '  ' + bobber + ' TRUE!!')
                    bobber_found = True
                    if not bobber_candidate and not self.bobber_img:
                        bobber_candidate = bobber


        def _start_bobber_threads():
            thr = []
            nonlocal stop_threads
            stop_threads = False
            if not self.bobber_img:
                for bobber_img in self.bobbers_list:
                    thr.append(threading.Thread(target=_pull_bobber_thread, args=(bobber_img,), daemon=True))
                    thr[-1].start()
                    time.sleep(0.05)
            else:
                for i in range(2):
                    thr.append(threading.Thread(target=_pull_bobber_thread, args=(self.bobber_img,), daemon=True))
                    thr[-1].start()
                    time.sleep(0.1)
            return thr

        def _stop_threads(thr):
            # print(sysm.get_time() + '   останавливаем потоки')
            nonlocal stop_threads
            stop_threads = True
            for th in thr:
                th.join()
                # print(sysm.get_time() + '   поток', th.is_alive())

        stop_threads = False
        bobber_candidate = None
        bobber_found = False
        self.print_status()
        threads = _start_bobber_threads()
        catch_timer = None  # таймер включается после нахождения поплавка, чтобы понять, поймана ли рыба.
        bobber_last_seen_timer = time.monotonic() + 60  # если за 30 секунд не найдем поплавок, начнем перебор всех заново

        # print(threads, type(threads[0]))
        while True:
            if bobber_found and not catch_timer:
                print(sysm.get_time() + '  ..pulling')
                sysm.clickoncoord(self.push_rod_region)
                catch_timer = time.monotonic() + 7
                bobber_last_seen_timer = time.monotonic() + 30

            if catch_timer:
                fish_cought = sysm.findpiconregion(self.fish_cought_img, self.game_area)
                # print('проверяем поймана ли рыба')
                if fish_cought:
                    # print('поймана')
                    self.count['success'] += 1
                    print(sysm.get_time() + '  ..success')
                    _stop_threads(threads)
                    return True
                if bobber_candidate and not self.bobber_img:
                    self.bobber_img = bobber_candidate
                    bobber_candidate = None
                    _stop_threads(threads)
                    threads = _start_bobber_threads()
                    print(sysm.get_time() + '  ..new bobber: ', self.bobber_img)

                if time.monotonic() > catch_timer:
                    # print('сбросили таймер поиска')
                    catch_timer = None
                    bobber_found = False
                    self.count['fail'] += 1
                    print(sysm.get_time() + '  ..fail')

            if time.monotonic() > bobber_last_seen_timer and self.bobber_img:
                # print ('сброслили поплавок')
                self.bobber_img = None
                _stop_threads(threads)
                threads = _start_bobber_threads()

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


game = MFW()

game.start()

# game.make_screenshot()
