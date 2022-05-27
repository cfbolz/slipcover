import threading

class Tracker:
    def __init__(self, sci, filename, lineno, d_threshold):
        self._sci = sci
        self._filename = filename
        self._lineno = lineno
        self._signalled = False
        self._instrumented = True
        self._d_miss_count = -1
        self._u_miss_count = 0
        self._hit_count = 0
        self._d_threshold = d_threshold
        self._lock = threading.RLock()


def hit(t):
    with t._lock:
        t._hit_count += 1

def signal(t):
    with t._lock:
        if not t._signalled:
            t._signalled = True
            t._sci.new_lines_seen[t._filename].add(t._lineno)
        if t._instrumented:
            t._d_miss_count += 1
            if t._d_miss_count == t._d_threshold:
                t._sci.deinstrument_seen()
        else:
            t._u_miss_count += 1

def register(sci, filename, lineno, d_threshold):
    return Tracker(sci, filename, lineno, d_threshold)

def deinstrument(t):
    with t._lock:
        t._instrumented = False

def get_stats(t):
    return (t._filename, t._lineno, max(t._d_miss_count, 0),
            t._u_miss_count, 1 + t._d_miss_count + t._u_miss_count + t._hit_count)

