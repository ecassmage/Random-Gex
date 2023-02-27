from .Objects import RGex
from .Coders import Codex


class RSGen:
    def __init__(self):
        pass

    @staticmethod
    def compile(string: str, max_iterations: int = 100, shortcuts: dict = None, **kwargs) -> RGex:
        return RGex(Codex(string, max_iterations=max_iterations, shortcuts=shortcuts).encoded_string, **kwargs)

    @staticmethod
    def get(string: str, max_iterations: int = 100, shortcuts: dict = None, **kwargs) -> str:
        return RGex(Codex(string, max_iterations=max_iterations, shortcuts=shortcuts).encoded_string, **kwargs).get()


# def compile_r_gex(string: str, max_iterations: int = 100, shortcuts: dict = None, **kwargs) -> RGex:
#     codex = Codex(string, max_iterations=max_iterations, shortcuts=shortcuts)
#     return RGex(codex.encoded_string, **kwargs)
#
#
# def get_r_gex(string: str, max_iterations: int = 100, shortcuts: dict = None, **kwargs):
#     return compile_r_gex(string, max_iterations=max_iterations, shortcuts=shortcuts, **kwargs).get()


if __name__ == '__main__':

    r = RSGen.compile(
        'Testing String Generator [0-9]  \\W{1,5}',
        shortcuts={
            'f': 'failure'
        }
    )

    for _ in range(100):
        print(RSGen.get('Testing String Generator [0-9]  \\W{1,5}', shortcuts={ 'f': 'failure' }))

    pass
