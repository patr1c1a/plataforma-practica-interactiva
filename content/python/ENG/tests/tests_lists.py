###########################
# DO NOT MODIFY THIS FILE #
###########################

import unittest
from src.lists import *


class TestsListFunctions(unittest.TestCase):

    def test_multiplication(self):
        test_cases = {
            "Argument used: nums=[1, 2, 3, 4]": [multiplication([1, 2, 3, 4]), 24],
            "Argument used: nums=[0, 3, 7, 9]": [multiplication([0, 3, 7, 9]), 0],
            "Argument used: nums=[]": [multiplication([]), None],
            "Argument used: nums=[1, 1, 1]": [multiplication([1, 1, 1]), 1],
        }
        for test_case, (a, b) in test_cases.items():
            with self.subTest(test_case=test_case):
                self.assertEqual(a, b, test_case)

    def test_greatest_element(self):
        test_cases = {
            "Argument used: strings=['x', 'y', 'z']": [
                greatest_element(["x", "y", "z"]),
                "z",
            ],
            "Argument used: strings=['z', 'y', 'x']": [
                greatest_element(["z", "y", "z"]),
                "z",
            ],
            "Argument used: strings=['abc', 'cba', 'cab', 'bca']": [
                greatest_element(["abc", "cba", "cab", "bca"]),
                "cba",
            ],
            "Argument used: strings=['abc', 'abc', 'abc']": [
                greatest_element(["abc", "abc", "abc"]),
                "abc",
            ],
            "Argument used: strings=[]": [greatest_element([]), None],
        }
        for test_case, (a, b) in test_cases.items():
            with self.subTest(test_case=test_case):
                self.assertEqual(a, b, test_case)

    def test_highest_profit(self):
        test_cases = {
            "Argument used: prices=[70, 53, 15, 23, 41, 30]": [
                highest_profit([70, 53, 15, 23, 41, 30]),
                55,
            ],
            "Argument used: prices=[5, 5, 5, 5, 5]": [
                highest_profit([5, 5, 5, 5, 5]),
                0,
            ],
            "Argument used: prices=[15.6, 12.8, 4, 2.5, 19]": [
                highest_profit([15.6, 12.8, 4, 2.5, 19]),
                16.5,
            ],
            "Argument used: prices=[12, 21]": [highest_profit([12, 21]), 9],
            "Argument used: prices=[21, 12]": [highest_profit([21, 12]), 9],
        }
        for test_case, (a, b) in test_cases.items():
            with self.subTest(test_case=test_case):
                self.assertEqual(a, b, test_case)

    def test_no_duplicates(self):
        test_cases = {
            "Argument used: might_have_duplicates=[3, False, 'a', 1, 1, 2, 4, False, 4]": [
                no_duplicates([3, False, "a", 1, 1, 2, 4, False, 4]),
                [3, "a", 2],
            ],
            "Argument used: might_have_duplicates=[1, 1, 1]": [
                no_duplicates([1, 1, 1]),
                [],
            ],
            "Argument used: might_have_duplicates=['hello', True, 5.1]": [
                no_duplicates(["hello", True, 5.1]),
                ["hello", True, 5.1],
            ],
            "Argument used: might_have_duplicates=[]": [no_duplicates([]), []],
        }
        for test_case, (a, b) in test_cases.items():
            with self.subTest(test_case=test_case):
                self.assertEqual(a, b, test_case)

    def test_percentages_even_odd_numbers(self):
        test_cases = {
            "Argument used: nums=[-5, 3, 2, -4, 7]": [
                percentages_even_odd_numbers([-5, 3, 2, -4, 7]),
                (40.0, 60.0),
            ],
            "Argument used: nums=[1, 1, 1, 1]": [
                percentages_even_odd_numbers([1, 1, 1, 1]),
                (0.0, 100.0),
            ],
            "Argument used: nums=[1, 5]": [
                percentages_even_odd_numbers([1, 5]),
                (0.0, 100.0),
            ],
            "Argument used: nums=[2, 4]": [
                percentages_even_odd_numbers([2, 4]),
                (100.0, 0.0),
            ],
            "Argument used: nums=[1, 2, 3, 4]": [
                percentages_even_odd_numbers([1, 2, 3, 4]),
                (50.0, 50.0),
            ],
        }
        for test_case, (a, b) in test_cases.items():
            with self.subTest(test_case=test_case):
                self.assertEqual(a, b, test_case)

    def test_add_index(self):
        test_cases = {
            "Argument used: nums=[1, 2, 3, 4, 5, 6]": [
                add_index([1, 2, 3, 4, 5, 6]),
                [1, 3, 5, 7, 9, 11],
            ],
            "Argumento usado: numeros=[-6, 4, -2.8, 0]": [
                add_index([-6, 4, -2.8, 0]),
                [-6, 5, 0.8, 3],
            ],
            "Argument used: nums=[0, 0, 0]": [add_index([0, 0, 0]), [0, 1, 2]],
            "Argument used: nums=[]": [add_index([]), []],
        }
        for test_case, (a, b) in test_cases.items():
            with self.subTest(test_case=test_case):
                self.assertEqual(a, b, test_case)

    def test_partial_sums(self):
        test_cases = {
            "Argument used: nums=[4, 6, 10, 7]": [
                partial_sums([4, 6, 10, 7]),
                [4, 10, 20, 27],
            ],
            "Argument used: nums=[1, 1, 1, 1, 1]": [
                partial_sums([1, 1, 1, 1, 1]),
                [1, 2, 3, 4, 5],
            ],
            "Argument used: nums=[1, 2, 3, 4]": [
                partial_sums([1, 2, 3, 4]),
                [1, 3, 6, 10],
            ],
            "Argument used: nums=[]": [partial_sums([]), []],
            "Argument used: nums=[5, 0, 0, 0, 0]": [
                partial_sums([5, 0, 0, 0, 0]),
                [5, 5, 5, 5, 5],
            ],
        }
        for test_case, (a, b) in test_cases.items():
            with self.subTest(test_case=test_case):
                self.assertEqual(a, b, test_case)

    def test_missing_numbers(self):
        test_cases = {
            "Argument used: nums=[5, 0, 2, 9, 8, 12, 9]": [
                missing_numbers([5, 0, 2, 9, 8, 12, 9]),
                [1, 3, 4, 6],
            ],
            "Argument used: nums=[3, 7, 15, 3, 9]": [
                missing_numbers([3, 7, 15, 3, 9]),
                [0, 1, 2, 4],
            ],
            "Argument used: nums=[1, 2, 3, 4]": [missing_numbers([1, 2, 3, 4]), [0]],
            "Argument used: nums=[0, 1, 2, 3]": [missing_numbers([0, 1, 2, 3]), []],
            "Argument used: nums=[5]": [missing_numbers([5]), [0]],
            "Argument used: nums=[]": [missing_numbers([]), []],
        }
        for test_case, (a, b) in test_cases.items():
            with self.subTest(test_case=test_case):
                self.assertEqual(a, b, test_case)

    def test_how_many_are_smaller(self):
        test_cases = {
            "Argument used: nums=[6, 3, 3, 4, 2]": [
                how_many_are_smaller([6, 3, 3, 4, 2]),
                [4, 1, 1, 3, 0],
            ],
            "Argument used: nums=[3, 3, 3, 3]": [
                how_many_are_smaller([3, 3, 3, 3]),
                [0, 0, 0, 0],
            ],
            "Argument used: nums=[]": [how_many_are_smaller([]), []],
            "Argument used: nums=[1]": [how_many_are_smaller([1]), [0]],
        }
        for test_case, (a, b) in test_cases.items():
            with self.subTest(test_case=test_case):
                self.assertEqual(a, b, test_case)

    def test_two_largest(self):
        test_cases = {
            "Argument used: nums=[5, 3, 6, 2, 8]": [
                two_largest([5, 3, 6, 2, 8]),
                (8, 6),
            ],
            "Argument used: nums=[6, 8, 3, 5, 2]": [
                two_largest([6, 8, 3, 5, 2]),
                (8, 6),
            ],
            "Argument used: nums=[5, 3, 2, 8, 6]": [
                two_largest([5, 3, 2, 8, 6]),
                (8, 6),
            ],
            "Argument used: nums=[5, 5, 5, 5]": [two_largest([5, 5, 5, 5]), (5, 5)],
            "Argument used: nums=[1.3, -4, 2.5, 7, -2.2]": [
                two_largest([1.3, -4, 2.5, 7, -2.2]),
                (7, 2.5),
            ],
            "Argument used: nums=[1, 2]": [two_largest([1, 2]), (2, 1)],
        }
        for test_case, (a, b) in test_cases.items():
            with self.subTest(test_case=test_case):
                self.assertEqual(a, b, test_case)

    def test_uno_round(self):
        test_cases = {
            "Arguments used: hand=['red 2', 'blue 5', 'green 1'], card_discard_pile='red 3'": [
                uno_round(["red 2", "blue 5", "green 1"], "red 3"),
                True,
            ],
            "Arguments used: hand=['red 2', 'blue 5', 'green 1'], card_discard_pile='yellow 3'": [
                uno_round(["red 2", "blue 5", "green 1"], "yellow 3"),
                False,
            ],
            "Arguments used: hand=['green 4'], card_discard_pile='yellow 4'": [
                uno_round(["green 4"], "yellow 4"),
                True,
            ],
            "Arguments used: hand=['green 1'], card_discard_pile='green 6'": [
                uno_round(["green 1"], "green 6"),
                True,
            ],
            "Arguments used: hand=['green 1'], card_discard_pile='blue 5'": [
                uno_round(["green 1"], "blue 5"),
                False,
            ],
            "Argument used: hand=[], card_discard_pile='blue 5'": [
                uno_round([], "blue 5"),
                False,
            ],
        }
        for test_case, (a, b) in test_cases.items():
            with self.subTest(test_case=test_case):
                self.assertEqual(a, b, test_case)

    def test_discard_excess_occurrences(self):
        test_cases = {
            "Arguments used: nums=[1, 2, 3, 2, 3, 3], maximum=1": [
                discard_excess_occurrences([1, 2, 3, 2, 3, 3], 1),
                [1, 2, 3],
            ],
            "Arguments used: nums=[1, 2, 3, 2, 3, 3], maximum=3": [
                discard_excess_occurrences([1, 2, 3, 2, 3, 3], 3),
                [1, 2, 3, 2, 3, 3],
            ],
            "Arguments used: nums=[7, 4, 5, 4, 4, 7, 8, 4, 5], maximum=2": [
                discard_excess_occurrences([7, 4, 5, 4, 4, 7, 8, 4, 5], 2),
                [7, 4, 5, 4, 7, 8, 5],
            ],
            "Arguments used: nums=[1, 1, 1, 1, 1, 1], maximum=0": [
                discard_excess_occurrences([1, 1, 1, 1, 1, 1], 0),
                [],
            ],
            "Arguments used: nums=['a', 'a', 'a'], maximum=1": [
                discard_excess_occurrences(["a", "a", "a"], 1),
                ["a"],
            ],
            "Arguments used: nums=[], maximum=1": [
                discard_excess_occurrences([], 1),
                [],
            ],
        }
        for test_case, (a, b) in test_cases.items():
            with self.subTest(test_case=test_case):
                self.assertEqual(a, b, test_case)

    def test_is_shifted(self):
        test_cases = {
            "Arguments used: nums1=[1, 2, 3, 4], nums2=[3, 4, 1, 2], n=2": [
                is_shifted([1, 2, 3, 4], [3, 4, 1, 2], 2),
                True,
            ],
            "Arguments used: nums1=[1, 2], nums2=[3, 4], n=1": [
                is_shifted([1, 2], [3, 4], 1),
                False,
            ],
            "Arguments used: nums1=[1, 2, 3, 4], nums2=[1, 2, 3, 4], n=0": [
                is_shifted([1, 2, 3, 4], [1, 2, 3, 4], 0),
                True,
            ],
            "Arguments used: nums1=[6.2, 8, -3, 1, 2.4], nums2=[1, 2.4, -3, 8, 6.2], n=5": [
                is_shifted([6.2, 8, -3, 1, 2.4], [1, 2.4, -3, 8, 6.2], 5),
                False,
            ],
            "Arguments used: nums1=[6.2, 8, -3, 1, 2.4], nums2=[6.2, 8, -3, 1, 2.4], n=5": [
                is_shifted([6.2, 8, -3, 1, 2.4], [6.2, 8, -3, 1, 2.4], 5),
                True,
            ],
            "Arguments used: nums1=[4, 4], nums2=[4, 4], n=3": [
                is_shifted([4, 4], [4, 4], 3),
                True,
            ],
            "Arguments used: nums1=[7, 1.1, 0, -8, 9.15], nums2=[9.15, 7, 1.1, 0, 3], n=1": [
                is_shifted([7, 1.1, 0, -8, 9.15], [9.15, 7, 1.1, 0, 3], 1),
                False,
            ],
            "Arguments used: nums1=[-2], nums2=[-2], n=6": [
                is_shifted([-2], [-2], 6),
                True,
            ],
            "Arguments used: nums1=[], nums2=[], n=2": [is_shifted([], [], 2), True],
        }
        for test_case, (a, b) in test_cases.items():
            with self.subTest(test_case=test_case):
                self.assertEqual(a, b, test_case)

    def test_add_every_nth(self):
        test_cases = {
            "Arguments used: nums=[5, 2, 1, 6, 4, 9, 3, 7, 8], n=3": [
                add_every_nth([5, 2, 1, 6, 4, 9, 3, 7, 8], 3),
                18,
            ],
            "Arguments used: nums=[1.5, 2, -3, 4], n=5": [
                add_every_nth([1.5, 2, -3, 4], 5),
                0,
            ],
            "Arguments used: nums=[1, 2, 3, -4], n=1": [
                add_every_nth([1, 2, 3, -4], 1),
                2,
            ],
            "Arguments used: nums=[6, 1, 2, 3, 7, 9, 4, 8], n=6": [
                add_every_nth([6, 1, 2, 3, 7, 9, 4, 8], 6),
                9,
            ],
            "Arguments used: nums=[9, -2, 3.5, -6.2, 1], n=2": [
                add_every_nth([9, -2, 3.5, -6.2, 1], 2),
                -8.2,
            ],
        }
        for test_case, (a, b) in test_cases.items():
            with self.subTest(test_case=test_case):
                self.assertEqual(a, b, test_case)

    def test_move_zeroes(self):
        test_cases = {
            "Argument used: nums=[5, 8, 0, 3, 0, 0, 4]": [
                move_zeroes([5, 8, 0, 3, 0, 0, 4]),
                [5, 8, 3, 4, 0, 0, 0],
            ],
            "Argument used: nums=[1, 2, 3, 0, 0, 0]": [
                move_zeroes([1, 2, 3, 0, 0, 0]),
                [1, 2, 3, 0, 0, 0],
            ],
            "Argument used: nums=[0, 0, 0, 0]": [
                move_zeroes([0, 0, 0, 0]),
                [0, 0, 0, 0],
            ],
            "Argument used: nums=[1, 2, 3, 4]": [
                move_zeroes([1, 2, 3, 4]),
                [1, 2, 3, 4],
            ],
            "Argument used: nums=[0, 0, 0, 1, 2, 3]": [
                move_zeroes([0, 0, 0, 1, 2, 3]),
                [1, 2, 3, 0, 0, 0],
            ],
            "Argument used: nums=[]": [move_zeroes([]), []],
        }
        for test_case, (a, b) in test_cases.items():
            with self.subTest(test_case=test_case):
                self.assertEqual(a, b, test_case)

    def test_unnest(self):
        test_cases = {
            "Argument used: nested_lists=[[1, 0, 4], ['a', 'b'], [True, False, True, True]]": [
                unnest([[1, 0, 4], ["a", "b"], [True, False, True, True]]),
                [1, 0, 4, "a", "b", True, False, True, True],
            ],
            "Argument used: nested_lists=[[], ['a', 'b']]": [
                unnest([[], ["a", "b"]]),
                ["a", "b"],
            ],
            "Argument used: nested_lists=[['a', 'b'], []]": [
                unnest([["a", "b"], []]),
                ["a", "b"],
            ],
            "Argument used: nested_lists=[[1], [2], [3]]": [
                unnest([[1], [2], [3]]),
                [1, 2, 3],
            ],
            "Argument used: nested_lists=[[], [], []]": [unnest([[], [], []]), []],
        }
        for test_case, (a, b) in test_cases.items():
            with self.subTest(test_case=test_case):
                self.assertEqual(a, b, test_case)

    def test_how_many_passed(self):
        test_cases = {
            "Argument used: exam_results=[['Joan Taylor', 331, 6], ['Louisa Kay', 112, 3], ['Adam Burton', 256, 8], "
            "['Martin Smith', 209, 7]]": [
                how_many_passed(
                    [
                        ["Joan Taylor", 331, 6],
                        ["Louisa Kay", 112, 3],
                        ["Adam Burton", 256, 8],
                        ["Martin Smith", 209, 7],
                    ]
                ),
                3,
            ],
            "Argument used: exam_results=[['Joan Taylor', 331, 6], ['Luisa Kay', 112, 6], ['Adam Burton', 256, 6]]": [
                how_many_passed(
                    [
                        ["Joan Taylor", 331, 6],
                        ["Luisa Kay", 112, 6],
                        ["Adam Burton", 256, 6],
                    ]
                ),
                3,
            ],
            "Argument used: exam_results=[['Joan Taylor', 331, 1], ['Luisa Kay', 112, 5], ['Adam Burton', 256, 2], "
            "['Martin Smith', 209, 4]]": [
                how_many_passed(
                    [
                        ["Joan Taylor", 331, 1],
                        ["Luisa Kay", 112, 5],
                        ["Adam Burton", 256, 2],
                        ["Martin Smith", 209, 4],
                    ]
                ),
                0,
            ],
            "Argument used: exam_results=[['Joan Taylor', 331, 6]]": [
                how_many_passed([["Joan Taylor", 331, 6]]),
                1,
            ],
            "Argument used: exam_results=[]": [how_many_passed([]), 0],
        }
        for test_case, (a, b) in test_cases.items():
            with self.subTest(test_case=test_case):
                self.assertEqual(a, b, test_case)

    def test_diagonal_sum(self):
        test_cases = {
            "Argument used: matrix=[[1, 2, 3], [4, 5, 6], [7, 8, 9]]": [
                diagonal_sum([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
                15,
            ],
            "Argument used: matrix=[[5, 3], [8, 0]]": [
                diagonal_sum([[5, 3], [8, 0]]),
                5,
            ],
            "Argument used: matrix=[]": [diagonal_sum([]), 0],
            "Argument used: matrix=[[4]]": [diagonal_sum([[4]]), 4],
        }
        for test_case, (a, b) in test_cases.items():
            with self.subTest(test_case=test_case):
                self.assertEqual(a, b, test_case)

    def test_find_country(self):
        test_cases = {
            "Arguments used: cities=[('Buenos Aires', 'Argentina'), ('Glasgow', 'Scotland'), ('Liverpool', 'England'), "
            "('Madrid', 'Spain')], city_name='Glasgow'": [
                find_country(
                    [
                        ("Buenos Aires", "Argentina"),
                        ("Glasgow", "Scotland"),
                        ("Liverpool", "England"),
                        ("Madrid", "Spain"),
                    ],
                    "Glasgow",
                ),
                "Scotland",
            ],
            "Arguments used: cities=[('Buenos Aires', 'Argentina'), ('Glasgow', 'Scotland'), ('Liverpool', 'England'), "
            "('Madrid', 'Spain')], city_name='Montevideo'": [
                find_country(
                    [
                        ("Buenos Aires", "Argentina"),
                        ("Glasgow", "Scotland"),
                        ("Liverpool", "England"),
                        ("Madrid", "Spain"),
                    ],
                    "Montevideo",
                ),
                None,
            ],
            "Arguments used: cities=[], city_name='Glasgow'": [
                find_country([], "Glasgow"),
                None,
            ],
        }
        for test_case, (a, b) in test_cases.items():
            with self.subTest(test_case=test_case):
                self.assertEqual(a, b, test_case)

    def test_find_destination(self):
        test_cases = {
            "Arguments used: [(100, 'Buenos Aires'), (110, 'Madrid'), (120, 'Glasgow')], cities=[('Buenos Aires', 'Argentina'),"
            "('Glasgow', 'Scotland'), ('Liverpool', 'England'), ('Madrid', 'Spain')], ticket_number=100": [
                find_destination(
                    [(100, "Buenos Aires"), (110, "Madrid"), (120, "Glasgow")],
                    [
                        ("Buenos Aires", "Argentina"),
                        ("Glasgow", "Scotland"),
                        ("Liverpool", "England"),
                        ("Madrid", "Spain"),
                    ],
                    100,
                ),
                "Argentina",
            ],
            "Arguments used: tickets=[(100, 'Buenos Aires'), (110, 'Madrid'), (120, 'Glasgow'), (130, 'Madrid')],"
            "cities=[('Buenos Aires', 'Argentina'), ('Glasgow', 'Scotland'), ('Liverpool', 'England'), "
            "('Madrid', 'Spain')], ticket_number=100": [
                find_destination(
                    [
                        (100, "Buenos Aires"),
                        (110, "Madrid"),
                        (120, "Glasgow"),
                        (130, "Madrid"),
                    ],
                    [
                        ("Buenos Aires", "Argentina"),
                        ("Glasgow", "Scotland"),
                        ("Liverpool", "England"),
                        ("Madrid", "Spain"),
                    ],
                    130,
                ),
                "Spain",
            ],
            "Arguments used: tickets=[(100, 'Buenos Aires'), (110, 'Madrid'), (120, 'Glasgow')], cities=[('Buenos "
            "Aires', 'Argentina'), ('Glasgow', 'Scotland'), ('Liverpool', 'England'), ('Madrid', 'Spain')], "
            "ticket_number=140": [
                find_destination(
                    [(100, "Buenos Aires"), (110, "Madrid"), (120, "Glasgow")],
                    [
                        ("Buenos Aires", "Argentina"),
                        ("Glasgow", "Scotland"),
                        ("Liverpool", "England"),
                        ("Madrid", "Spain"),
                    ],
                    140,
                ),
                None,
            ],
            "Arguments used: tickets=[(100, 'Montevideo'), (110, 'Madrid'), (120, 'Glasgow')], cities=[('Buenos Aires',"
            "'Argentina'), ('Glasgow','Scotland'), ('Liverpool', 'England'), ('Madrid', 'Spain')], ticket_number=100": [
                find_destination(
                    [(100, "Montevideo"), (110, "Madrid"), (120, "Glasgow")],
                    [
                        ("Buenos Aires", "Argentina"),
                        ("Glasgow", "Scotland"),
                        ("Liverpool", "England"),
                        ("Madrid", "Spain"),
                    ],
                    100,
                ),
                None,
            ],
            "Arguments used: tickets=[], cities=[('Buenos Aires', 'Argentina'), ('Glasgow', 'Scotland')], "
            "ticket_number=100": [
                find_destination(
                    [], [("Buenos Aires", "Argentina"), ("Glasgow", "Scotland")], 100
                ),
                None,
            ],
            "Arguments used: tickets=[], cities=[(100, 'Buenos Aires'), (110, 'Madrid'), (120, 'Glasgow')], "
            "ticket_number=100": [
                find_destination(
                    [], [(100, "Buenos Aires"), (110, "Madrid"), (120, "Glasgow")], 100
                ),
                None,
            ],
        }
        for test_case, (a, b) in test_cases.items():
            with self.subTest(test_case=test_case):
                self.assertEqual(a, b, test_case)
