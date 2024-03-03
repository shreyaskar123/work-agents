def compute_slug(input_string):
    unique_chars = sorted(set(input_string.lower()), key=lambda x: (input_string.index(x), x))
    alphabet = set('abcdefghijklmnopqrstuvwxyz')
    remaining_chars = sorted(alphabet.difference(unique_chars))
    return unique_chars + remaining_chars