class PasswordTool(object):           #()中是父类
    def __init__(self, password):
        # 类初始化的属性
        self.password = password

    # 类的方法
    def abc(self):
       self.password += 1
       return(self.password)
    def abc1(self):
        self.password += 3
        return (self.password)

# 类的继承
class B(PasswordTool):
    def abc2(self):
        self.password += 2
        return (self.password)

# 类的super方法
class C(PasswordTool):
    def abc2(self):
       super(C, self).abc1()
       return (self.password)


# 实例化对象(类的使用）
password = input('请输入密码：')
passwordtool = B(int(password))
a = passwordtool.abc()

print(a)

# # 类变量和实例变量
# class Apple(object):
#     name = 'apple'
#
# p1 = Apple()
# p2 = Apple()
# p1.name = 'orange'
# print(p1.name)
# print(p2.name)
