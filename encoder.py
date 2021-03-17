# encoder.py is responsible for encoding and decoding strings
import re
import random

# regex to match words (alphanumeric + underscores), re.U allows for unicode to be matched too
_tokenize_re = re.compile(r"(\w+)", re.U)

# separator used in encoded text
SEPARATOR = "\n-weird-\n"


# encode_word shuffles the word's letters, excluding the first and last character
# @param word: single word to weird-encode
def encode_word(word: str) -> str:
    # encode doesn't make sense for words shorter or equal to 3 characters
    if len(word) <= 3:
        return word
    infix = word[1:-1]  # Remove the first and last character
    # Create a permutation of characters, then join the characters in list
    shuffled = "".join(random.sample(infix, len(infix)))
    # take care of a case where encoded word would be tha same as original
    if shuffled == infix:
        # this will cause the probability of reversed infix appearing to double
        # could be improved by making a custom shuffle function
        shuffled = infix[::-1]
    return word[0] + shuffled + word[-1]


# encode a string into the weird format
# @param text: string to be weird-encoded
def encode(text: str) -> str:
    tokens = re.findall(_tokenize_re, text)

    # sub_func replaces words with encoded ones
    def sub_func(match) -> str:
        return encode_word(match.group(1))

    # substitute every word with an encoded one
    encoded_text = re.sub(_tokenize_re, sub_func, text)
    sorted_unique_words = sorted(list(set(tokens)))
    # remove words shorter or equal to 3 characters
    sorted_unique_words = [s for s in sorted_unique_words if len(s) > 3]
    # create a space separated string of sorted words
    suw_string = " ".join(sorted_unique_words)
    return SEPARATOR + encoded_text + SEPARATOR + suw_string


# decode_word decodes a single weird-encoded word
# @param word: word to decode
# @param words: dictionary of words in original text
def decode_word(word: str, words: list) -> str:
    # trivial case, word's length is 3 or less
    if len(word) <= 3:
        return word
    for w in words:
        # possible candidate for unscrambled word must have the right length,
        # starting and ending character and contain the same chatacters as processed word
        if len(word) == len(w) and word[0] == w[0] and word[-1] == w[-1] and sorted(word) == sorted(w):
            return w
    raise ValueError(f"Cannot unscramble {word}, no valid candidate is present in the dictionary")


# decode a string from the weird format
# @param text: text in weird format to be decoded
def decode(text: str) -> str:
    parts = text.split(SEPARATOR)
    # split text should have empty data before -weird- tag, encoded data, and dictionary
    if len(parts) != 3:
        raise ValueError(f"The text doesn't appear to be weird encoded (missing {repr(SEPARATOR)} tags)")
    encoded_data = parts[1]  # type: str
    words_list = parts[2].split()  # type: List[str]

    def sub_func(match):
        return decode_word(match.group(1), words_list)

    # substitute encoded words with their decoded countrparts
    decoded_data = re.sub(_tokenize_re, sub_func, encoded_data)
    return decoded_data
