"""Cambio mínimo de monedas con suministro ilimitado mediante programación dinámica."""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from math import inf
from typing import Iterable, Literal

Decision = Literal["U", "L"]


@dataclass(frozen=True)
class CoinChangeResult:
    coins: tuple[int, ...]
    amount: int
    costs: tuple[tuple[float, ...], ...]
    paths: tuple[tuple[tuple[Decision, ...], ...], ...]

    @property
    def minimum_coins(self) -> int | None:
        value = self.costs[-1][-1]
        return None if value == inf else int(value)

    def one_solution(self) -> list[int] | None:
        """Reconstruye una combinación óptima; devuelve None si no existe."""
        if self.minimum_coins is None:
            return None
        i, j = len(self.coins), self.amount
        result: list[int] = []
        while j > 0 and i > 0:
            choices = self.paths[i][j]
            if "L" in choices:
                coin = self.coins[i - 1]
                result.append(coin)
                j -= coin
            elif "U" in choices:
                i -= 1
            else:
                raise RuntimeError(f"Sin decisión de reconstrucción en ({i}, {j})")
        if j != 0:
            raise RuntimeError("No fue posible reconstruir una solución factible")
        return result

    def all_solutions(self, limit: int = 1000) -> list[list[int]]:
        """Enumera combinaciones óptimas distintas, hasta el límite indicado."""
        if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
            raise ValueError("limit debe ser un entero positivo")
        if self.minimum_coins is None:
            return []

        @lru_cache(maxsize=None)
        def visit(i: int, j: int) -> frozenset[tuple[int, ...]]:
            if j == 0:
                return frozenset({()})
            if i == 0:
                return frozenset()
            solutions: set[tuple[int, ...]] = set()
            for decision in self.paths[i][j]:
                if decision == "U":
                    solutions.update(visit(i - 1, j))
                else:
                    coin = self.coins[i - 1]
                    solutions.update(
                        tuple(sorted(solution + (coin,)))
                        for solution in visit(i, j - coin)
                    )
                if len(solutions) >= limit:
                    break
            return frozenset(solutions)

        found = visit(len(self.coins), self.amount)
        return [list(solution) for solution in sorted(found)[:limit]]


def _validate(coins: Iterable[int], amount: int) -> tuple[int, ...]:
    denominations = tuple(coins)
    if not denominations:
        raise ValueError("Se requiere al menos una denominación")
    if any(not isinstance(c, int) or isinstance(c, bool) or c <= 0
           for c in denominations):
        raise ValueError("Las denominaciones deben ser enteros positivos")
    if len(set(denominations)) != len(denominations):
        raise ValueError("No se permiten denominaciones repetidas")
    if not isinstance(amount, int) or isinstance(amount, bool) or amount < 0:
        raise ValueError("El monto debe ser un entero no negativo")
    return denominations


def solve_coin_change(coins: Iterable[int], amount: int) -> CoinChangeResult:
    """Calcula C y P para monedas ilimitadas. C[i][j] es el mínimo número."""
    denominations = _validate(coins, amount)
    n = len(denominations)
    costs = [[inf] * (amount + 1) for _ in range(n + 1)]
    paths: list[list[tuple[Decision, ...]]] = [
        [tuple() for _ in range(amount + 1)] for _ in range(n + 1)
    ]

    for i in range(n + 1):
        costs[i][0] = 0

    for i, coin in enumerate(denominations, start=1):
        for target in range(1, amount + 1):
            if coin > target:
                costs[i][target] = costs[i - 1][target]
                paths[i][target] = (
                    ("U",) if costs[i][target] != inf else tuple()
                )
                continue

            skip = costs[i - 1][target]
            previous = costs[i][target - coin]
            use = inf if previous == inf else 1 + previous
            best = min(skip, use)
            costs[i][target] = best
            decisions: list[Decision] = []
            if skip == best and skip != inf:
                decisions.append("U")
            if use == best and use != inf:
                decisions.append("L")
            paths[i][target] = tuple(decisions)

    return CoinChangeResult(
        coins=denominations,
        amount=amount,
        costs=tuple(tuple(row) for row in costs),
        paths=tuple(tuple(row) for row in paths),
    )


def greedy_change(coins: Iterable[int], amount: int) -> list[int] | None:
    """Heurística voraz de mayor denominación primero; no garantiza óptimo."""
    denominations = _validate(coins, amount)
    result: list[int] = []
    remaining = amount
    for coin in sorted(denominations, reverse=True):
        while coin <= remaining:
            result.append(coin)
            remaining -= coin
    return result if remaining == 0 else None
