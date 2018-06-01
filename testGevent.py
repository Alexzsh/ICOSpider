import gevent
import greenlet


def callback(event, *args):
    print(    event, args[0], '===:>>>>', args[1])


# 想象成你的爬虫1
def foo():
    print('Running in foo')
    # 这个时候做了网络IO
    gevent.sleep(0)
    print('Explicit context switch to foo again')


# 想象成你的爬虫2
def bar():
    print('Explicit context to bar')
    # 这个时候做了网络IO
    gevent.sleep(0)
    print('Implicit context switch back to bar')


print('main greenlet info: ', greenlet.greenlet.getcurrent())
print('hub info', gevent.get_hub())
oldtrace = greenlet.settrace(callback('event',1,2))

gevent.joinall([
    gevent.spawn(foo),
    gevent.spawn(bar),
])
greenlet.settrace(oldtrace)
