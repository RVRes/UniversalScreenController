import time

def time_of_function(function):
    def wrapped(*args):
        t1 = time.monotonic()
        t2 = time.localtime()
        res = function(*args)
        lt = str(time.strftime("%H:%M:%S", t2)) + ' ' + str("%.3f" % (time.monotonic() - t1)) + ': '
        print(lt, function.__name__, args, res)
        return res

    return wrapped