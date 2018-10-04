# python

---

## 1. 导学
  1. simple is better than complex  简洁甚于复杂
  2. Now is better than never. Although never is often better than right now 做也许好过不做，但不加思索的去做还不如不做

## 2. 特点
  1. python 是一门编程语言
  2. 语法简洁，优雅，编写的程序容易阅读
  3. 跨平台，可以运行在windows linux 以及MacOs
  4. 易于学习
  5. 极为强大而丰富的标准库与第三方库，比如电子邮件，比如图形GUI界面
  6. oython是面向对象的语言

## 3. python能做什么
   1. 爬虫
   2. 大数据与数据分析
   3. 自动化运维与自动化测试
   4. web开发：flask, Django
   5. 机器学习 : Tensor Flow
   6. 胶水语言 : 混合自他如 C++。 Java等来编程。
   7.

## 4. 版本介绍
1. python 2.x 与 python 3.x 区别

## 5. 安装 python
  1. 下载 python3.7

## 基础语法
   1. int float number
   2. type(1) 类型检查
   3. type(2/2) float 型 type(2//2) int型
   4. 7.14版本 type(2/2) int
   5. 10进制， 二进制，八进制，16进制
   6. 0b10(2进制)  0o10(8进制)  0x10(16进制)
   7. 进制转换 bin(10)
      1. 转换成二进制
         1. bin(10)
         2. bin(0o7)
         3. bin(0xE)
      2. 转换成10进制
         1. int(0b111)
         2. int(0o77)
      3 转16进制
         1. hex(888)
         2. hex(0o77777)
      4. 转成8 禁止
         1. oct(0b111)
         2. oct(0o77)
   8. boll
      1. True
      2. False
      3. 非0的都为True bool(1.1)  bool(0)
      4. bool('') bool ([]) bool({}) bool(None)
   9. 复数 complex
      1. 36j
  10. str
      1. 单引号， 双引号，三引号
         1. “let's go”  'let\'s go'(增加转义字符)
      2. 字符串运算
        1. 字符串拼接  'hello ' + ' world'
        2. 字符串乘法  'hello' * 3 输出三次
        3. 截取字符   'hello wordl'[1]
        4. 截取字符 'hello world'[0:5]

   11. 转义字符
         1. \n 换行符
         2. \' 单引号
         3. \t 横向制表符
         4. \r 回车
         5. print('hello \\n world')
         6. print(r'1234567') r 将字符串原始输出
    12. 数据基础类型
        1. list
           1. type([1,2,3,4,5,6])
           2. type([1,"2",True, False])
           3. type([[1,"2",True, False]])
        2. 筛选 注意空格问题
           1. [1,2,3,4,5,6][0]
           2. [1,2,3,4,5,6][0:2]
        3. 列表合并
           1. [1,2,3] + ["4","5"] 加法
           2. [1,3,4]*2  乘法
        4. 分组
           1. [["巴西","克罗地亚","墨西哥","喀麦隆"]]
           2. 元祖 (1,2,3)
           3. 为什么 type((1)) 显示的是 int ? 优先级当作运算处理
           4. type((1,)) 增加的逗号
           5. 空的元祖  type(())
           