name = input('你想给谁发祝福：')


def cong(name1):
    a = list(map(lambda x: 'happy birthday to' + (' you' if x % 2 == 0 else ' '+name1+''), range(4)))
    return a


if __name__ == '__main__':
    print(cong(name))
b = input('如要退出请输入exit:')
