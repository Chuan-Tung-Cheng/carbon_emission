import utils_regex_pattern as rep

from decimal import Decimal, ROUND_HALF_UP

"""
README:
This util is to process the filed of quantity and it mainly separate the values into the number part and the unit part.
Basically, The data type of the number part is decimal; the unit part is string 
"""


def blank_comma_removal(text: str) -> str:
    """
    Remove the comma symbol.
    Here it will also remove blanks.
    """
    text = text.strip()
    text = text.replace(" ", "")

    if "," in text:
        text = text.replace(",", "")
        return text
    return text


"""The below is to get the number part"""
def get_num_in_field_quantity(text: str) -> float | str | None:
    """
    Separate the number and thr unit, and mainly fetch the number
    """

    have_digit_num = any(num.isdigit() for num in text)
    # first filter: check if text has digits
    if have_digit_num: # with digits
        # second filter: check if text has "~", "-", "～"
        if any(sep in text for sep in ("~", "-", "～", "至", "_")):
            matches = rep.COMPILED_PATTERN_WITH_NUMBERS_RANGE.finditer(text)
            if matches is not None:
                return match_num_with_digit_range(matches)
        else:
            matches = rep.COMPILED_PATTERN_WITH_NUMBERS.finditer(text) # bool
            if matches is not None:
                return match_num_with_digit(matches)
    else: # without digits
        have_char_num = have_chinese_char_num(text)
        if have_char_num:
            # second filter: check if text has "~", "-", "～"
            if any(sep in text for sep in ("~", "-", "～", "至", "_")):
                matches = rep.COMPILED_PATTERN_WITH_NUMBERS_RANGE.finditer(text)
                if matches is not None:
                    return match_num_with_chinese_range(matches)
            else:
                matches = rep.COMPILED_PATTERN_WITH_NUMBERS.finditer(text) # bool
                if matches is not None:
                    return match_num_with_chinese(matches)
        else: # process "適量", "少許"
            pass
    return None

def get_unit_in_field_quantity(text: str) -> float | str | None:
    """
    Separate the number and thr unit, and mainly fetch the number
    """
    # first filter: check if text has digits
    have_num = any(num.isdigit() for num in text)
    if have_num: # check if text has numerics
        # second filter: check if text has "~", "-", "～"
        if any(sep in text for sep in ("~", "-", "～", "至", "_")):
            matches = rep.COMPILED_PATTERN_WITH_NUMBERS_RANGE.finditer(text)
            if matches is not None:
                return match_unit(matches)
        else:
            matches = rep.COMPILED_PATTERN_WITH_NUMBERS.finditer(text) # bool
            if matches is not None:
                return match_unit(matches)

    else: # first filter: check if text has chinese-character numbers
        have_char_num = have_chinese_char_num(text)
        if have_char_num:
            # second filter: check if text has "~", "-", "～"
            if any(sep in text for sep in ("~", "-", "～", "至", "_")):
                matches = rep.COMPILED_PATTERN_WITH_NUMBERS_RANGE.finditer(text)
                if matches is not None:
                    return match_unit(matches)
            else:
                matches = rep.COMPILED_PATTERN_WITH_NUMBERS.finditer(text) # bool
                if matches is not None:
                    return match_unit(matches)
    return None

def have_chinese_char_num(text) -> bool:
    """
    # check if text has chinese-character numbers
    param matches: Iterator[Match[str]]
    return: bool
    """
    for char in text:
        if char in  rep.CHAR_NUM_MAPS:
            return True
    return False

def match_num_with_digit(matches) -> float | Decimal | str | None:
    """
    extract num part of digits
    param matches: Iterator[Match[str]]
    """
    for m in matches: # activate this iterate generator
        try:
            """when value is presented as an integer or an integer with decimal, such as 1 or 1.5"""
            number_part = Decimal(float(m.group(1)))
            return number_part

        except ValueError:
            """ when value is presented as a fraction, such as 1/3"""
            if "/" in m.group(1):
                fraction = m.group(1).split("/") # list
                """
                fraction[0] = numerator(分子)
                fraction[-1] = denominator(分母)
                """
                try:
                    numerator = Decimal(fraction[0])
                    denominator = Decimal(fraction[-1])
                    number_part = (numerator / denominator).quantize(
                        Decimal("0.01"),
                        rounding=ROUND_HALF_UP,
                    )
                    return number_part
                except ValueError:
                    return None
    return None

def match_unit(matches) ->  str | None:
    """
    extract num part of digits
    param matches: Iterator[Match[str]]
    """
    for m in matches: # activate this iterate generator
        return m.group(2)
    return None


def match_num_with_digit_range(matches) -> float | Decimal | str | None:
    """
    extract num part of digits
    param matches: Iterator[Match[str]]
    """
    # 1-2(0.5-0.8), 1/3 - 1/2,
    for m in matches: # activate this iterate generator
            try:
                boolean = any(spe in m.group(1) for spe in ["/"] ) # separate the fraction
                if not boolean: # second filter -> 1-2 kg
                    range_num = rep.re.split(r"[-~～至到_]", m.group(1))
                    first_num = Decimal(range_num[0])
                    last_num = Decimal(range_num[-1])
                    average = (first_num + last_num) / 2
                    return average
                else: # second filter -> 1/2-1/3 kg
                    range_num = rep.re.split(r"[-~～至到_]", m.group(1))
                    first_fraction = range_num[0]
                    if "/" in first_fraction:
                        front_fraction = list(map(int, first_fraction.split("/")))
                        front = Decimal(front_fraction[0] / front_fraction[-1])
                    else:
                        front = Decimal(first_fraction)
                    second_fraction = range_num[-1]
                    if "/" in second_fraction:
                        behind_fraction = list(map(int, first_fraction.split("/")))
                        behind = Decimal(behind_fraction[0] / behind_fraction[-1])
                    else:
                        behind = Decimal(second_fraction)

                    total = Decimal((front + behind) / 2).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                    return total

            except ValueError:
                return None
    return None

def match_num_with_chinese(matches) -> float | Decimal | str | None:
    """
    extract num part of digits that are meant by Chinese characters
    param matches: Iterator[Match[str]]
    """
    # 三 | 三分之一
    for m in matches:
        # no 分之
        if "分之" not in m.group(1):
            if m.group(1) in rep.CHAR_NUM_MAPS:
                return Decimal(rep.CHAR_NUM_MAPS[m.group(1)])
            else:
                return m.group(1)

        char_fraction = m.group(1).split("分之")
        # with 分之
        if char_fraction:
            """
            char_fraction[-1] = numerator(分子)
            char_fraction[0] = denominator(分母)
            """
            try:
                numerator = Decimal(char_fraction[-1])
                denominator = Decimal(char_fraction[0])
                number_part = (numerator / denominator).quantize(
                    Decimal("0.01"),
                    rounding=ROUND_HALF_UP,
                )
                return number_part
            except ValueError:
                return m.group(1)
    return None

def match_num_with_chinese_range(matches) -> float | Decimal | str | None:
    """
    extract num part of digits that are meant by Chinese characters
    param matches: Iterator[Match[str]]
    """
    # 一 ~ 二, 三分之一 ~ 二分之一
    for m in matches:
        try:
            boolean = any(spe in m.group(1) for spe in ["分之"])  # separate the fraction
            if not boolean: # second filter -> 一 - 二 kg
                range_num = rep.re.split(r"[-~～至到]", m.group(1))
                if range_num[0] in rep.CHAR_NUM_MAPS:
                    first_num = Decimal(rep.CHAR_NUM_MAPS[range_num[0]])
                else:
                    return None
                if range_num[-1] in rep.CHAR_NUM_MAPS:
                    second_num = Decimal(rep.CHAR_NUM_MAPS[range_num[-1]])
                else:
                    return None
                total = Decimal((first_num + second_num) / 2).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                return total

            else: # second filter -> 三分之一 ~ 二分之一
                range_num = rep.re.split(r"[-~～至到]", m.group(1)) # range_num[0] = "三分之一", range_num[1] = "二分之一"
                front_fraction = list(map(str, range_num[0].split("分之")))
                if front_fraction[0] in rep.CHAR_NUM_MAPS:
                    front_num = Decimal(rep.CHAR_NUM_MAPS[front_fraction[0]]) # front numerator
                else:
                    return None
                if front_fraction[-1] in rep.CHAR_NUM_MAPS:
                    behind_num = Decimal(rep.CHAR_NUM_MAPS[front_fraction[-1]]) # front denominator
                else:
                    return None
                front_total = Decimal( behind_num / front_num ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

                behind_fraction = list(map(str, range_num[-1].split("分之")))
                if behind_fraction[0] in rep.CHAR_NUM_MAPS:
                    front_num = Decimal(rep.CHAR_NUM_MAPS[behind_fraction[0]]) # front numerator
                else:
                    return None
                if behind_fraction[-1] in rep.CHAR_NUM_MAPS:
                    behind_num = Decimal(rep.CHAR_NUM_MAPS[behind_fraction[-1]]) # front denominator
                else:
                    return None
                behind_total = Decimal( behind_num / front_num ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

                total = Decimal((front_total + behind_total) / 2).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                return total

        except ValueError as e:
            print(e)
    return None
