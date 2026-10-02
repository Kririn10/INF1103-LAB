import time

def green(end_time):
    light = 0
    while light != 3:
        if time.time() >= end_time:
            return

        print("go!")
        time.sleep(1)
        light += 1


def yellow(end_time):
    light = 0
    while light != 2:
        if time.time() >= end_time:
            return

        print("slow down!")
        time.sleep(1)
        light += 1


def red(end_time):
    light = 0
    while light != 3:
        if time.time() >= end_time:
            return

        print("stop!")
        time.sleep(1)
        light += 1


def main():
    start_time = time.time()
    end_time = start_time + 10

    while time.time() < end_time:
        green(end_time)

        if time.time() >= end_time:
            break

        yellow(end_time)

        if time.time() >= end_time:
            break

        red(end_time)


main()
