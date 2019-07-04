import threading
import time

class mailThread(threading.Thread):
    def __init__(self):
        # threading.Thread.__init__()
        super().__init__()
        self._delay_time = 5
    def run(self):
        time.sleep(self._delay_time)
        print('23333%s' % self.name)

if __name__ == '__main__':
    test_thread = mailThread()
    test_thread2 = mailThread()
    test_thread.start()
    test_thread.join()
    test_thread2.start()
    test_thread2.join()