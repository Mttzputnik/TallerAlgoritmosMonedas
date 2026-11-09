import unittest

from src.coin_change import greedy_change, solve_coin_change


class CoinChangeTests(unittest.TestCase):
    def test_greedy_counterexample(self):
        result = solve_coin_change([1, 5, 6, 9], 11)
        self.assertEqual(result.minimum_coins, 2)
        self.assertEqual(sorted(result.one_solution()), [5, 6])
        self.assertEqual(len(greedy_change([1, 5, 6, 9], 11)), 3)

    def test_unlimited_coins_reuse_same_row(self):
        result = solve_coin_change([1, 5, 6, 9], 10)
        self.assertEqual(result.costs[2][10], 2)
        self.assertIn(sorted(result.one_solution()), ([1, 9], [5, 5]))
        self.assertEqual(result.minimum_coins, 2)

    def test_unreachable_amount(self):
        result = solve_coin_change([3, 5], 1)
        self.assertIsNone(result.minimum_coins)
        self.assertIsNone(result.one_solution())
        self.assertEqual(result.all_solutions(), [])

    def test_tie_keeps_both_decisions_and_solutions(self):
        result = solve_coin_change([1, 2, 3], 4)
        self.assertEqual(result.minimum_coins, 2)
        self.assertCountEqual(result.all_solutions(), [[1, 3], [2, 2]])
        self.assertEqual(set(result.paths[3][4]), {"U", "L"})

    def test_zero_amount(self):
        result = solve_coin_change([2, 3], 0)
        self.assertEqual(result.minimum_coins, 0)
        self.assertEqual(result.one_solution(), [])
        self.assertEqual(greedy_change([2, 3], 0), [])

    def test_greedy_rejects_invalid_inputs(self):
        invalid = [([], 4), ([0, 2], 4), ([1, 1], 4),
                   ([1.5, 2], 4), ([1, 2], -1), ([1, 2], 2.5)]
        for coins, amount in invalid:
            with self.subTest(coins=coins, amount=amount):
                with self.assertRaises(ValueError):
                    greedy_change(coins, amount)

    def test_invalid_inputs(self):
        invalid = [([], 4), ([0, 2], 4), ([1, 1], 4),
                   ([1, 2], -1), ([1, 2], 2.5), ([True, 2], 4)]
        for coins, amount in invalid:
            with self.subTest(coins=coins, amount=amount):
                with self.assertRaises(ValueError):
                    solve_coin_change(coins, amount)

    def test_invalid_solution_limit(self):
        result = solve_coin_change([1, 2], 2)
        with self.assertRaises(ValueError):
            result.all_solutions(0)


if __name__ == "__main__":
    unittest.main()
