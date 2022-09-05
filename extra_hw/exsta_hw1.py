def make_readable(seconds: int):
    print(f'{int(seconds//36000)}{int(seconds//3600%10)}:{int(seconds//60%60//10)}{int(seconds//60%60%10)}:{int(seconds%60//10)}{int(seconds%60%10)}')


make_readable(0)
make_readable(5)
make_readable(60)
make_readable(86399)
make_readable(359999)