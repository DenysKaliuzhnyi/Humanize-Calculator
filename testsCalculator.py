import pytest
import humanizeCalculator as hc


def test_remove_white_symbols():
    assert hc.remove_white_symbols("     1+   2+3+4 = \n  1234\t  ") == "1+2+3+4=1234"
    assert hc.remove_white_symbols("0") == '0'


def test_get_operands():
    assert hc.get_operands("1+2+3+4=1234") == ['1', '2', '3', '4', '1234']
    assert hc.get_operands("1") == ['1']


def test_replace_numbers_by_0():
    assert hc.replace_numbers_by_0('1+2+3+4=1234') == "0+0+0+0=0"
    for i in range(0, 100):
        assert hc.replace_numbers_by_0(f'{i}+{i*i}=-5') == "0+0=-0"


def test_separate_number_by_hundreds():
    assert hc.separate_number_by_hundreds("1139312234456") == ['1', '139', '312', '234', '456']
    assert hc.separate_number_by_hundreds("123456789098765432") == ['123', '456', '789', '098', '765', '432']
    assert hc.separate_number_by_hundreds("12345") == ['12', '345']
    assert hc.separate_number_by_hundreds("0") == ['0']


def test_humanize_hundreds():
    assert hc.humanize_hundreds("123") == "one hundred and twenty-three"
    assert hc.humanize_hundreds("1") == "one"
    assert hc.humanize_hundreds("99") == "ninety-nine"
    assert hc.humanize_hundreds("666") == "six hundred and sixty-six"


def test_append_decimal_name_to_hundreds():
    assert hc.append_decimal_name_to_hundreds(['one', 'six hundred and sixty-six', 'one hundred and twenty-three']) == \
           ['one million', 'six hundred and sixty-six thousand', 'one hundred and twenty-three']
    assert hc.append_decimal_name_to_hundreds(['ninety-nine']) == ['ninety-nine']


def test_construct_final_number():
    assert hc.construct_final_number(['a', 'b', 'c', 'd', 'e']) == "a b c d e"
    assert hc.construct_final_number([]) == ""
    assert hc.construct_final_number(['101']) == "101"
    assert hc.construct_final_number(['one million', 'six hundred and sixty-six thousand', 'one hundred and twenty-three'])\
           == 'one million six hundred and sixty-six thousand one hundred and twenty-three'


def test_build_expression():
    assert hc.build_expression(['a', 'b', 'c'], '0+0=-0') == 'a plus b equals minus c'
    assert hc.build_expression(['1', '2', '3', '4', '5'], '0-0*0/0-0') == '1 minus 2 multiplied by 3 divided by 4 minus 5'
    assert hc.build_expression([], '') == ""


def test_valid_syntax():
    assert hc.valid_syntax("2132= 3 - 1223+ 342423/234243*23", ['2132', '3', '1223', '342423', '234243', '23'], "0=0-0+0/0*0")
    assert hc.valid_syntax("-1=-2", ['1', '2'], '-0=-0')
    assert not hc.valid_syntax('=2', ['2'], "=0")
    assert not hc.valid_syntax('2++1=3', ['2', '1'], "0++0=3")
    assert not hc.valid_syntax('', [], "")





