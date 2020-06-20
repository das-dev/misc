class Averager:

    def __init__(self):
        self.count = 0
        self.total = 0

    def __call__(self, new_value):
        self.count += 1
        self.total += new_value
        return self.total / self.count


def make_averager():
    count = 0
    total = 0

    def averager(val):
        nonlocal count, total
        count += 1
        total += val
        return total / count
    return averager


if __name__ == '__main__':
    averager1 = Averager()
    averager2 = make_averager()
    assert averager1(10) == averager2(10)
    assert averager1(11) == averager2(11)
    assert averager1(12) == averager2(12)
