#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,os
import base64
import json
import xlwt
from urllib.parse import urlparse
import urllib.request
import base64
import time,datetime

ENCODING = 'utf-8'

def get_img_base64(img_file):
    with open(img_file, 'rb') as infile:
        s = infile.read()
        return base64.b64encode(s).decode(ENCODING)



def predict(url, appcode, img_base64, kv_configure):
        param = {}
        param['image'] = img_base64
        if kv_configure is not None:
            param['configure'] = json.dumps(kv_configure)
        body = json.dumps(param)
        data = bytes(body, "utf-8")

        headers = {'Authorization' : 'APPCODE %s' % appcode}
        request = urllib.request.Request(url = url, headers = headers, data = data)
        try:
            response = urllib.request.urlopen(request, timeout = 10)
            return response.code, response.headers, response.read()
        except urllib.request.HTTPError as e:
            return e.code, e.headers, e.read()


def jsonToexcel2(jsonfile):
    print (jsonfile)
    workbook = xlwt.Workbook()
    # 是否存在 suunto ，追加写入，写入后保存
    
    sheet1 = workbook.add_sheet('s')
    ll = list(jsonfile[0].keys())
    for i in range(0,len(ll)):
        sheet1.write(0,i,ll[i])
    for j in range(0,len(jsonfile)):
        m = 0
        ls = list(jsonfile[j].values())
        for k in ls:
            sheet1.write(j+1,m,k)
            m += 1
    workbook.save('s2.xls')



json_items=[]

def demo(img_file):
    appcode = 'youappcode'
    url = 'https://ocrdiy.market.alicloudapi.com/api/predict/ocr_sdt'

    configure ={"template_id":"your template_id"}
    #如果没有configure字段，configure设为None
    #configure = None

    img_base64data = get_img_base64(img_file)
    stat, header, content = predict( url, appcode, img_base64data, configure)
    #TODO 异常处理
    if stat != 200:
        print('Http status code: ', stat)
        print('Error msg in header: ', header['x-ca-error-message'] if 'x-ca-error-message' in header else '')
        print('Error msg in body: ', content)
        exit()
    result_str = content
    data=json.loads(result_str.decode(ENCODING))

    json_items.append(data['items'])

    writetxt('json2.txt',result_str.decode(ENCODING))

    
# TODO 异常处理
def writetxt(filename,data):
    file_handle=open(filename,mode='a+',encoding=ENCODING)
    file_handle.writelines(data+"\r\n")
    file_handle.close()

def writelisttxt(filename,data):
    file_handle=open(filename,mode='a+',encoding=ENCODING)
    file_handle.writelines(str(data))
    file_handle.close()

path_suunto = r"C:\Users\ec\Downloads\And-Bot\s2" 
suunto ='s2'

if __name__ == '__main__':
    files= os.listdir(path_suunto) #得到文件夹下的所有文件名称
    count=0
    for file in files:
        count=count+1
        start = time.time()
        writetxt('data_path.txt',file)
        demo(path_suunto+"\\"+file)
        end = time.time()
        t= end-start

        print('总数 {0} 文件 {1} {2} 耗时 {3}'.format(len(files),count,file,t))
    writelisttxt('json_item.txt',json_items)
    jsonToexcel2(json_items)    
