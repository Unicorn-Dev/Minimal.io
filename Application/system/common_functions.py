def static_vars(**kwargs):
    def wrapper(function):
        for key in kwargs:
            setattr(function, key, kwargs[key])
        return function
    return wrapper


@static_vars(errors_cnt=dict())
def try_wrapper(message, errors_limit, funk, *args):
    """
        В общем это  'обертка функции', котороая просто выполняет функцию,
    принимая ее аргументы, и следит вылетела функция или нет.
    Если функция упала, то увеличивается счетчик ошибок на этой функции
    и выводится трейсбек и месседж.
        Если счетчик превышает лимит, то обертка raise Exception.
    """
    try:
        funk(*args)
    except SystemExit as e:
        raise e
    except:
        from traceback import print_exc

        print_exc()
        print(message)
        try:
            try_wrapper.errors_cnt[funk]
        except:
            try_wrapper.errors_cnt[funk] = 0
        try_wrapper.errors_cnt[funk] += 1
        if (try_wrapper.errors_cnt[funk] >= errors_limit):
            try_wrapper.errors_cnt[funk] = 0
            raise Exception