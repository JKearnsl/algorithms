"""
    Задача о рюкзаке: дискретная

"""


def knapsack(weights: list, values: list, capacity: int) -> int:
    """
        Решение задачи о рюкзаке: дискретная

        :param weights: веса предметов
        :param values: ценности предметов
        :param capacity: вместимость рюкзака
        :return: максимальная ценность предметов, которые можно унести в рюкзаке
    """
    n = len(values)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(n + 1):
        for w in range(capacity + 1):
            if i == 0 or w == 0:
                dp[i][w] = 0
            elif weights[i - 1] <= w:
                dp[i][w] = max(values[i - 1] + dp[i - 1][w - weights[i - 1]], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]

    return dp[n][capacity]
