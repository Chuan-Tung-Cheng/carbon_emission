import re

#1又 1/2

PATTERN_STR_VERBOSE_WITH_NUMBERS = r"""
    ( # Group 1: 捕獲整個「數字」部分
        (?:[一二三四五六七八九十百千萬]+)分之(?:[一二三四五六七八九十百千萬]+)    # 中文表達分數 (e.g., 三分之二)
        |

    ) # --- Group 1 結束 ---
    (?: # 單位部分 (可選)
        ( # Group 2: 捕獲「單位」本身
            [a-zA-Z%°\.一-龥]+   # 英文/符號/中文 
        ) # --- Group 2 結束 ---
    )? # 整個單位部分可選
    """

#### 100g or 1.5g, it works
PATTERN_WITH_DIGITAL_WITHOUT_RANGE = r"""
    ((?:\d+(?:\.\d+)?)) # num part
    (?:\s?([a-zA-Z%°\.一-龥]+))? # unit part
"""

CMP_PATTERN_WITH_DIGITAL_WITHOUT_RANGE = re.compile(
    PATTERN_WITH_DIGITAL_WITHOUT_RANGE,
    re.VERBOSE
)
#### 100g or 1.5g

#### 1/3g or 1 1/3 kg or 1又1/3 公斤, it works
PATTERN_WITH_DIGITAL_FRACTION_WITHOUT_RANGE = r"""
    ((?:\d?[\s|又]?\d+\/\d+))
    (?:\s?([a-zA-Z%°\.一-龥]+))?
"""

CMP_PATTERN_WITH_DIGITAL_FRACTION_WITHOUT_RANGE = re.compile(
    PATTERN_WITH_DIGITAL_FRACTION_WITHOUT_RANGE,
    re.VERBOSE
)
#### 1/3g

#### 三公斤 or 三 公斤, it works
PATTERN_WITH_CHINESE_NUM_WITHOUT_RANGE = r"""
    ((?:[半一二三四五六七八九十百千萬]+))
    (?:\s?([a-zA-Z%°\.一-龥]+))?
"""

CMP_PATTERN_WITH_CHINESE_WITHOUT_RANGE = re.compile(
    PATTERN_WITH_CHINESE_NUM_WITHOUT_RANGE,
    re.VERBOSE
)
#### 三公斤 or 三 公斤


#### 三分之一公斤 or 三分之一 公斤 or 一又三分之一 公斤, it works
PATTERN_WITH_CHINESE_NUM_FRACTION_WITHOUT_RANGE = r"""
    (?:([一二三四五六七八九十百千萬]?又?[一二三四五六七八九十百千萬]+分之[一二三四五六七八九十百千萬]+))
    (?:\s?([a-zA-Z%°\.一-龥]+))?
"""
CMP_PATTERN_WITH_CHINESE_FRACTION_WITHOUT_RANGE = re.compile(
    PATTERN_WITH_CHINESE_NUM_FRACTION_WITHOUT_RANGE,
    re.VERBOSE
)
#### 三分之一公斤 or 三分之一 公斤


PATTERN_STR_VERBOSE_WITH_NUMBERS_RANGE = r"""
    ( # Group 1: 捕獲整個「數字」部分
        (?:[一二三四五六七八九十百千萬]+)分之(?:[一二三四五六七八九十百千萬]+)[-~～到至](?:[一二三四五六七八九十百千萬]+)分之(?:[一二三四五六七八九十百千萬]+)
        # 中文表達分數區間 (e.g., 三分之一-~～三分之二)
        |
        (?:[一二三四五六七八九十百千萬]+)分之(?:[一二三四五六七八九十百千萬]+)[-~～到至](?:[一二三四五六七八九十百千萬]+)
        |
        (?:[半一二三四五六七八九十百千萬]+)[-~～到至](?:[半一二三四五六七八九十百千萬]+) # 中文表達分數區間 (e.g., 二-~～三)
        |
    ) # --- Group 1 結束 ---
    ( # 單位部分 (可選)
        ( # Group 2: 捕獲「單位」本身
            [a-zA-Z%°\.一-龥]+   # 英文/符號/中文 
        ) # --- Group 2 結束 ---
    )? # 整個單位部分可選
"""

#### 約1-2kg, 1.1~2 kg, 1～2.1 kg, 1至2 kg, it works
PATTERN_WITH_DIGITAL_RANGE = r"""
    (?:(\d+(?:\.\d+)?[-~～_至]\d+(?:\.\d+)?))
    (?:\s?([a-zA-Z%°\.一-龥]+))?
"""

CMP_PATTERN_WITH_DIGITAL_RANGE = re.compile(
    PATTERN_WITH_DIGITAL_RANGE,
    re.VERBOSE
)

#### 約1/2-1kg, 1/3~1/2 kg, 0.5-2/3 kg, 1又1/2～2.1 kg, it works
PATTERN_WITH_DIGITAL_FRACTION_RANGE = r"""
    ((?:(?:\d+[\s|又]?)?\d+\/\d+|\d+(?:\.\d+)?)(?:[-~～_至](?:(?:\d+[\s|又]?)?\d+\/\d+|\d+(?:\.\d+)?))?)
    (?:\s?([a-zA-Z%°\.一-龥]+))?
"""

CMP_PATTERN_WITH_DIGITAL_FRACTION_RANGE = re.compile(
    PATTERN_WITH_DIGITAL_FRACTION_RANGE,
    re.VERBOSE
)
#### 約1/2-1kg, 1/3~1/2 kg, 0.5-2/3 kg, 1又1/2～2.1 kg


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

def blank_comma_removal(text: str) -> str:
    """
    For field: people
    Remove the comma symbol.
    Here it will also remove blanks.
    """
    text = text.replace("\n", "").replace("\t","").strip()

    if "," in text:
        text = text.replace(",", "")
        return text
    return text


if __name__ == "__main__":
    text = "約0.5~1又1/2 公斤"
    matches =re.finditer(CMP_PATTERN_WITH_DIGITAL_FRACTION_RANGE, text)
    for m in matches:
        print(m.group(0))
        print(m.group(1))
        print(m.group(2))
