from functools import lru_cache
from fluent_python.chapter_7.clock_deco import clock


if __name__ == '__main__':
    @lru_cache()
    @clock
    def fib(n):
        if n < 2:
            return n
        return fib(n - 2) + fib(n - 1)

    print(fib(6))
