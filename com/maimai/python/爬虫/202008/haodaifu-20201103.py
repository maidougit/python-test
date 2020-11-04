import urllib.parse
import ssl
from multiprocessing.dummy import Pool as ThreadPool,Manager
import  json
import pymysql as pm
from warnings import filterwarnings
filterwarnings('error', category=pm.Warning)
import urllib
import urllib.request,csv
from urllib.request import Request, urlopen


def db():
    db = pm.connect(host='192.168.1.56', port=3306,
                         user='root', passwd='Yly,1O1', db='xr-doctor-test', charset='utf8',cursorclass=pm.cursors.DictCursor)
    return db

# SQL 插入语句
sql = "select  * from t_hdf_doctor_list_20201102 where is_deal2 = 0"


request_url = {
    # {"errorCode":0,"msg":"","data":{"isOpenFollowup":0,"yesterdayCnt":3098,"patientSigninCnt":0,"spaceRepliedCount":7291,"doctorVoteCnt":"1123","thankLetterCount":"554","spaceActiveDate":"今天","openSpaceTime":"2010-08-10 20:45","yesterdayDate":1604210325}}
    "ajaxGetDoctorData":"https://renxianguo.haodf.com/ndoctor/ajaxGetDoctorData?spaceId={spaceId}",
    # {"errorCode":0,"msg":"","data":3969376}
    "ajaxGetSpaceHits":"https://renxianguo.haodf.com/ndoctor/ajaxGetSpaceHits?doctorId={doctorId}",
    # {"errorCode":0,"msg":"","data":[0,2627,2677]} 昨日诊后报到患者  微信诊后报到患者  总诊后报到患者
    "ajaxGetDoctorOtherData":"https://renxianguo.haodf.com/ndoctor/ajaxGetDoctorOtherData?"
}


def request_param(spaceId):
    param = {
        "startTime":"2020-11-01 00:00:00",
        "endTime":"2020-11-01 23:59:59",
        "spaceId":spaceId
    }

    return param

#更新sql
#  `statC_zuorifangwen` text COMMENT '昨日访问',
#   `statC_suifanghuanzheshu` text COMMENT '随访患者数',
#   `statC_zongwenzhang` text COMMENT '总文章',
#   `statC_zonghuanzhe` text COMMENT '总患者',
#   `statC_zuorizhenghoubaodaohuanzhe` text COMMENT '昨日诊后报到患者',
#   `statC_weixinzhenhoubaodaohuanzhe` text COMMENT '微信诊后报到患者',
#   `statC_zongzhenhoubaodaohuanzhe` text COMMENT '总诊后报到患者',
#   `statC_huanzhetoupiao` text COMMENT '患者投票',
#   `statC_ganxiexin` text COMMENT '感谢信',
#   `statC_xinyiliwu` text COMMENT '心意礼物',
#   `statC_shangcizaixian` text COMMENT '上次在线',
#   `statC_kaitongshijian` text COMMENT '开通时间',
sql_update ='''
update t_hdf_doctor_list_20201102 
set statC_zuorifangwen = '{statC_zuorifangwen}',
statC_suifanghuanzheshu='{statC_suifanghuanzheshu}', 
statC_zongwenzhang ='{statC_zongwenzhang}',
statC_zonghuanzhe ='{statC_zonghuanzhe}',
statC_zuorizhenghoubaodaohuanzhe ='{statC_zuorizhenghoubaodaohuanzhe}',
statC_weixinzhenhoubaodaohuanzhe ='{statC_weixinzhenhoubaodaohuanzhe}',
statC_zongzhenhoubaodaohuanzhe ='{statC_zongzhenhoubaodaohuanzhe}',
statC_huanzhetoupiao ='{statC_huanzhetoupiao}',
statC_ganxiexin ='{statC_ganxiexin}',
statC_xinyiliwu ='{statC_xinyiliwu}',
statC_shangcizaixian ='{statC_shangcizaixian}',
statC_kaitongshijian ='{statC_kaitongshijian}',
where serial = {serial}
'''

requesturl = 'https://gw.xingren.com/consult/common/api/doctor/homepage/{serial}/intro'



def header2() :
    header = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Chromium";v="86", ""Not\\A;Brand";v="99", "Google Chrome";v="86"',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://renxianguo.haodf.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie': 'UM_distinctid=17586f1ee4b1ea-07f8e1eb5ac9b5-303464-1fa400-17586f1ee4c42b; _ga=GA1.2.550920409.1604286804; _gid=GA1.2.371788661.1604286804; Hm_lvt_dfa5478034171cc641b1639b2a5b717d=1604286804; __jsluid_s=8790bbff442fd45d611dda8d718c6f1d; g=3390_1604286822675; CNZZDATA-FE=CNZZDATA-FE; Hm_lpvt_dfa5478034171cc641b1639b2a5b717d=1604286823',
        'If-None-Match': 'W/"2d-HEQt9yjq4z4HGf3p9GyEwQ"'
    }

    return header

def header1() :
    header = {
         'Connection': 'keep-alive',
          'sec-ch-ua': '"Chromium";v="86", ""Not\\A;Brand";v="99", "Google Chrome";v="86"',
          'Accept': '*/*',
          'X-Requested-With': 'XMLHttpRequest',
          'sec-ch-ua-mobile': '?0',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
          'Sec-Fetch-Site': 'same-origin',
          'Sec-Fetch-Mode': 'cors',
          'Sec-Fetch-Dest': 'empty',
          'Referer': 'https://renxianguo.haodf.com/',
          'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
          'Cookie': 'UM_distinctid=17586f1ee4b1ea-07f8e1eb5ac9b5-303464-1fa400-17586f1ee4c42b; _ga=GA1.2.550920409.1604286804; _gid=GA1.2.371788661.1604286804; Hm_lvt_dfa5478034171cc641b1639b2a5b717d=1604286804; __jsluid_s=8790bbff442fd45d611dda8d718c6f1d; g=3390_1604286822675; CNZZDATA-FE=CNZZDATA-FE; Hm_lpvt_dfa5478034171cc641b1639b2a5b717d=1604286823',
          'If-None-Match': 'W/"27-VjvUjNrBOgkXp1IT4nnfcQ"'
    }

    return header

#查询
def select():
    sdb1 = db()
    cursor = sdb1.cursor()
    try:
        cursor.execute(sql)  # 执行sql语句
        results = cursor.fetchall()  # 获取查询的所有记录
        sdb1.commit()
        return results
    except pm.Warning as w:
        print(repr(w))
        # 如果发生错误则回滚
        sdb1.rollback()
    finally:
        sdb1.close()

#更新数据
def updateData(each):
    sdb2 = db()
    cursor = sdb2.cursor()
    try:
        # 像sql语句传递参数
        update = "update t_hdf_doctor_list_20201102  set zuorizhenghoubaodaohuanzhe = '{zuorizhenghoubaodaohuanzhe}',weixinzhenhoubaodaohuanzhe='{weixinzhenhoubaodaohuanzhe}', zongzhenhoubaodaohuanzhe ='{zongzhenhoubaodaohuanzhe}',total_visits ='{total_visits}',is_deal2 = 1 where  doctorId = {doctorId};"
        sql_update1 = update.format(zuorizhenghoubaodaohuanzhe=each['zuorizhenghoubaodaohuanzhe'],
                                    weixinzhenhoubaodaohuanzhe=each['weixinzhenhoubaodaohuanzhe'],
                                    zongzhenhoubaodaohuanzhe=each['zongzhenhoubaodaohuanzhe'],
                                    total_visits=each['total_visits'],
                                    doctorId=each['doctorId']
                                    )
        print(sql_update1)
        cursor.execute(sql_update1)
        # 提交
        sdb2.commit()
    except Exception as e:
        # 错误回滚
        print(e)
        sdb2.rollback()
    finally:
        sdb2.close()


def ajaxGetSpaceHits(items):
        # 记录日志
        row = {}
        row['doctorId'] = items['doctorId']
        row['spaceId'] = items['spaceId']
        total_data = request_data(request_url['ajaxGetSpaceHits'].format(doctorId=items['doctorId']), header1())
        total_errorCode = total_data['errorCode']
        if total_errorCode == 0:
            data = total_data['data']
            if data:
                row['total_visits'] = data

        if items['spaceId'] == '0':
            row['zuorizhenghoubaodaohuanzhe'] = 0
            row['weixinzhenhoubaodaohuanzhe'] = 0
            row['zongzhenhoubaodaohuanzhe'] = 0
        else:
            param_data = urllib.parse.urlencode(request_param(spaceId=items['spaceId']))
            huanzhe_data = request_data(request_url['ajaxGetDoctorOtherData'] + param_data, header2())
            huanzhe_errorCode = huanzhe_data['errorCode']
            if huanzhe_errorCode == 0:
                huanzhe_data = huanzhe_data['data']
                row['zuorizhenghoubaodaohuanzhe'] = huanzhe_data[0]
                row['weixinzhenhoubaodaohuanzhe'] = huanzhe_data[1]
                row['zongzhenhoubaodaohuanzhe'] = huanzhe_data[2]
        updateData(row)


def request_data(url, header):
    req = urllib.request.Request(url=url, headers=header,method='GET')
    context = ssl._create_unverified_context()
    with urllib.request.urlopen(req, context=context) as response:
        html = response.read()
        html = html.decode("utf-8")
        data = json.loads(html)
    # req = Request(url=url, headers=header,method='GET')
    # file_content = urlopen(req).read().decode('utf-8')
    #     data = json.loads(file_content)
        return data

def slices(list):
    deal_slices_pool = ThreadPool(8)
    deal_slices_pool.map(ajaxGetSpaceHits, list)
    deal_slices_pool.close()
    deal_slices_pool.join()

#主方法
if __name__ == '__main__':
    # 请求参数
    #查询处理
    list = select()
    list = [list[i:i + 20] for i in range(0, len(list), 20)]
    #ajaxGetSpaceHits(list[0][0])
    pool = ThreadPool(8)
    pool.map(slices, list)
    pool.close()
    pool.join()



