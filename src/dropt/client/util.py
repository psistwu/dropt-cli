'''util.py

Module util includes all common utility functions used
by other modules in dropt-cli library.
'''


def is_float(string):
    '''Check a given string can be converted to a float number.'''
    try:
        float(string)
        return True
    except ValueError:
        return False
