__init_path__ = 'aestate/__init__.py'
__version__ = "1.0.1b1"
__description__ = "The Aestate framework is suitable for ORM frameworks of all web architectures in the Python language. " \
                  "The first ORM framework that supports custom sql grammar, allows you to customize your own sql grammar," \
                  "Adapting to all database creators who comply with DB-API2."
__author__ = "CACode"
__author_email__ = "cacode@163.com"
__url__ = "https://gitee.com/cacode_cctvadmin/aestate"

out_init = __version__, __description__, __author__, __author_email__


def input_default(*args):
    val = input(args[0])
    return val if val else args[1], val


def repo_url():
    val = input_default('repository url:', __url__)
    if not val[1]:
        val = val[0]
    return val


def version():
    val = input_default(f'version {__version__}:', __version__)
    if not val[1]:
        val = val[0]
    return val


def __out_init__(**kwargs):
    with open(__init_path__, 'w+') as f:
        for key, val in kwargs.items():
            out = [key, ' = ', '"', str(val), '"', '\n']
            print(*out)
            f.writelines(out)


if __name__ == '__main__':
    __version__ = version()
    __url__ = repo_url()
    __out_init__(__version__=__version__,
                 __url__=__url__,
                 __description__=__description__,
                 __author__=__author__,
                 __author_email__=__author_email__)
