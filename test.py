import asyncio


a = 0
c = 0
d = 10
b = 10
async def test1():
    global a
    while a < b:
        a += 1
        print("A",a)
        await asyncio.sleep(.25)
    a = 0

async def test2():
    global c
    while c <= d:
        c += 1
        print("\tC",c)
        await asyncio.sleep(.25)
    c = 0
tasks = []
async def main():
    for _ in range(3):
        print('\t\tDöngü',_)
        tasks.clear()
        print(tasks)
        tasks.append(asyncio.create_task(test1()))
        tasks.append(asyncio.create_task(test2()))
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())