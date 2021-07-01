import sys
from aestate.work.commad import Commands

DEBUG = True
DEBUG_ARGS = ('aestate', '-check', 'example.tables.demoModels', '_demo')


def start():
    avg = sys.argv
    if DEBUG:
        avg = DEBUG_ARGS
    _ = Commands(*avg)
    if len(avg) == 1:
        _.c[''][0]()
    else:
        _.c[avg[1]][0]()


def parse_sys():
    pass


if __name__ == '__main__':
    start()
