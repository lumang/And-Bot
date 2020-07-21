# -*- coding: utf-8 -*-
import sys
import random
import time
from PIL import Image


if sys.version_info.major != 3:
    print('Please run under Python3')
    exit(1)
try:
    from common import debug, config, screenshot, UnicodeStreamFilter
    from common.auto_adb import auto_adb
    from common import apiutil
    from common.compression import resize_image
except Exception as ex:
    print(ex)
    print('请将脚本放在项目根目录中运行')
    print('请检查项目根目录中的 common 文件夹是否存在')
    exit(1)

VERSION = "0.0.1"

DEBUG_SWITCH = True

adb = auto_adb()
adb.test_device()
config = config.open_accordant_config()



def yes_or_no():
    """
    检查是否已经为启动程序做好了准备
    """
    while True:
        yes_or_no = str(input('请确保手机打开了 ADB 并连接了电脑，'
                              '然后打开手机软件，确定开始？[y/n]:'))
        if yes_or_no == 'y':
            break
        elif yes_or_no == 'n':
            print('谢谢使用', end='')
            exit(0)
        else:
            print('请重新输入')


def _random_bias(num):
    """
    random bias
    :param num:
    :return:
    """
    print('num = ', num)
    return random.randint(-num, num)

#back
def back_up():
    """
    返回
    :return:
    """
    cmd = 'shell input tap {x} {y}'.format(
        x=config['back_bottom']['x'] + _random_bias(10),
        y=config['back_bottom']['y'] + _random_bias(10)
    )
    adb.run(cmd)
    time.sleep(0.5)
    print("back")
#click
def click_user():
    """
    点击进入
    :return:
    """
    cmd = 'shell input tap {x} {y}'.format(
        x=config['click_bottom']['x'] + _random_bias(10),
        y=config['click_bottom']['y']
    )
    adb.run(cmd)
    time.sleep(0.5)
    print('click_user')

def next_page():
    """
    翻到下一页
    :return:
    """
    cmd = 'shell input swipe {x1} {y1} {x2} {y2} {duration}'.format(
        x1=config['center_point']['x'],
        y1=config['center_point']['y']+config['center_point']['ry'],
        x2=config['center_point']['x'],
        y2=config['center_point']['y'],
        duration=200
    )
    adb.run(cmd)
    time.sleep(1.5)
    print("next_item")


def main():
    """
    main
    :return:
    """
    print('程序版本号：{}'.format(VERSION))
    print('激活窗口并按 CONTROL + C 组合键退出')
    debug.dump_device_info()

    screenshot.check_screenshot()

    while True:
        

        time.sleep(1)
        click_user()
        time.sleep(2)
        screenshot.pull_screenshot()
        back_up()
        next_page()


if __name__ == '__main__':
    try:
        # yes_or_no()
        main()
    except KeyboardInterrupt:
        adb.run('kill-server')
        print('\n谢谢使用', end='')
        exit(0)
