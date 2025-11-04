import re

PATTERN_STR_VERBOSE_WITH_NUMBERS = r"""
    ( # Group 1: 捕獲整個「數字」部分
        (?:[一二三四五六七八九十百千萬]+)分之(?:[一二三四五六七八九十百千萬]+)    # 中文表達分數 (e.g., 三分之二)
        |
        (?:\d+\/\d+)                                    # 分數 (e.g., 1/2)
        | 
        (?:[半一二三四五六七八九十百千萬]+)                  # 中文數字 (e.g., 一)
        | 
        (?:\d+(?:\.\d+)?)                               # 整數/小數 (e.g., 200, 0.5)
        # |

    ) # --- Group 1 結束 ---
    (?: # 單位部分 (可選)
        ( # Group 2: 捕獲「單位」本身
            [a-zA-Z%°\.一-龥]+   # 英文/符號/中文 
        ) # --- Group 2 結束 ---
    )? # 整個單位部分可選
    """

PATTERN_STR_VERBOSE_WITH_NUMBERS_RANGE = r"""
    ( # Group 1: 捕獲整個「數字」部分
        (?:[一二三四五六七八九十百千萬]+)分之(?:[一二三四五六七八九十百千萬]+)[-~～到至](?:[一二三四五六七八九十百千萬]+)分之(?:[一二三四五六七八九十百千萬]+)
        # 中文表達分數區間 (e.g., 三分之一-~～三分之二)
        |
        (?:[一二三四五六七八九十百千萬]+)分之(?:[一二三四五六七八九十百千萬]+)[-~～到至](?:[一二三四五六七八九十百千萬]+)
        |
        (?:[半一二三四五六七八九十百千萬]+)[-~～到至](?:[半一二三四五六七八九十百千萬]+) # 中文表達分數區間 (e.g., 二-~～三)
        |
        (?:(?:\d+(?:\/\d+)?[-~～](?:\d+(?:\/\d+)?)))                    # 範圍 (e.g., 1/3-1/2)
        |
        (?:(\d+(?:\.\d+)?[-~～_](?:\d+(?:\.\d+)?)))          # 範圍 (e.g., 2-3 (1.1-1.2))
    ) # --- Group 1 結束 ---
    ( # 單位部分 (可選)
        ( # Group 2: 捕獲「單位」本身
            [a-zA-Z%°\.一-龥]+   # 英文/符號/中文 
        ) # --- Group 2 結束 ---
    )? # 整個單位部分可選
"""

# PATTERN_STR_VERBOSE_WITHOUT_NUMBERS = r"""
#     # 直接選單位
#     (\b\w+\b)   # 完全沒數字 (e.g., 適量))
#     """

# Compiled pattern with numbers
COMPILED_PATTERN_WITH_NUMBERS = re.compile(
    PATTERN_STR_VERBOSE_WITH_NUMBERS,
    re.VERBOSE
)

COMPILED_PATTERN_WITH_NUMBERS_RANGE = re.compile(
    PATTERN_STR_VERBOSE_WITH_NUMBERS_RANGE,
    re.VERBOSE
)

# convert the characters with the meaning of number to the relative numeric numbers
CHAR_NUM_MAPS = {
    "零": 0,
    "半": 0.5,
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