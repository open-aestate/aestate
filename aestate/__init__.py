import sys

from aestate.work.commands import Commands

DEBUG = False
DEBUG_ARGS = ('aestate', '-create', 'testOpera.table.demoModels', 'demo')


def start():
    avg = sys.argv
    print(avg)
    if DEBUG:
        avg = DEBUG_ARGS
    _ = Commands(*avg)
    if len(avg) == 1:
        _.c[''][0]()
    else:
        _.c[avg[1]][0]()


if __name__ == '__main__':
    start()
