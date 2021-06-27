import sys

from . import commad as _


def version():
    pass


def start():
    c = _.Commands()
    if len(sys.argv) == 1:
        c.c[''][0]()
    else:
        c.c[sys.argv[1]][0]()


def parse_sys():
    pass


if __name__ == '__main__':
    start()
