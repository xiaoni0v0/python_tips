import time

n = 20

for i in range(n):
    print('\r进度：[%s%s]' % ('■' * i, '□' * (n - i)), end='')
    time.sleep(0.1)
