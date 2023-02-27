try:
    from .RGexObj import RSGen
    # from .RGexObj import compile_r_gex as __compile__, get_r_gex as __get_r__
except ImportError:
    from RGexObj import RSGen
    # from RGexObj import compile_r_gex as __compile__, get_r_gex as __get_r__


# if __name__ == "__main__":
#     for _ in range(10): print(RSGen.get('This is a test|This is not a test'))
