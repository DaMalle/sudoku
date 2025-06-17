import unittest, random, logging
from sudoku.model import SolutionGenerator


class TestSolutionGenerator(unittest.TestCase):
    def setUp(self) -> None:
        self.solution = SolutionGenerator().create()
        self.logger = logging.getLogger(__name__)

    def test_format(self):
        self.logger.info("running: test_format")

        self.assertIsInstance(self.solution, tuple)
        self.assertTrue(all(isinstance(row, tuple) for row in self.solution))


        self.assertEqual(len(self.solution), 9)
        self.assertTrue(all(len(row)==9 for row in self.solution))

        self.assertTrue(all(1 <= x <= 9 for row in self.solution for x in row))

    def test_deterministic_with_seed(self):
        self.logger.info("running: test_deterministic_with_seed")

        random.seed(42) # random with fixed seed
        solution1 = SolutionGenerator(rng=random).create()
        random.seed(42) # reset seed
        solution2 = SolutionGenerator(rng=random).create()

        self.assertEqual(solution1, solution2)

    def test_is_valid_row(self):
        self.logger.info("running: test_is_valid_row")

        for i in range(9):
            with self.subTest(i=i):
                self.logger.info(f"running: test_is_valid_row: index{i}")
                self.assertEqual(set(self.solution[i]), set(range(1, 10, 1)))

    def test_is_valid_column(self):
        self.logger.info("running: test_is_valid_column")

        for i in range(9):
            with self.subTest(i=i):
                self.logger.info(f"running: test_is_valid_column: index{i}")
                self.assertEqual(set(self.solution[i][j] for j in range(9)), set(range(1, 10, 1)))

    def test_is_valid_box(self):
        self.logger.info("running: test_is_valid_box")

        for i in range(9):
            with self.subTest(i=i):
                self.logger.info(f"running: test_is_valid_box: index{i}")
                x0 = ()
                self.assertEqual(
                    set(self.solution[((i // 3) * 3 + k)][((i % 3) * 3 + j)]
                        for k in range(3)
                        for j in range(3)),
                    set(range(1, 10, 1))
                )


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
