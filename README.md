# 运动app 数据抓取

友情提醒：本文仅供学习技术，不要做违反法的事情
说到抓取网页数据，一般来说比较简单，会python 跑个爬虫框架基本上问题不大，app 抓取数据相对来说复杂一些，需要抓数据的人懂一点Android开发。
今天给大家介绍两种app 抓包方案。



# Fiddler 抓包
这个相对简单一些
主要原理就是 Fiddler 作为代理服务器，来转发接受app请求和接受数据，从而获取数据，可以像抓网页那样获取数据
这是不是本文重点,具体细节不提

# OCR抓取数据
由于很多app数据是加密的，我们抓到数据可能解析不了，这里就借鉴了文字识别ocr 能力。
具体过程如下
自动截图->截图上传到云平台->ocr 解析->返回数据导入文件中
## 自动截图
下面具体说下自动截图过程
根据app的页面结构，
第一页是个列表，点击一个列表项进去查看详情，然后截图，截图完成后返回列表，点击下一条,循环执行
```python 
while True:
    time.sleep(1)
    count++
    # 点击
    click_user()
    # 截图并上传pc 端
    screenshot.pull_pc()
    # 返回
    backup()
    # 下一个
    next_item()

```
截图使用的是Android的adb
```shell
adb  shell screencap -p xxx 截图
asb pull xxx  上传图片
```
模拟点击:进入，退出,需要根据手机型号确定x,y 数据
> adb shell input tap x  y

模拟拖动 列表
> adb shell input swipe x1 y1 x2 y3 duration

```python 
#click
def click_user():
    """
    点击进入
    """
    cmd = 'shell input tap {x} {y}'.format(
        x=config['click_bottom']['x'] + _random_bias(10),
        y=config['click_bottom']['y'] + _random_bias(10)
    )
    adb.run(cmd)

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

def next_item():
    """
    划到下一项
    """
    cmd = 'shell input swipe {x1} {y1} {x2} {y2} {duration}'.format(
        x1=config['center_point']['x'],
        y1=config['center_point']['y']+config['center_point']['ry'],
        x2=config['center_point']['x'],
        y2=config['center_point']['y'],
        duration=200
    )
    adb.run(cmd)
```
# 自定义ocr 模板
百度，阿里云都有，操作模式相同

以阿里云为例

1. 选择定位点，

2. 选择识别内容，

3. 保存，

4. 试一试，

5. 发布生成模板id 

注意点样图要清晰标准，余量充足


# 数据解析为excel
云平台返回的 json 数据，需要转换为json 数据
