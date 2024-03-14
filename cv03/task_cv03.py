"""CV03"""


def factorize(n: int) -> list:
    """Rozklad čísla na prvočísla."""
    factors = []
    d = 2
    while n > 1:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    return factors


def queen(n: int, m: int, x: int, y: int) -> None:
    """
    Funkce vykresluje hraci plochu n x m.
    Na vstupní souřadnice umisťuje dámu a znakem * označuje
    všechna pole ohrožená dámou.
    """
    x -= 1
    y -= 1
    for i in range(n):
        for j in range(m):
            if (i == x and j == y):
                print('D', end='')
            elif i == x or j == y or abs(i - x) == abs(j - y):
                print('*', end='')
            else:
                print('.', end='')
        print()


def censor_number(n: int, c: int) -> None:
    """
    Funkce vypisuje posloupnost od 1 do prvního parametru.
    Čísla obsahující druhý vstup budou nahrazena hvězdičkou.
    """
    for i in range(1, n):
        if str(c) in str(i):
            print('*')
        else:
            print(i)


def text_analysis(text_file: str) -> dict:
    """
    Funkce vrací dvě struktury s výsledky provedné analýzy textu.
    První struktura obsahuje písmena a počet jejich výskytů.
    Druhá struktura obsahuje jednotlivá slova a počet jejich výskytů v textu.
    """
    with open(text_file, 'r', encoding='utf-8') as file:
        text = file.read()
        text = text.lower()
        text.replace('\n', ' ').replace(".", "").replace(
            ",", "").replace("!", "").replace("?", "")
        letters, words = {}, {}
        for char in text:
            if char.isalpha():
                if char in letters:
                    letters[char] += 1
                else:
                    letters[char] = 1
        for word in text.split():
            if word in words:
                words[word] += 1
            else:
                words[word] = 1
        letters = sorted(letters.items(), key=lambda x: x[1], reverse=True)
        words = sorted(words.items(), key=lambda x: x[1], reverse=True)
        return letters, words


def get_words(n: int, m: int, analysis: dict) -> dict:
    """
    Funkce vrací n slov o minimální délce m s nejvyšším výskytem včetně počtu
    """
    words = {}
    for word in analysis[1]:
        if len(word[0]) >= m:
            words[word[0]] = word[1]
        if len(words) == n:
            return words
    return words


INITIALS: dict = {
    0: "ا",
    1: "ب",
    2: "پ",
    3: "ت",
    4: "ث",
    5: "ج",
    6: "چ",
    7: "ح",
    8: "خ",
    9: "د",
    10: "ذ",
    11: "ر",
    12: "ز",
    13: "ژ",
    14: "س",
    15: "ش",
}

FINALS: dict = {
    0: "ص",
    1: "ض",
    2: "ط",
    3: "ظ",
    4: "ع",
    5: "غ",
    6: "ف",
    7: "ق",
    8: "ک",
    9: "گ",
    10: "ل",
    11: "م",
    12: "ن",
    13: "و",
    14: "ه",
    15: "ی",
}

NUMERALS = {
    0: "٠",
    1: "١",
    2: "٢",
    3: "٣",
    4: "٤",
    5: "٥",
    6: "٦",
    7: "٧",
    8: "٨",
    9: "٩",
}

PUNCTUATIONS = {
    ".": "۔",
    ",": "،",
    "!": "!",
    "?": "؟",
    ";": "؛",
    ":": ":",
}


def cypher(in_file: str, out_file: str) -> None:
    """
    Funkce text ze vstupního souboru šifruje do výstupního souboru
    """
    with open(in_file, 'r', encoding="utf-8") as file:
        text = file.read()

        new_text = ""
        for char in text:
            if char.isalpha():
                unicode = ord(char)
                initial = unicode // 16
                final = unicode % 16
                new_text += INITIALS[initial] + FINALS[final]
            elif char.isnumeric():
                num = NUMERALS[int(char)]
                new_text += num
            elif char in PUNCTUATIONS:
                punctuation = PUNCTUATIONS[char]
                new_text += punctuation
            else:
                new_text += char
    with open(out_file, 'w', encoding="utf-8") as file:
        file.write(new_text)

    return new_text


def decypher(in_file: str, out_file: str) -> None:
    """
    Funkce text ze vstupního souboru dešifruje do výstupního souboru
    """
    with open(in_file, 'r', encoding="utf-8") as file:
        text = file.read()
        new_text = ""
        for i, char in enumerate(text):
            if (char in INITIALS.values() and text[i + 1] in FINALS.values()):
                initial = list(INITIALS.keys())[
                    list(INITIALS.values()).index(char)]
                final = list(FINALS.keys())[
                    list(FINALS.values()).index(text[i + 1])]
                unicode = initial * 16 + final
                new_text += chr(unicode)
            elif (char in FINALS.values() and text[i - 1] in INITIALS.values()):
                continue
            elif char in NUMERALS.values():
                num = list(NUMERALS.keys())[
                    list(NUMERALS.values()).index(char)]
                new_text += str(num)
            elif char in PUNCTUATIONS.values():
                punctuation = list(PUNCTUATIONS.keys())[
                    list(PUNCTUATIONS.values()).index(char)]
                new_text += punctuation
            else:
                new_text += char

    with open(out_file, 'w', encoding="utf-8") as file:
        file.write(new_text)

    return new_text
