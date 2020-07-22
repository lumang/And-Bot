# -*- coding:UTF-8 -*-
# -*- encoding: utf-8 -*-
import base64
import requests
import sys,os
import json
import time
import xlwt
ENCODING='UTF-8'

if sys.version_info.major == 2:
    from urllib import quote
else:
    from urllib.parse import quote



json_items=[]
item={'name':'','word_name':'','word':''}

path_suunto = r"C:\Users\ec\Downloads\And-Bot\s4" 
suunto ='s4'
# TODO 异常处理
def writetxt(filename,data):
    file_handle=open(filename,mode='a+',encoding=ENCODING)
    file_handle.writelines(data+"\r\n")
    file_handle.close()

def writelisttxt(filename,data):
    file_handle=open(filename,mode='a+',encoding=ENCODING)
    file_handle.writelines(str(data))
    file_handle.close()


def jsonToexcel2(jsonfile):
    print (jsonfile)
    workbook = xlwt.Workbook()
    # 是否存在 suunto ，追加写入，写入后保存
    
    sheet1 = workbook.add_sheet('suunto')
    ll = list(jsonfile[0].keys())
    for i in range(0,len(ll)):
        sheet1.write(0,i,ll[i])
    for j in range(0,len(jsonfile)):
        m = 0
        ls = list(jsonfile[j].values())
        for k in ls:
            sheet1.write(j+1,m,k)
            m += 1
    workbook.save('s4.xls')


headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'charset': "utf-8"
    }

def iocr(image_path):
    recognise_api_url = "https://aip.baidubce.com/rest/2.0/solution/v1/iocr/recognise"
    access_token = "access_token" 
    templateSign = "templateSign"

    classifierId = "your_classifier_id"
    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()
        if sys.version_info.major == 2:
            image_b64 = base64.b64encode(image_data).replace("\r", "")
        else:
            image_b64 = base64.b64encode(image_data).decode().replace("\r", "")

        # 请求模板的bodys
        recognise_bodys = "access_token=" + access_token + "&templateSign=" + templateSign + \
                "&image=" + quote(image_b64.encode("utf8"))
        # 请求分类器的bodys
        # classifier_bodys = "access_token=" + access_token + "&classifierId=" + classifierId + \
        #        "&image=" + quote(image_b64.encode("utf8"))

        # 请求模板识别
        response = requests.post(recognise_api_url, data=recognise_bodys, headers=headers)
        # 请求分类器识别
        # response = requests.post(recognise_api_url, data=classifier_bodys, headers=headers)

        print(response.text)
        print(response.json()['data']['ret'])
        for i in response.json()['data']['ret']:
            word_name=i['word_name']
            word=i['word']
            if(i['word_name']=='name'):
                item['name']=i['word']
            elif(i['word_name']=='odometer'):
                item['name']=i['word']
            elif(i['word_name']=="calorie"):
                item['name']=i['word']
            else:
                pass
        # items.append('{'+'{0},{1}'.format(word_name,word)+'}')
            print('{0} {1}'.format(word_name,word))
        json_items.append(item)
    except Exception as e:
        print (e)


if __name__ == '__main__':
    files=os.listdir(path_suunto)
    count=0
    for file in files:
        count=count+1
        start = time.time()
        writetxt('data_baidu.txt',file)
        iocr(path_suunto+"\\"+file)
        t=time.time()-start
        print('{0} 文件 {1} {2} 耗时 {3}'.format(len(files),count,file,t))
    writelisttxt('json_baidu_item2.txt',json_items)
    jsonToexcel2(json_items) 
