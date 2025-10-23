import re

PATTERN_STR_VERBOSE = r"""
    ( # Group 1: 捕獲整個「數字」部分
        (?:\d+(?:\.\d+)?)[~-](?:\d+(?:\.\d+)?)   # 模組 A: 範圍 (e.g., 2-3)
        | 
        (?:\d+\/\d+)                             # 模組 B: 分數 (e.g., 1/2)
        | 
        (?:[一二三四五六七八九十百千萬]+)            # 模組 C: 中文數字 (e.g., 一)
        | 
        (?:\d+(?:\.\d+)?)                        # 模組 D: 整數/小數 (e.g., 200, 0.5)
    ) # --- Group 1 結束 ---
    
    (?: # 單位部分 (可選)
        \s* # 0 或多個空格
        ( # Group 2: 捕獲「單位」本身
            [a-zA-Z%°]+   # 英文/符號
            |
            [一-龥]+       # 中文
        ) # --- Group 2 結束 ---
    )? # 整個單位部分可選
    """

COMPILED_PATTERN = re.compile(PATTERN_STR_VERBOSE, re.VERBOSE)


def parse_quantities(text_list):
    """
    使用 re.VERBOSE 編譯的 Regex 來解析字串列表中的數量和單位
    """

    # --- 開始測試 ---
    for text in text_list:
        print(f"--- 測試: '{text}' ---")

        # 使用 finditer 獲取所有匹配的迭代器
        matches = COMPILED_PATTERN.finditer(text)

        match_found = False
        for m in matches:
            match_found = True
            number_part = m.group(1)
            unit_part = m.group(2)  # 如果沒有匹配到，group(2) 會是 None

            print(f"  > 找到: [原文: '{m.group(0)}']")
            print(f"    - 數字 (Group 1): {number_part}")
            print(f"    - 單位 (Group 2): {unit_part}")

        if not match_found:
            print("  > (未找到匹配)")

def separate_num_unit(string):
    """
    separate the ingredients' number and unit
    param string: str, Quantity with unit
    return: num: float, unit: string
    """
    match = re.fullmatch(COMPILED_PATTERN, string)
    if match:
        # extract the unit part
        unit_part = match.group(2).strip().replace(" ", "")
        try:
            # extract the num part
            num_part = float(match.group(1).strip().replace(" ", ""))
            return num_part, unit_part

        except ValueError:  # for fraction scenario
            # extract the num part
            fractions = match.group(1).strip().split("/")
            numerator, denominator = map(int, fractions)
            num_part = numerator / denominator
            return num_part, unit_part
    else:
        return None, string
