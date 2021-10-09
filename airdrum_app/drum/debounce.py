import functools
import time


def debounce(timeout_ms: int = 1000):
    timeout_ns = timeout_ms * 1e6
    last_execution = time.time_ns()

    def wrap(f):
        @functools.wraps(f)
        def do_debounce(*args, **kwargs):
            nonlocal last_execution
            now = time.time_ns()
            if now - last_execution > timeout_ns:
                last_execution = now
                return f(*args, **kwargs)

        return do_debounce

    return wrap
