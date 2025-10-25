import re

from decimal import Decimal, ROUND_HALF_UP


PATTERN_STR_VERBOSE_WITH_NUMBERS = r"""
    ( # Group 1: 捕獲整個「數字」部分
        (?:(?:.*)+分之(?:.*))                            # 中文表達分數 (e.g., 三分之二)
        |
        (?:\d+(?:\.\d+)?)[~-](?:\d+(?:\.\d+)?)          # 範圍 (e.g., 2-3)
        | 
        (?:\d+\/\d+)                                    # 分數 (e.g., 1/2)
        | 
        (?:[半一二三四五六七八九十百千萬]+)                  # 中文數字 (e.g., 一)
        | 
        (?:\d+(?:\.\d+)?)                               # 整數/小數 (e.g., 200, 0.5)
        # |
        
    ) # --- Group 1 結束 ---
    
    (?: # 單位部分 (可選)
        \s* # 0 或多個空格
        ( # Group 2: 捕獲「單位」本身
            [a-zA-Z%°\.一-龥]+   # 英文/符號/中文 
        ) # --- Group 2 結束 ---
    )? # 整個單位部分可選
    """

PATTERN_STR_VERBOSE_WITHOUT_NUMBERS = r"""
    # 直接選單位
    (\b\w+\b)   # 完全沒數字 (e.g., 適量))
    """
# Compiled pattern with numbers
COMPILED_PATTERN_WITH_NUMBERS = re.compile(
    PATTERN_STR_VERBOSE_WITH_NUMBERS,
    re.VERBOSE
)

# Compiled pattern without numbers
COMPILED_PATTERN_WITHOUT_NUMBERS = re.compile(
    PATTERN_STR_VERBOSE_WITH_NUMBERS,
    re.VERBOSE
)

# MANDARIN_FRACTION = re.compile(r"[一二三四五六七八九十]+分之[一二三四五六七八九十]+")

# convert the characters with the meaning of number to the relative numeric numbers
CHAR_NUM_MAPS ={
    "零": 0,
    "一": 1,
    "二": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
    "十": 10,
}


def get_num_in_field_quantity(text: str) -> float | str | None:
    """
    Separate the number and thr unit, and mainly fetch the number
    """
    have_num = any(num.isdigit() for num in text)
    if have_num:
        matches = COMPILED_PATTERN_WITH_NUMBERS.finditer(text) # bool
        if matches is not None:
            match_num_function(matches)
        return None
    else:
        return None

def match_num_function(matches) -> float | Decimal | str | None:
    """param matches: Iterator[Match[str]]"""

    for m in matches:
        try:
            """when value is presented as an integer or an integer with decimal, such as 1 or 1.5"""
            number_part = Decimal(m.group(1))
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
                    return m.group(1)

            elif any(sep in m.group(1) for sep in ("-", "~")):
                """when value is presented as a range of numbers, such as 4-5 or 4~5"""
                range_num = re.split(r"[-~]", m.group(1))
                first_num = Decimal(range_num[0])
                last_num = Decimal(range_num[-1])
                average = (first_num + last_num) / 2
                return average




"""
The instructions of processing the values of the quantity field :
use blank_comma_removal() to remove commas

"""

def blank_comma_removal(text: str) -> str:
    """
    Remove the comma symbol.
    Here it will also remove blanks.

    Param text : string
    Return : string
    """
    text = text.strip()
    text = text.replace(" ", "")

    if "," in text:
        text = text.replace(",", "")
        return text

    return text


def process_fraction_string():
    pass



# def separate_num_unit(string):
#     """
#     separate the ingredients' number and unit
#     param string: str, Quantity with unit
#     return: num: float, unit: string
#     """
#     _match = re.fullmatch(COMPILED_PATTERN, string)
#     if _match:
#         # extract the unit part
#         unit_part = match.group(2).strip().replace(" ", "")
#         try:
#             # extract the num part
#             num_part = float(match.group(1).strip().replace(" ", ""))
#             return num_part, unit_part
#
#         except ValueError:  # for fraction scenario
#             # extract the num part
#             fractions = match.group(1).strip().split("/")
#             numerator, denominator = map(int, fractions)
#             num_part = numerator / denominator
#             return num_part, unit_part
#     else:
#         return None, string


# def match_function(matches):
#     match_found = False
#     for m in matches:
#         match_found = True
#         number_part = m.group(1)
#         unit_part = m.group(2)  # 如果沒有匹配到，group(2) 會是 None
#
#         print(f"  > 找到: [原文: '{m.group(0)}']")
#         print(f"    - 數字 (Group 1): {number_part}")
#         print(f"    - 單位 (Group 2): {unit_part}")
#
#     if not match_found:
#         print("  > (未找到匹配)")