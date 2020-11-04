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
sql = "select * from t_hdf_doctor_list_20201102 where is_deal = 0"


request_url = {
    # {"errorCode":0,"msg":"","data":{"isOpenFollowup":0,"yesterdayCnt":3098,"patientSigninCnt":0,"spaceRepliedCount":7291,"doctorVoteCnt":"1123","thankLetterCount":"554","spaceActiveDate":"今天","openSpaceTime":"2010-08-10 20:45","yesterdayDate":1604210325}}
    "ajaxGetDoctorData":"https://renxianguo.haodf.com/ndoctor/ajaxGetDoctorData?spaceId={spaceId}",
    # {"errorCode":0,"msg":"","data":3969376}
    "ajaxGetSpaceHits":"https://renxianguo.haodf.com/ndoctor/ajaxGetSpaceHits?doctorId={doctorId}",
    # {"errorCode":0,"msg":"","data":[0,2627,2677]} 昨日诊后报到患者  微信诊后报到患者  总诊后报到患者
    "ajaxGetDoctorOtherData":"https://renxianguo.haodf.com/ndoctor/ajaxGetDoctorOtherData?startTime=2020-11-01 00:00:00&endTime=2020-11-01 23:59:59&spaceId={spaceId}"
}

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



def header() :
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
        'If-None-Match': 'W/"ff-iIFLjkk1emJikoxUVLRlUQ"'
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
#"yesterdayCnt": 3098,
#"spaceRepliedCount": 7291,
#"doctorVoteCnt": "1123",
#"thankLetterCount": "554",
#"spaceActiveDate": "今天",
#"openSpaceTime": "2010-08-10 20:45",
#"yesterdayDate": 1604210325
def updateData(each):
    sdb2 = db()
    cursor = sdb2.cursor()
    print(each)
    try:
        # 像sql语句传递参数
        sql_update = '''
                update t_hdf_doctor_list_20201102 
                set yesterdayCnt = '{yesterdayCnt}',
                spaceRepliedCount='{spaceRepliedCount}', 
                doctorVoteCnt ='{doctorVoteCnt}',
                thankLetterCount ='{thankLetterCount}',
                spaceActiveDate ='{spaceActiveDate}',
                openSpaceTime ='{openSpaceTime}',
                is_deal = 1
                where spaceId = {spaceId} and doctorId = {doctorId}
                '''
        sql_update1 = sql_update.format(yesterdayCnt=each['yesterdayCnt'],
                                        spaceRepliedCount=each['spaceRepliedCount'],
                                        doctorVoteCnt=each['doctorVoteCnt'],
                                        thankLetterCount=each['thankLetterCount'],
                                        spaceActiveDate=each['spaceActiveDate'],
                                        openSpaceTime=each['openSpaceTime'],
                                        spaceId=each['spaceId'],
                                        doctorId=each['doctorId']
                                        )
        cursor.execute(sql_update1)
        # 提交
        sdb2.commit()
    except Exception as e:
        # 错误回滚
        print(e)
        sdb2.rollback()
    finally:
        sdb2.close()


#     # {"errorCode":0,"msg":"","data":{"isOpenFollowup":0,"yesterdayCnt":3098,"patientSigninCnt":0,"spaceRepliedCount":7291,"doctorVoteCnt":"1123","thankLetterCount":"554","spaceActiveDate":"今天","openSpaceTime":"2010-08-10 20:45","yesterdayDate":1604210325}}
def requestAjaxGetDoctorData(items):
        req = Request(url=request_url['ajaxGetDoctorData'].format(spaceId=items['spaceId']), headers=header(), method='GET')
        file_content = urlopen(req).read().decode('utf-8')
        data = json.loads(file_content)
        # 记录日志
        errorCode = data['errorCode']
        if errorCode == 0:
            data = data['data']
            row = {}
            if data:
                row['yesterdayCnt'] = data['yesterdayCnt']
                row['spaceRepliedCount'] = data['spaceRepliedCount']
                row['doctorVoteCnt'] = data['doctorVoteCnt']
                row['thankLetterCount'] = data['thankLetterCount']
                row['spaceActiveDate'] = data['spaceActiveDate']
                row['spaceActiveDate'] = data['spaceActiveDate']
                row['openSpaceTime'] = data['openSpaceTime']
                row['doctorId'] = items['doctorId']
                row['spaceId'] = items['spaceId']
                # 更新
                updateData(row)


#主方法
if __name__ == '__main__':
    # 请求参数
    #查询处理
    list = select()
    pool = ThreadPool(8)
    pool.map(requestAjaxGetDoctorData, list)
    pool.close()
    pool.join()



