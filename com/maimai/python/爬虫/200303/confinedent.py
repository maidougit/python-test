#-*- coding:utf8 -*-
import datetime

# 末次生理期 = 预产期 - 280 - 1
# 孕周天数差值 = (当前时间 - 末次生理期)
# 孕周 = 孕周天数差值 / 7
# 孕天 = 孕周天数差值 % 7
def confinement_date(confinement_date):
    today = datetime.date.today()
    diffday = (today - confinement_date).days + 280
    yunzhou = int(diffday/7)
    yuntian = diffday % 7
    print(yunzhou,'周', yuntian,'天')




if __name__ == '__main__':
    confinement_date(datetime.date(2020, 12, 1))