import os

# path = r"C:\Users\ec\Downloads\xdfman-Douyin-Bot-master\Douyin-Bot" 
# #文件夹目录
# files= os.listdir(path) #得到文件夹下的所有文件名称
# txts = []
# for file in files: #遍历文件夹
#     position = path+'\\'+ file
#     print (position)           
    # with open(position, "r",encoding='utf-8') as f:    #打开文件        
    #     lines = f.readlines()   #读取文件中的一行
    #     for line in lines:
    #         txts.append(line)
    #     f.close()
# print (txts)

import xlwt,json

items=[]
def readJsonfile():
    # json_file=json.load(r'C:\Users\ec\Downloads\xdfman-Douyin-Bot-master\Douyin-Bot\477.json')
    f = open(r'C:\Users\ec\Downloads\xdfman-Douyin-Bot-master\Douyin-Bot\477.json','r',encoding='UTF-8')
    for line in f:
        item = json.loads(line)
        items.append(item['items'])
        print(item['items'])
    return items

def jsonToexcel2():
    jsonfile = readJsonfile()
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
    workbook.save('suunto202007.xls')

jsonToexcel2()