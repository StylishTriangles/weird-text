import random
import encoder
import pytest

def random_word(letters: str, length: int) -> str:
    return "".join(random.choices(letters, k=length))

def random_alphanum_word(length: int) -> str:
    word_spec = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return random_word(word_spec, length)

#### ENCODE_WORD TESTS ####

def assert_correct_encoding(original: str, scrambled: str):
    assert len(original) == len(scrambled)
    assert original[0] == scrambled[0] 
    assert original[-1] == scrambled[-1]
    assert sorted(original) == sorted(scrambled) # must contain the same letters

def test_encode_word_short_random():
    test_size = 100
    # random alphanumeric words of lengths 1 to 3
    words = [random_alphanum_word(random.choice(range(1,4))) for _ in range(test_size)]
    for w in words:
        assert w == encoder.encode_word(w)

def test_encode_word_long_random():
    test_size = 100
    min_len, max_len = 4, 100
    words = [random_alphanum_word(random.choice(range(min_len,max_len+1))) for _ in range(test_size)]
    for w in words:
        assert_correct_encoding(w, encoder.encode_word(w))


def test_encode_word_unicode():
    words = ["kałuża", "😉😉🥱😶", "媽且月阿界期達角來輕", "♖♘♗♕♔♗♘♖"]
    for w in words:
        assert_correct_encoding(w, encoder.encode_word(w))

#### ENCODE TESTS ####

def test_encode():
    text = "Litwo, Ojczyzno moja! ty jesteś jak zdrowie;\nIle cię trzeba cenić, ten tylko się dowie"
    sorted_words = "Litwo Ojczyzno cenić dowie jesteś moja trzeba tylko zdrowie"
    encoded_text = encoder.encode(text)
    parts = encoded_text.split(encoder.SEPARATOR)
    assert len(parts) == 3 # check if text contains 2 separators
    assert parts[2] == sorted_words

#### DECODE TESTS ####

def test_decode_validation():
    bad_separator = encoder.SEPARATOR + "aaa a aaaaaa" + "\n-weird#-\n" + "aaa aaaaaa"
    with pytest.raises(ValueError):
        encoder.decode(bad_separator)

def test_decode_simple():
    encoded = "random stuff" + encoder.SEPARATOR + "Tihs is Sartpa!!!" + encoder.SEPARATOR + "Sparta This"
    assert encoder.decode(encoded) == "This is Sparta!!!"

def test_decode_encode():
    text = "Hello World! 😉 Lorem ipsum, random words, punctuation; even some unicode: 醤油"
    encoded = encoder.encode(text)
    assert encoder.decode(encoded) == text

def test_decode_ambiguous():
    text = "mango magno"
    encoded = encoder.encode(text)
    decoded = encoder.decode(encoded)
    decoded = decoded.split()
    assert decoded[0] == "magno" or decoded[0] == "mango"
    assert decoded[1] == "magno" or decoded[1] == "mango"

#### DECODE_WORD TESTS ####

def test_decode_word_validation():
    word = "unavailable"
    words = ["unobtainable", "heavy", "none"]
    with pytest.raises(ValueError):
        encoder.decode_word(word, words)