try:
    from .Codex import Codex
except ImportError:
    from Codex import Codex


def __main__():
    C = Codex("This{1,3} i+s* [aA] test (string)")
    pass


if __name__ == '__main__':
    __main__()
    pass
