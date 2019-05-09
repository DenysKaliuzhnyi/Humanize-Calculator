import re
import data


def get_equation(fname):
    """
    :param fname: name of file to read equation
    :return: string of all data in file
    """
    with open(fname, 'r', encoding='utf8') as f:
        return f.read()


def valid_syntax(eq, operands, structure):
    """
    :param eq: string of math equation
    :param operands: string list of numbers
    :param structure: string that contains only +-/*=0 symbols
    :return: whether equation is valid or not
    """
    if len(eq) == 0:
        return False

    if re.sub(r'[0-9\-\+\*\/\=]+', '', eq).strip() != '':  # must contain only digits and +-*/=
        return False

    # first sign must be a digit or '-' and last is digit
    if (structure[0] != '0' and structure[0] != '-') or structure[-1] != '0':
        return False

    for number in operands:
        if number[0] == '0' and len(number) != 1:   # number cannot begin from 0
            return False
        if len(number) > 306:
            return False

    ops = re.findall(r'[\-\+\*\/\=]+', structure)
    for op in ops:
        if len(op) > 1 and op != '=-':
            return False

    return True


def remove_white_symbols(eq):
    """
    :param eq: string of math equation
    :return: copy of string without white symbols
    :example: "  3 + \t4 =\n7" |-> "3+4=7"
    """
    return re.sub(r'[\s]', '', eq)


def get_operands(eq):
    """
    :param eq: string of math equation
    :return: list of string numbers
    :example: "32000+5514*44+423=1" |-> ['32000', '5514', '44', '423', '1']
    """
    res = re.split('[\-\+\*\/\=]+', eq)
    return [el for el in res if el != '']


def replace_numbers_by_0(eq):
    """
    :param eq: string of math equation
    :return: string where each number replaced by '0'
    :example: "3-6=-3" |-> "0-0=-0"
    """
    return re.sub(r'[0-9]+', '0', eq)


def separate_number_by_hundreds(number):
    """
    :param number: string of number
    :return: list of string numbers - splitted by every 3rd digit param
    :example: "73798234" |-> ['73', '798', '234']
    """
    separated_operands = []
    for times in range(0, len(number), 3):
        separated_operands.append(number[-3:])
        number = number[:-3]
    return list(reversed(separated_operands))


def humanize_hundreds(number3):
    """
    :param number3: string of 3, 2 or 1-digit int number
    :return: humanized representation of number
    :example: "178" |-> "one hundred seventy-eight"
    """
    res = ''
    numlen = len(number3)
    if numlen == 3:
        if number3[0] != '0':
            res = f'{data.digits[number3[0]]} ' \
                   f'hundred' \
                   f'{" and " if number3[2]!="0" or number3[1]!="0" else ""}'
        if number3[1] != '1':
            res = f'{res}' \
                   f'{data.tens[number3[1]]}' \
                   f'{"-" if number3[2]!="0" and number3[1]!="0" else ""}' \
                   f'{data.digits[number3[2]]}'
        else:
            res = f'{res}' \
                   f'{data.teens[number3[2]]}'

    elif numlen == 2:
        if number3[0] != '1':
            res = f'{data.tens[number3[0]]}' \
                   f'{"-" if number3[1]!="0" and number3[0]!="0" else ""}' \
                   f'{data.digits[number3[1]]}'
        else:
            res = f'{data.teens[number3[1]]}'
    else:
        res = f'{data.digits[number3[0]]}'
    return res


def append_decimal_name_to_hundreds(humanizedHundreds):
    """
    :param humanizedHundreds: string list of humanized representation of 3, 2 or 1-digit numbers:
    :return: modified list, append decimal name for each hundred
    :example: "one hundred seventy-eight" |-> "one hundred seventy-eight thousands"
    """
    hhlen = len(humanizedHundreds)
    res = list(
                map(
                    lambda args: f'{args[1]} '
                                 f'{data.decimals[hhlen-args[0]-1 if args[1] != "" else -1]}'.strip(),
                    enumerate(humanizedHundreds)
                )
            )
    res = [el for el in res if el != "delete_me"]
    return res


def humanize_operands(operands):
    """
    :param operands: string list of numbers
    :return: humanized representation of number
    :example: "432343" |-> "four hundreds and thirty-two thousands, three hundreds and forty-three"
    """
    humanizedOperands = []
    for number in operands:
        if number == '0':                     # special case
            humanizedOperands.append('zero')
            continue
        splitedNumber = separate_number_by_hundreds(number)
        humanizedHundreds = [humanize_hundreds(number3) for number3 in splitedNumber]
        humanizedHundreds = append_decimal_name_to_hundreds(humanizedHundreds)
        finalHumanizedNumber = construct_final_number(humanizedHundreds)
        humanizedOperands.append(finalHumanizedNumber)
    return humanizedOperands


def construct_final_number(humanizedHundreds):
    """
    :param humanizedHundreds: string list of 3, 2 or 1-digit string numbers
    :return: joined by ' ' elements
    """
    return ' '.join(humanizedHundreds).strip(', ')


def build_expression(humanizedOperands, structure):
    """
    :param humanizedOperands: string list of translated numbers
    :param structure: string that contains only +-/*=0 symbols
    :return: string of constructed expression
    """
    res = ''
    for el in structure:
        if el == '0':
            res = f'{res} {humanizedOperands.pop(0)}'
        else:
            res = f'{res} {data.operators[el]}'
    return res.strip()


def humanize_equation(fname):
    """
    :param fname: string name of file of a math expression
    :return: string of humanized equation
    :example: "32 + 654 * 22  = 7560" |-> "thirty-two plus six hundreds and fifty-four times twenty-two equals seven thousands, five hundreds and sixty"
    """
    equation = remove_white_symbols(get_equation(fname))
    structure = replace_numbers_by_0(equation)
    operands = get_operands(equation)
    if not valid_syntax(equation, operands, structure):
        expr = "invalid input"
    else:
        humanizedOperands = humanize_operands(operands)
        expr = build_expression(humanizedOperands, structure)
    return expr
