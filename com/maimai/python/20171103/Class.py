#-*-coding=utf-8-*-
#类的名字，首字母，有一个不可文的规定，最好是大写，这样需要在代码中识别区分每个类。
class School:
    
    #它的内部有一个“self”，参数，它的作用是对于对象自身的引用。
    def fname(self, name):
        self.name = name