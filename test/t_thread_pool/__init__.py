import time
from concurrent.futures import ThreadPoolExecutor


def fetch_url(url):
    print(url)
    time.sleep(2)
    return url + '-123456'


pool = ThreadPoolExecutor()
# Submit work to the pool
a = pool.submit(fetch_url, 'http://www.python.org')
b = pool.submit(fetch_url, 'http://www.pypy.org')

if __name__ == '__main__':
    # Get the results back
    x = a.result()
    y = b.result()

    print(x)
    print(y)
    print(1)
