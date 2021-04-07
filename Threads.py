from Logger import time_of_function
import threading
import time

# @time_of_function
# def write_million_str_in_file_threads():
#     t0 = threading.Thread(target=writerB, args=('test0.txt', 1000000,))
#     t1 = threading.Thread(target=writerB, args=('test1.txt', 1000000,))
#     t2 = threading.Thread(target=writerB, args=('test2.txt', 1000000,))
#     t3 = threading.Thread(target=writerB, args=('test3.txt', 1000000,))
#     t4 = threading.Thread(target=writerB, args=('test4.txt', 1000000,))
#     t5 = threading.Thread(target=writerB, args=('test5.txt', 1000000,))
#     t6 = threading.Thread(target=writerB, args=('test6.txt', 1000000,))
#     t7 = threading.Thread(target=writerB, args=('test7.txt', 1000000,))
#     t8 = threading.Thread(target=writerB, args=('test8.txt', 1000000,))
#     t9 = threading.Thread(target=writerB, args=('test9.txt', 1000000,))
#
#     t0.start()
#     t1.start()
#     t2.start()
#     t3.start()
#     t4.start()
#     t5.start()
#     t6.start()
#     t7.start()
#     t8.start()
#     t9.start()
#
#     t0.join()
#     t1.join()
#     t2.join()
#     t3.join()
#     t4.join()
#     t5.join()
#     t6.join()
#     t7.join()
#     t8.join()
#     t9.join()


def test_thread_access_to_var():
    signal = False

    def _thredfunc1():
        while True:
            time.sleep(1)
            nonlocal signal
            signal = True

    a = threading.Thread(target=_thredfunc1, args=())
    b = threading.Thread(target=_thredfunc1, args=())

    a.start()
    time.sleep(0.5)
    b.start()

    i = 50
    while i>0:
        if signal:
            print(time.strftime('%H:%M:%S', time.localtime()), '   Signal')
            signal = False
            i -= 1



test_thread_access_to_var()