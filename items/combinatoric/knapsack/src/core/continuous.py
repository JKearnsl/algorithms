"""
    Задача о рюкзаке: непрерывная


"""
from typing import List


class Item:
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value
        self.ratio = value / weight


def knapsack(items: List[Item], capacity: int) -> float:
    """
        Задача о рюкзаке: непрерывная

        :param items: список предметов
        :param capacity: вместимость рюкзака
        :return: максимальная стоимость рюкзака
    """
    items.sort(key=lambda x: x.ratio, reverse=True)

    total_value = 0
    for i in items:
        if capacity == 0:
            break
        amount = min(i.weight, capacity)
        total_value += amount * i.ratio
        capacity -= amount

    return total_value
