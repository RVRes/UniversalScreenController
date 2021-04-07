import sysm
import pyautogui
from Logger import time_of_function
import time, sys
import threading


# for i in range(10):
#     sys.stdout.write("\r")
#     sys.stdout.write('#')
#     sys.stdout.flush()
#     time.sleep(.3)
# sys.stdout.write('\n')

@time_of_function
def tst_function():
    test = {
        'iterations': 100,
        'screens': sysm.find_files_list('progress_', 'Temp'),
        'samples': sysm.find_files_list('pb_', 'Temp'),
        'speeds': [],
        'average_speed': [],
        'errors': []
    }

    total_iterations = test['iterations'] * len(test['screens']) * len(test['samples'])
    counter = 0
    percent = 999

    for sm in range(len(test['samples'])):
        test['speeds'].append([])
        test['errors'].append(0)
        test['average_speed'].append(999)

    for i in range(0, test['iterations']):
        for sc in range(len(test['screens'])):
            for sm in range(len(test['samples'])):
                counter += 1
                cur_percent = int(counter / total_iterations * 100)
                if percent != cur_percent:
                    percent = cur_percent
                    sys.stdout.write('\r')
                    sys.stdout.write(str(percent) + '    ')
                    sys.stdout.flush()
                t1 = time.monotonic()
                a = pyautogui.locate('temp/' + test['samples'][sm], 'temp/' + test['screens'][sc], confidence=0.9,
                                     grayscale=True)
                # a = pyautogui.locate('IMG/fish_cought.png', 'IMG/' + test['screens'][sc], grayscale=False)
                test['speeds'][sm].append(time.monotonic() - t1)
                if not a:
                    test['errors'][sm] += 1

    for sm in range(len(test['samples'])):
        test['average_speed'][sm] = int(sum(test['speeds'][sm]) / len(test['speeds'][sm]) * 100000) / 100000

    print()
    for sm in range(len(test['samples'])):
        print(test['samples'][sm], 'speed:', test['average_speed'][sm], 'errors:', test['errors'][sm])


@time_of_function
def tst_function_thread():
    def _test_thread():
        t1 = time.monotonic()

        a = pyautogui.locate('temp/' + test['samples'][sm], 'temp/' + test['screens'][sc], confidence=0.9,
                             grayscale=True)

        test['speeds'][sm].append(time.monotonic() - t1)
        if not a:
            test['errors'][sm] += 1



    test = {
        'iterations': 100,
        'screens': sysm.find_files_list('progress_', 'Temp'),
        'samples': sysm.find_files_list('pb_', 'Temp'),
        'speeds': [],
        'average_speed': [],
        'errors': []
    }

    total_iterations = test['iterations'] * len(test['screens']) * len(test['samples'])
    counter = 0
    percent = 999
    t = []

    for sm in range(len(test['samples'])):
        test['speeds'].append([])
        test['errors'].append(0)
        test['average_speed'].append(999)

    for i in range(0, test['iterations']):
        for sc in range(len(test['screens'])):
            for sm in range(len(test['samples'])):
                counter += 1
                cur_percent = int(counter / total_iterations * 100)
                if percent != cur_percent:
                    percent = cur_percent
                    sys.stdout.write('\r')
                    sys.stdout.write(str(percent) + '    ')
                    sys.stdout.flush()
                t.append(threading.Thread(target=_test_thread, args=()))
                t[sm].start()
            for sm in range(len(test['samples'])):
                t[sm].join()
            t=[]


    for sm in range(len(test['samples'])):
        test['average_speed'][sm] = int(sum(test['speeds'][sm]) / len(test['speeds'][sm]) * 100000) / 100000

    print()
    for sm in range(len(test['samples'])):
        print(test['samples'][sm], 'speed:', test['average_speed'][sm], 'errors:', test['errors'][sm])


tst_function_thread()
tst_function()
