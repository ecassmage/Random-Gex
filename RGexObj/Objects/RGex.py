from .Nodes import Nodes


"""

(a|b)* | 
a -> b -> (c|d) -> e -> f
[a-b]*|(ab(c|d)ef|t)
((a|b)*|(ab(c|d)ef|t))
|_1  # add to stack at this point in the parse
| |_ a
| |_ b
|_2  # add to stack at this point in the parse
| |_ a
| | |_ b
| | | |_3  # add to stack at this point in the parse
| | | | |_ c
| | | | | |_ e
| | | | | |_ f
| | | | |_ d
| | | | | |_ e
| | | | | |_ f
| |_ t

"""


class RGex:
    def __init__(self, array, **kwargs):
        self.kwargs = kwargs
        self.root = Nodes()

        self.root.next_value = self._run(_build_r_gex_nested_array(array))

        self.clean()
        pass

    def clean(self): self.root.clean_pointers()
    def print(self): self.root.print_nodes()
    def get(self): return self.root.iterate_string()

    def _run(self, array):
        ptr = Nodes()
        pointers_to_return = [ptr]
        index = 0
        previous_ptr = None
        while index < len(array):
            val = array[index]
            if isinstance(val, list):
                temp = self._run(val)
                ptr = ptr.next_ptr()
                previous_ptr = ptr
                ptr.new_node_path(temp)
                ptr = ptr.next_ptr()
            elif val == -124:
                ptr = Nodes()
                pointers_to_return.append(ptr)
            elif val == -123:
                if previous_ptr is None:
                    pass
                pos = index + array[index:].index(-125) if -125 in array else - (index + 1)
                sub_string = ''.join(array[index + 1:pos] if pos > 0 else []).replace(' ', '').split(',')
                if len(sub_string) == 1:
                    sub_string = [sub_string[0], int(sub_string[0])+1]
                sub_string = [int(sub_string[0]), int(sub_string[1])]
                previous_ptr.repeater = sub_string
                previous_ptr = None
                index = pos
            else:
                temporary_pointer = Nodes(val)
                ptr = ptr.next_ptr(temporary_pointer)
                previous_ptr = ptr
            index += 1
        return pointers_to_return


def __miscellaneous(array, index, sub_array, inside_range, new_array):
    if inside_range:

        if array[index + 1] == -45 and index + 1 < len(array):  # -45 == -
            sub_array += [ascii_num for ascii_num in range(array[index], array[index + 2] + 1)]
            index += 2

        else:
            sub_array.append(array[index])

    else:
        new_array.append(array[index])

    return index


def __closed_bracket(sub_array, new_array):
    if sub_array: new_array.append(-40)  # (
    for num, val in enumerate(sub_array):
        if num != 0: new_array.append(-124)  # |
        new_array.append(val)
    if sub_array: new_array.append(-41)  # )

    return False


def __expand_ranges(array: list):
    inside_range = False
    new_array = []
    sub_array = []
    index = 0
    while index <= len(array) - 1:
        match array[index]:
            case -91:
                inside_range = True
            case -93:
                inside_range = False
                __closed_bracket(sub_array, new_array)
                sub_array = []
            case _:
                index = __miscellaneous(array, index, sub_array, inside_range, new_array)
        index += 1
    if index < len(array):
        new_array.append(array[index])
    return new_array


def _build_r_gex_nested_array(array: list):
    def add(*args):
        for arg in args:
            if arg != '':
                if isinstance(arg, str):
                    for char in list(arg): output.append(char)
                else:
                    output.append(arg)

    index = 0
    buffer = ['']
    output = []
    reference_stack = [output]

    array = __expand_ranges(array)

    while index < len(array):
        match array[index]:
            case -40:  # (
                temp = []
                add(buffer[-1], temp)
                buffer[-1] = ''
                reference_stack.append(output)
                output = temp
                buffer.append('')
            case -41:  # )
                add(buffer[-1])
                output = reference_stack.pop()  # ignore warning that occasionally pops up.
                buffer.pop()  # closed a nested section so removing highest level nesting
            case -124:  # |
                add(buffer[-1], -124)
                buffer[-1] = ''  # buffer has been applied, remove it
            case -42 | -43 | -123 | -125:
                add(buffer[-1], array[index])
                buffer[-1] = ''
            case _:
                buffer[-1] += chr(abs(array[index]))
        index += 1

    add(buffer[-1])
    return output


def __main__():
    # example = split(encode('(a{4}z+|b)*|(a{1, 2}b(c|d)ef|t)'))
    # ex = ['a', ['a', -124, 'b'], '*', -124, ['a', 'b', ['c', -124, 'd'], 'e', 'f', -124, 't']]
    # # root = Nodes()
    # root = Container(example)
    # for _ in range(100):
    #     print(root.build())
    # # root.print_nodes()
    # '(a|b)(c|d)(e|f)(g|h)'
    # """
    # a|b
    #   |_ c|d
    #   |    |_ e|f
    #   |    |    |_ g|h
    # """
    pass


if __name__ == '__main__':
    __main__()
    pass
