def make_assert(arg1, arg2, expression, operation, message):
    if not expression:
        print(f'''
            arg1: {arg1},
            arg2: {arg2},
            operation: {operation}
        ''')
        raise AssertionError

    assert expression, f'''
    arg1: {arg1},
    arg2: {arg2},
    operation: {operation},
    message: {message}
    '''


def assert_eq(arg1, arg2, message=''):
    make_assert(arg1, arg2, arg1 == arg2, '==', message)


def assert_neq(arg1, arg2, message=''):
    make_assert(arg1, arg2, arg1 != arg2, '!=', message)


def assert_l(arg1, arg2, message=''):
    make_assert(arg1, arg2, arg1 < arg2, '<', message)


def assert_le(arg1, arg2, message=''):
    make_assert(arg1, arg2, arg1 <= arg2, '<=', message)


def assert_g(arg1, arg2, message=''):
    make_assert(arg1, arg2, arg1 > arg2, '>', message)


def assert_ge(arg1, arg2, message=''):
    make_assert(arg1, arg2, arg1 >= arg2, '>=', message)


def assert_t(arg, message=''):
    make_assert(arg, None, arg, 'is True', message)


def assert_f(arg, message=''):
    make_assert(arg, None, not arg, 'is False', message)
