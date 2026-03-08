# Práctica Interactiva - Programación Desde Cero

## What exactly is this tool

This project is a tool you can use to practise programming challenges (or exercises) for beginners, using Python 3.

Exercises are mainly intended to help develop algorithmic and logical reasoning skills as well as learn how to work with programming fundamentals. It doesn't focus on learning the perks of the Python language. That's why in most cases you're encouraged to build your own solution without using the built-in solutions that Python offers.

Challenges are divided into categories (or topics) to help you practise with specific data types and structures, but that doesn't mean there can't be other possible solutions (which might even be more efficient).

## Instructional approach

Each category includes a variety of functions where their body is missing, and some documentation showing how each
function should behave. Also, each function has a set of unit tests associated to it. You'll need to fill in the blanks (that is: write the function body) without modifying anything else, and get all tests to pass.

Tests will then need to be executed to evaluate if the functions return their expected result.

Exercises are divided into the following categories or topics: _numbers, strings, lists and tuples, sets and dictionaries_; meaning you're encouraged to solve challenges using these data types in order to practise programming fundamentals. But they can be solved in other ways too, as long as the tests pass successfully.

Although it's possible to solve the exercises in any given order, there's a preferred order that allows to solve them with increasing difficulty:

1. Numbers
2. Strings
3. Lists and tuples
4. Sets and dictionaries

This means that exercises in the `numbers.py` module can be solved without using strings, lists, tuples, sets or dictionaries. But the challenges in strings.py module may need to be solved using number as well as string manipulation. Challenges in the list and tuples module may need number and string manipulation in addition to lists and tuples. Then challenges with sets may need working with numbers, strings, lists or tuples in addition to sets. Finally, the dictionary challenges may need working with any of the previous data types (numbers, strings, lists, tuples and sets).  

## How this tool is organized

- The **ENG** folder contains two subfolders: **src** and **tests**.
  - The **/ENG/src** folder contains a file for each category, and these files contain functions with only `pass` as their body, which you'll need to replace with your code.
  - The **/ENG/tests** folder contains the unit tests. There is one test file per each category file in `/ENG/src`. Each file contains a function per each exercise and its name is precede by "test_" and continues with the exercise name.

You'll be able to run the unit tests associated to any exercise to check if your algorithm is correct.

At first, all tests are expected to fail. The goal is to add the function bodies in `ENG/src` (replacing the `pass` statements with your algorithms) and get the tests to pass.

Example: `/ENG/src/numbers.py` has exercise (function) `absolute_value` and `/ENG/tests/tests_numbers.py` contains the tests for that exercise, in function `test_absolute_value`.

## How to use the tool

Pre-requisite: Python 3 needs to be installed (the minimum required version is 3.4).

In order to solve the exercises, only the function bodies in the files from `/ENG/src` should be modified. Files from `/ENG/tests` shouldn't be altered.

After adding the algorithm for one or more functions from the files in `/ENG/src`, you'll need to run the
tests to see if they pass or fail. When tests pass, they will show an "ok" result; if a test fails, it will show which function it ran, the arguments used to call it, what it returned and what was the expected return value.

You'll be able to run tests in three ways:

- only for a specific function,
- for all functions in a `/ENG/src` file,
- for more than one file in `/ENG/src` at the same time.

### How to solve the exercises

Using a text editor or an IDE, open any of the files in `/ENG/src` (for the chosen category). Example: `numbers.py`.

Each exercise is represented by a function in the code. Example: `absolute_value()`.

To solve the exercises:

- The documentation (_docstrings_) in each function shows what is expected from the algorithm, provides examples and detailed information about the parameters and return value.
- The related test function contains the unit tests with the specific cases that must be considered by the algorithm.

Within the selected file from `/ENG/src`, replace `pass` (in one or more functions) with the algorithm that solves the exercise.

To solve the exercises you'll only need to modify the function bodies in the `/ENG/src` files. The function signature shouldn't be altered, and neither should the `/ENG/tests` files.

Finally, run the tests for the completed exercises, to know if they pass or fail.

### How to run the tests

Tests can be executed for a single function (just one exercise), for all functions in a category (file) or for all categories at once.

To run the tests you can use a terminal or configure your preferred IDE. If you use a terminal, you'll need to change directory ("CD") to the project folder (example: if the project is placed in c:/myuser/project that's the folder you'll need to change to) and then run the python command.

**Note 1:** depending on your Python installation, you might need to replace the "python" command with "python3" or something else.

**Note 2:** If you use Pycharm, configurations must be created from the top menu "Run > Edit Configurations" and then "Add new run configuration".

#### Run tests for a single function/exercise

In a terminal or command line interface, run the following command:

`python -m unittest -v path/to/file.py -k test_function`

where _path/to/file.py_ must be replaced with the path from the root folder to the test file containing the tests to be executed (e.g.: **ENG/tests/tests_numbers.py**) and _test_function_ must be replaced with the test function to be executed (e.g.: **test_absolute_value**). For instance, to run tests for function **absolute_value** in the _numbers_ category:

`python -m unittest -v ENG/tests/tests_numbers.py -k test_absolute_value`

**To do the same by using a Pycharm configuration:** select the "Module name" option (while editing configurations) and click on "..." to open a new dialog where you'll need to enter the name of the category file you want to execute (e.g.: tests_numbers) and select it from the dropdown. Then, in "Additional Arguments", enter "-k test_function_name" (replace with the name of the function to execute). Check the option "Add contents to PYTHONPATH" is checked.

#### Run all tests from a category

`python -m unittest -v path/to/file.py`

where _path/to/file.py_ must be replaced with the path from the root folder to the test file containing the tests to be executed (e.g.: **ENG/tests/tests_numbers.py**). For instance, to run all tests for all exercises in the _numbers_ category:

`python -m unittest -v ENG/tests/tests_numbers.py`

**To do the same by using a Pycharm configuration:** select the "Module name" option and then click on "..." to open a new dialog where you'll need to enter the name of the category file you want to execute (e.g.: tests_numbers) and select it from the dropdown. Check the option "Add contents to PYTHONPATH" is checked.

#### Run tests for more than one category at a time

To run tests for more than one category (or all categories) at the same time, execute **run_tests.py**. If you're using a terminal or command line interface, you'll first need to set the **PYTHONPATH** environment variable to the project folder. To avoid making this a permanent change, you can do it temporary, in each terminal session: open the terminal, CD into the project directory and run:

`export PYTHONPATH="$PWD"` if you're running Linux/Mac, or

`set PYTHONPATH=%cd%` if you're running Windows.

Next, execute **run_tests.py** with:

`python ENG/run_tests.py`

If you're using Pycharm, you can just run the **run_tests.py** file, by selecting it and then pressing Ctrl+Shift+F10 or simply clicking the "Run" button.

If you need to exclude a test category from execution, comment (with a leading #) the line in **run_tests.py**. The line will look like this: `suite.addTests(loader.loadTestsFromModule(category_to_be_excluded))`.

## Recommended approach

When writing professional code it's very likely that many of what is covered in these challenges is solved by just using built-in language tools.

But, for educational purposes, limiting the available tools is a valid restriction that allows to develop algorithmic thinking.

That why, when using this tool to practise, it's recommended to write your own algorithms instead, to exercise
logical reasoning and programming fundamentals. This is why some functions suggest avoiding some specific tools.

All the challenges in the project can be solved without the need of importing any libraries (so only the function bodies should be modified).

Also, the challenge topics suggest specific data types and structures to help improve algorithmic thinking, even when there might be more efficient solutions. Feel free to solve the problems in any way you think best, as this is only a suggestion.
