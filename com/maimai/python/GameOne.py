# -*- coding=utf-8 -*-
temp=input('游戏猜数:')
guess=int(temp)
if guess ==8:
    print '好厉害'
else:
    if guess > 8:
        print '大了啊'
    else:
        print '小了'
print "game over"