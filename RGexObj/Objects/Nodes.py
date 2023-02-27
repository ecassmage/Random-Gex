import random


class Nodes:
    def __init__(self, value: str = ''):
        self.value: str = value
        self.next_value: list[Nodes] = []
        self.ptr: Nodes | None = None  # next node in path
        self.repeater: list[int] = [1, 1]
        # an array of values for which to choose from, In the case of linear Grammar like ab,
        # next_value and ptr would be the same but a|b would split before reconnecting on the same path

    def iterate_string(self):
        string = ''
        for _ in range(random.randrange(self.repeater[0], self.repeater[1] + 1)):
            string += self.value
            if self.next_value:
                choice = random.choice(self.next_value)
                string += choice.iterate_string()
        string += self.ptr.iterate_string() if self.ptr is not None else ''
        return string

    def next(self):
        return self.next_value

    def new_node_path(self, pointers=None):
        if isinstance(pointers, Nodes):
            self.next_value.append(pointers)
        else:
            self.next_value += pointers

    def next_ptr(self, ptr=None):
        if ptr is None:
            ptr = Nodes()
        self.ptr = ptr
        return self.ptr

    def get_next(self):
        if len(self.next_value) == 1 and self.next_value[0] == self.ptr:
            return self.ptr
        return random.choice(self.next_value)

    def print_nodes(self, indent=0, spacing=3):
        def call_next(ind, spc):
            temp = ind
            for node in self.next_value:
                temp = node.print_nodes(indent=ind, spacing=spc)
                if self.ptr is not None:
                    temp = self.ptr.print_nodes(indent=temp, spacing=spc)
            if not self.next_value and self.ptr is not None:
                temp = self.ptr.print_nodes(indent=temp, spacing=spc)
            return temp

        if self.value != '':
            for _ in range(indent):
                print(f'|{" " * spacing}', end='')
            print('|_', self.value, self.repeater)
            indent = call_next(indent + 1, spacing)
        else:
            for _ in range(indent):
                print(f'|{" " * spacing}', end='')
            print('|_', self.repeater)
            indent = call_next(indent + 1, spacing)
        return indent

    def clean_pointers(self):
        for num, ptr in enumerate(self.next_value):
            if ptr.value == '':
                self.next_value[num] = ptr.ptr
                ptr.ptr.clean_pointers()
            else:
                ptr.clean_pointers()
            pass
        self.next_value = [value for value in self.next_value if self.next_value is not None]

        while self.ptr is not None:
            if self.ptr.value == '' and self.ptr.repeater == [1, 1] and not self.ptr.next_value:
                self.ptr = self.ptr.ptr
            else: break
        else:
            return
        self.ptr.clean_pointers()


"""
    def print_nodes(self, indent=None, spacing=3, indented=0):
        def call_next(ind, spc, indenter):
            ind.append(ind[-1] if ind else False)

            temp = copy.copy(ind)
            for node in self.next_value:
                ind[-1] = not (node == self.next_value[-1])
                temp = node.print_nodes(indent=copy.copy(ind), spacing=spc, indented=indenter)
                if self.ptr is not None:
                    temp = self.ptr.print_nodes(indent=copy.copy(temp), spacing=spc, indented=indenter)
            if not self.next_value and self.ptr is not None:
                temp = self.ptr.print_nodes(indent=copy.copy(temp), spacing=spc, indented=indenter)
            return temp

        if indent is None: indent = []

        if self.value != '':
            if True:
                pass
            for val in indent:
                print(f'|{" " * spacing}', end='') if val else print(f' {" " * spacing}', end='')
                # print(f'|{" " * spacing}', end='')
            print('|_', self.value, self.repeater)

            indent = call_next(indent, spacing, indented+1)
        else:
            if True:
                pass
            for val in indent:
                print(f'|{" " * spacing}', end='') if val else print(f' {" " * spacing}', end='')
                # print(f'|{" " * spacing}', end='')
            print('|_', self.repeater)

            indent = call_next(indent, spacing, indented+1)
        return indent


"""
