def _find_incorrectly_identified_range_characters(char: int, in_range: bool) -> (int, bool):
    if char == -91:  # 91 == [
        return 91 if in_range else -91, True
    elif char == -93:  # 93 == ]
        return 93 if not in_range else -93, False
    return char, in_range


def _find_closing_parenthesis_without_match(char: int, parentheses: int) -> (int, int):
    if char == -40:  # 40 == (
        return char, parentheses + 1
    elif char == -41:  # 41 == )
        return (41, 0) if not parentheses else (char, parentheses-1)
    return char, parentheses


def _random_number_range_can_apply(char: int, can_apply: bool) -> (int, bool):
    # [ord('{'), ord('}'), ord('+'), ord('*'), ord(',')]  # [123, 125, 43, 42, 44]

    match char:
        case -123:
            if can_apply: return char, False
            return abs(char), True
        case -125:
            if can_apply: return char, False
            return abs(char), True
        case -42:
            if can_apply: return char, False
            return abs(char), True
        case -43:
            if can_apply: return char, False
            return abs(char), True
        case _:
            if char in (-1 * ord('['), -1 * ord('('), -1 * ord('|')):
                return char, False
            return char, True


def _get_range_placeholder(start: int, max_iterations: str):
    return [-123, start, ord(',')] + [ord(char) for char in max_iterations] + [-125]


def iterate_chars(array: list, max_iterations) -> list:
    """
    This will iterate over the encoded characters and make sure that everything that should be formatted, is formatted and that everything that falls under the formatting category but can't be
    formatted due to reasons is converted back to its original character.

    This will also convert shortcuts to their full sequence.

    :param array:
    :param max_iterations: for + and * to identify the largest sequence these two characters can make so that there aren't just a bunch of infinitely long sequences designed by them
    :return:
    """

    in_range, parentheses, can_apply = False, 0, False
    for pos in range(len(array)):
        array[pos], in_range = _find_incorrectly_identified_range_characters(array[pos], in_range)
        array[pos], parentheses = _find_closing_parenthesis_without_match(array[pos], parentheses)
        array[pos], can_apply = _random_number_range_can_apply(array[pos], can_apply)

    index = 0
    new_array = []
    max_iterations = str(max_iterations)
    while index < len(array):
        if array[index] == -42:  # *
            new_array += _get_range_placeholder(ord('0'), max_iterations)
        elif array[index] == -43:  # +
            new_array += _get_range_placeholder(ord('1'), max_iterations)
        else:
            new_array.append(array[index])
        index += 1

    return new_array


class Codex:

    def __init__(self, string: str, max_iterations: int = 32, special_characters: list = None, shortcuts: dict = None):
        self.original_string = string
        self.special_characters: list = list('|-{}[]()+*?') if special_characters is None else special_characters
        self.max_iterations: int = max_iterations
        self.shortcuts: dict = {
            'd': '[0-9]',
            'w': '[a-zA-Z0-9_]',
            'W': '[A-Z0-9_]',
            **(shortcuts if shortcuts is not None else {})
        }

        self.encoded_string: list = self.encode(self.original_string)
        pass

    def check_for_shortcut(self, array, following_character):
        if following_character in self.shortcuts:
            array += [char_as_ord for char_as_ord in self.encode(self.shortcuts[following_character])]
        else:
            array.append(ord(following_character))

    def encode(self, string: str) -> list:
        array = []
        index = 0
        while index < len(string):
            if string[index] == '\\':
                self.check_for_shortcut(array, string[index + 1])  # array is appended in here
                # array.append(ord(string[index + 1]))
                index += 1
            elif string[index] in self.special_characters:
                array.append(-1 * ord(string[index]))
            else:
                array.append(ord(string[index]))

            index += 1
        array = iterate_chars(array, max_iterations=self.max_iterations)
        return array

    def decode(self, return_array=False):
        r_gex_chars = list('|-{}[]()+*?')
        string = []
        for char in self.encoded_string:
            if char < 0:
                string.append(chr(char * -1))
            elif chr(char) in r_gex_chars:
                string.append(f'\\{chr(char)}')
            else:
                string.append(chr(char))
        return string if return_array else ''.join(string)

    def __str__(self):
        return self.decode()
