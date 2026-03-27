##################################
#        TOPIC: NUMBERS          #
##################################


def smallest(number1, number2):
    """
    Returns the smallest between two numbers.
    Examples:
        smallest(number1=3, 1) -> 1
        smallest(number1=3, 3) -> 3
    -Parameters:
        -number1 (numeric): One of the numbers to be processed.
        -number2 (numeric): The other number to be processed.
    -Returns:
        (numeric) The smallest between two numbers. `number1` if they are equal.
    """
    pass


def absolute_value(number):
    """
    Returns the absolute value of a number.
    Suggestion: avoid using abs().
    Examples:
        absolute_value(number=3) -> 3
        absolute_value(number=-10) -> 10
    -Parameter:
        -number (numeric): The number whose absolute value will be calculated.
    -Returns:
        (numeric) Absolute value of `number`.
    """
    pass


def extract_month(date):
    """
    Given a date consisting of day, month and year, returns the month. Date will have the ddmmaaaa or dmmaaaa format,
    where "d" stands for day digits, "m" stands for month digits and "a" stands for year digits.
    Examples:
        extract_month(date=31122020) -> 12
        extract_month(date=5091946) -> 9
    -Parameters:
        -date (int): Valid date in a ddmmaaaa or dmmaaaa format. dd (or d) will be between 1 and 31. mm will be between
        1 and 12. Positive.
    -Returns:
        (int) The month contained in `date`.
    """
    pass


def add_multiples(lower, upper, n):
    """
    Adds up the multiples of `n` contained in a closed interval of integers.
    Examples:
        add_multiples(lower=0, upper=30, n=5) -> 105
        add_multiples(lower=-30, upper=0, n=5) -> -105
    -Parameters:
        -lower (int): Lower bound of the interval. Lesser or equal to `upper`.
        -upper (int): Upper bound of the interval. Greater or equal to `lower`.
        -n (int): Number whose multiples will be added up. Cannot be 0.
    -Returns:
        (int) Summation of multiples of `n` between `lower` and `upper` bounds.
    """
    pass


def is_palindromic_number(number):
    """
    Decides if a number is a palindrome or not. A palindrome number remains the same when its digits are reversed.
    Suggestion: only work with numbers (avoid other data types).
    Examples:
        is_palindromic_number(number=123321) -> True
        is_palindromic_number(number=1234) -> False
    -Parameters:
        -number (int): Number to evaluate. Positive.
    -Returns:
        (bool) True if `number` is a palindrome, False if it's not.
    """
    pass


def leap_year(year):
    """
    Decides if a given year is a leap year according to the Gregorian calendar.
    Examples:
        leap_year(year=2020) -> True
        leap_year(year=1800) -> False
    -Parameter:
        -year (int): Year to evaluate. Positive.
    -Returns:
        (bool) True if `year` is a leap year. False if it's not.
    """
    pass


def days_in_month(month, year):
    """
    Determines how many days are there in a given month, from a given year. The case where the month is February in a
    leap year must be considered.
    Suggestion: break the problem into steps, using an algorithm to determine if a year is a leap year.
    Example:
        days_in_month(month=11, year=1981) -> 30
    -Parameters:
        -month (int): Number representing the month. Between 1 and 12.
        -year (int): Number representing the year. Positive.
    -Returns:
        (int) Number of days in the given `month`.
    """
    pass


def digit_count(number):
    """
    Counts digits in a number.
    Example:
        digit_count(number=120) -> 3
    -Parameter:
        -number (int): Number whose digits are being counted.
    -Returns:
        (int) Digit count in `number`.
    """
    pass


def add_square_digits(number):
    """
    Determines the sum of squares of digits in a given number.
    Example:
        add_square_digits(number=15) -> 26
    -Parameter:
        -number (int): Number whose digits are being processed. Positive.
    -Returns:
        (int) Sum of squares of every digit in `number`.
    """
    pass


def percentage_even_digits(number):
    """
    Determines the percentage of even digits over the total amount of digits in a given number.
    Example:
        percentage_even_digits(number=5555666555) -> 30.0
    -Parameter:
        -number (int): Number whose digits are being processed. Positive.
    -Returns:
        (float) Percentage (from 0 to 100) of even digits in `number`.
    """
    pass


def is_pronic(number):
    """
    Decides if a number is "pronic". A number is considered "pronic" if it's the product of two consecutive integers.
    Example:
        is_pronic(number=56) -> True
        (56 can be expressed as 7*8).
    -Parameter:
        -number (int): Number to evaluate. Greater than 0.
    -Returns:
        (bool) True if `number` is pronic, False if it's not.
    """
    pass


def is_prime(number):
    """
    Determines if a number is prime.
    Example:
        is_prime(number=7) -> True
    -Parameter:
        -number (int): Number to evaluate. Positive.
    -Returns:
        (bool) True if `number` is prime. False if it's not.
    """
    pass


def factorial(number):
    """
    Determines the factorial of a positive number.
    Example:
        factorial(number=4) -> 24
    -Parameter:
        -number (int): Number whose factorial will be calculated. Positive.
    -Returns:
        (int) Factorial of `number`.
    """
    pass


def sum_first_n_fibonacci(n):
    """
    Determines the sum of the first `n` terms in the Fibonacci sequence, considering the first two terms in the series are 0
    and 1.
    Example:
        sum_first_n_fibonacci(n=6) -> 12
    -Parameters:
        -n (int): how many Fibonacci terms will be summed. Greater or equal than 2.
    -Returns:
        (int) Sum of first `n` numbers in the Fibonacci sequence.
    """
    pass


def greatest_divisor(number):
    """
    Returns the greatest integer divisor of a number (except for the number itself).
    If `number` is 1, returns 0.
    Example:
        greatest_divisor(number=182) -> 91
    -Parameters:
        -number (int): Number whose divisor will be calculated. Positive.
    -Returns:
        (int) Greatest number that can be used as a divisor for the `number`, without a remainder.
    """
    pass


def euclidean_gcd(m, n):
    """
    Returns the greatest common divisor of `m` and `n` using the Euclidean algorithm.
    Euclidean algorithm: dividing `m` by `n` (both integer numbers), we get a quotient `q` and a remainder `r`. The
    greatest common divisor of `m` and `n` is the same as for `n` and `r`.
    Example:
        euclidean_gcd(m=60, n=24) -> 12
    -Parameters:
        -m (int): Positive number.
        -n (int): Non-negative number.
    -Returns:
        (int) Greatest common divisor of `m` and `n`.
    """
    pass


def get_month(days_elapsed, year):
    """
    Returns the month number, given the number of days elapsed since January 1st in a particular year (taking into
    account that it could be a leap year).
    Suggestion: break the problem into steps, using an algorithm to get how many days are there in a month.
    Example:
        get_month(days_elapsed=200, year=1969) -> 7
        (the 60th consecutive day in a leap year represents February 29, while in a non-leap
        year it will be March 1st).
    -Parameters:
        -days_elapsed (int): Number of days elapsed from January 1st. Between 1 and 366.
        -year (int): Year (leap or non-leap). Positive.
    -Returns:
        (int) Month number (between 1 and 12) where `days_elapsed` lies in the given `year`.
    """
    pass


def is_disarium(number):
    """
    Determines if a number is a "disarium" number.
    A disarium number is one where the sum of each digit raised to the power of its position (starting from 1 on the
    left) equals the number itself.
    Suggestion: break the problem into steps, using an algorithm to count digits in a number.
    Example:
        is_disarium(number=518) -> True
        (518 is a disarium number, since 5**1=5, 1**2=1, 8**3=512, and 5+1+512=518).
    -Parameter:
        -number (int): Number whose digits will be evaluated. Positive.
    -Returns:
        (bool) True if `number` is "disarium", False if it's not.
    """
    pass


def arrange_coins(amount):
    """
    Determines how many rows can be "built" using a given `amount` of coins that will be arranged in a "staircase" way,
    where every "n"th row must contain exactly "n" coins. The last row of the staircase can be incomplete.
    Example:
        arrange_coins(amount=5) -> 2
        (With 5 coins we can build only 2 full rows, since there are not enough coins for the third row:
        ¤
        ¤ ¤
        ¤ ¤
        )
    -Parameter:
        -amount (int): Number of coins that must be used. Positive.
    -Returns:
        (int) Maximum full rows that can be built with the given `amount` of coins.
    """
    pass


def single_ones(number):
    """
    Determines how many "ones" in a number are not followed by another consecutive "one".
    Suggestion: avoid converting the number or its digits into a diferent data type.
    Example:
        single_ones(number=141211) -> 2
        single_ones(number=11411211) -> 0
    -Parameter:
        -number (int): Number whose digits will be evaluated. Positive.
    -Returns:
        (int) How many non-consecutive 1's are there in `number`.
    """
    pass
