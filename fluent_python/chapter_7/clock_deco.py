import time
from functools import wraps


def clock(func):
    @wraps(func)
    def clocked(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args)
        elapsed = time.perf_counter() - start
        arg_list = []
        if args:
            arg_list.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            pairs = [f'{k}={v}' for k, v in sorted(kwargs.items())]
            arg_list.append(', '.join(pairs))
        arg_str = ', '.join(arg_list)
        print(f'[{elapsed:.8f} {func.__name__}({arg_str}) -> {result}')
        return result
    return clocked


if __name__ == '__main__':
    @clock
    def snooze(seconds):
        time.sleep(seconds)

    snooze(.123)
