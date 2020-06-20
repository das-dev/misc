import bisect


def grade(score, breakpoints=(60, 40, 80, 90), grades='FDCBA'):
    """ Map score to a grade
    >>> [grade(score) for score in [33, 99, 77, 70, 89, 90, 100]]
    ['F', 'A', 'C', 'C', 'B', 'A', 'A']

    :param score: score value
    :param breakpoints: points where the grade changes
    :param grades: grade change points
    :return: grade value
    """
    i = bisect.bisect(breakpoints, score)
    return grades[i]


if __name__ == '__main__':
    import doctest
    doctest.testmod()
