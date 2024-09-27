from time import time

# Round Robin

def gen_filename():
    while True:
        pattern = 'file-{}.jpeg'
        t = int(time() * 1000)

        yield pattern.format(str(t))

        sum = 234 + 234
        print(sum)

# g = gen_filename()

def gen(s):
    for i in s:
        yield i
        

def gen1():
    for i in s:
        yield i


def gen2():
    for i in range(n):
        yield n


g1 = gen1('artur')
g2 = gen2(4)

tasks = [g1, g2]

while tasks:
    task = tasks.pop(0)

    try:
        i = next(task)
        print(i)
        tasks.append(task)
    except StopIteration:
        pass
