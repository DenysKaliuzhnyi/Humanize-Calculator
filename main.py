"""
This program converts math equation in humanized style
(2+2=4 will be "two plus two equals four").

About input data info:
    possible symbols are +-*/= and digits;
    white symbols will be ignored (even inside number);
    the program checks whether input formulation is valid in sense of maths,
but this doesn't include arithmetical correctness
(2 + 2 = 5/0 it's ok, but  *3 ++ 02 = 2*/1 — invalid);
    one number can contain no more then 306 digits.

Example of your correct input -1+2/4*100    - 191432423 =-0/0.
Write equation to be converted in input.txt and see result in output.txt
by running main.py.

You can run pytests of this prog by command "pytest testsCalculator.py" in your terminal.
"""

from humanizeCalculator import humanize_equation
import os

workingDirectory = os.getcwd()
finName = f'{workingDirectory}\input.txt'
foutName = f'{workingDirectory}\output.txt'


def write_result(fname, data):
    with open(fname, 'w', encoding='utf8') as f:
        f.write(str(data))


if __name__ == '__main__':
    res = humanize_equation(finName)
    write_result(foutName, res)
