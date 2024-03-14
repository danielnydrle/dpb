"""CV03 testy"""


from task_cv03 import cypher, decypher, factorize


def test_factorize():
    """Test funkce factorize."""
    assert not factorize(1)
    assert factorize(2) == [2]
    assert factorize(3) == [3]
    assert factorize(4) == [2, 2]
    assert factorize(10) == [2, 5]
    assert factorize(12) == [2, 2, 3]
    assert factorize(13) == [13]
    assert factorize(100) == [2, 2, 5, 5]
    assert factorize(373) == [373]
    assert factorize(999) == [3, 3, 3, 37]
    assert factorize(1000) == [2, 2, 2, 5, 5, 5]


def check_cyphering(in_file: str, out_file_cyphered: str, out_file_decyphered: str) -> bool:
    """
    Funkce porovnává výsledek šifrování a dešifrování.
    """
    cypher(in_file, out_file_cyphered)
    decypher(out_file_cyphered, out_file_decyphered)
    with open(in_file, 'r', encoding='utf-8') as f1:
        with open(out_file_decyphered, 'r', encoding='utf-8') as f2:
            line1 = f1.readline()
            line2 = f2.readline()
            while line1 and line2:
                if line1 != line2:
                    print(line1)
                    print(line2)
                    return False
                line1 = f1.readline()
                line2 = f2.readline()
    return True


def test_cypher():
    """Test funkce cypher."""
    assert check_cyphering('cv03/book.txt', 'cv03/book_cyphered.txt',
                           'cv03/book_decyphered.txt')
