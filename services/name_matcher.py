from jellyfish import nysiis
from fuzzywuzzy import fuzz


# phonetic encoding (only english):
# nysiis = metaphone > soundex
def encode(name: str) -> str:
    return nysiis(name)


# string comparison:
# fuzz.ratio ~= jaro > damerau_levenshtein_distance > levenshtein_distance > hamming_distance
def compare_strings(input: str, name: str) -> float:
    # return jaro_similarity(input, name)
    return fuzz.ratio(input, name)


def find_best_name_match(list_names: list[str], input: str) -> str:
    encoded_list_names = [encode(name) for name in list_names]
    encoded_input = encode(input)

    max_similarity = 0
    best_name_match = None
    for i in range(len(encoded_list_names)):
        enc_med = encoded_list_names[i]
        name = list_names[i]

        similarity = compare_strings(encoded_input, enc_med)
        if similarity > max_similarity:
            print("Similarity:", similarity, "name:", name)
            max_similarity = similarity
            best_name_match = name
    return best_name_match
