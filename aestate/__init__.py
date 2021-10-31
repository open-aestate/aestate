import sys
from aestate.work.commad import Commands

DEBUG = False
DEBUG_ARGS = ('aestate', '-create', 'example.tables.demoModels', '_demo')


def start():
    print('暂不可用')
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
