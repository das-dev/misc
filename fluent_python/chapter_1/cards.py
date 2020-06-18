from collections import namedtuple
from itertools import product
from random import choice, seed

Card = namedtuple('Card', ['rank', 'suit'])
suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)


def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]


class FrenchDeck:
    """ Implement object API through special methods
    >>> deck = FrenchDeck()
    >>> len(deck)
    52
    >>> deck[0]
    Card(rank='2', suit='spades')
    >>> deck[-1]
    Card(rank='A', suit='hearts')
    >>> deck[-3:]
    [Card(rank='Q', suit='hearts'), Card(rank='K', suit='hearts'), Card(rank='A', suit='hearts')]
    >>> deck[12::13]  # doctest: +ELLIPSIS
    [Card(rank='A', suit='spades'), Card(rank='A', suit='diamonds'), Card(rank='A', suit='clubs'), ...
    >>> seed(1)
    >>> choice(deck)
    Card(rank='10', suit='spades')
    >>> for card in sorted(deck, key=spades_high):  # doctest: +ELLIPSIS
    ...     print(card)
    Card(rank='2', suit='clubs')
    Card(rank='2', suit='diamonds')
    Card(rank='2', suit='hearts')
    ...
    Card(rank='A', suit='diamonds')
    Card(rank='A', suit='hearts')
    Card(rank='A', suit='spades')
    """

    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()
    #

    def __init__(self):
        self._cards = [Card(rank, suit) for suit, rank in product(self.suits, self.ranks)]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]


if __name__ == '__main__':
    import doctest
    doctest.testmod()
