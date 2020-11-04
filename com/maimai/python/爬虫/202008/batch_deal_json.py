import csv,os,json
from multiprocessing.dummy import Pool as ThreadPool


json_path = 'E:\BaiduNetdiskDownload\outputs\outputs'


headers = [
    'name',
    'title',
    'educate_title',
    'hospitals1',
    'hospitals2',
    'expertise',
    'brief',
    'statA_hot',
    'statA_satisfy',
    'statA_inquires',
    'statB_efficacy',
    'statB_attitude',
    # 总访问
    'statC_Total_visits',
    # 昨日访问
    'statC_zuorifangwen'  ,
    #随访患者数
    'statC_suifanghuanzheshu',
    # 总文章
    'statC_zongwenzhang',
    # 总患者,
    'statC_zonghuanzhe',
    # 昨日诊后报到患者
    'statC_zuorizhenghoubaodaohuanzhe',
    # 微信诊后报到患者,
    'statC_weixinzhenhoubaodaohuanzhe',
    # 总诊后报到患者,
    'statC_zongzhenhoubaodaohuanzhe',
    # 患者投票
    'statC_huanzhetoupiao',
    # 感谢信,
    'statC_ganxiexin',
    # 心意礼物,
    'statC_xinyiliwu',
    # 上次在线
    'statC_shangcizaixian',
    # 开通时间
    'statC_kaitongshijian',
    # 是否存在
    'statC_is_exist',
    'file_name',
    'doctorId',
    'spaceId',
    'todayTime',
    'allConsultCnt',
    'departmentName',
    'statD_zhenhoufuwuxing',
    'statD_zhenzhihouhuanzheshu',
    'statD_suifanghuanzheshu'
]



def file_path():
     return os.listdir(json_path)




def deal_item_json(data):
    each = {}
    each['name'] = data['name']
    each['title'] = data['title']
    if 'educate_title' in data:
        each['educate_title'] = data['educate_title']
    hospital = data['hospitals']
    if len(hospital) == 1:
        each['hospitals1'] = hospital[0]
    elif len(hospital) == 2:
        each['hospitals1'] = hospital[0]
        each['hospitals2'] = hospital[1]
    if 'expertise' in data:
        each['expertise'] = data['expertise']
    if 'brief' in data:
        each['brief'] = data['brief']
    if 'statA' in data:
        statA = data['statA']
        if hasattr(statA, 'hot'):
            each['statA_hot'] = statA['hot']
        elif hasattr(statA, 'satisfy'):
            each['statA_satisfy'] = statA['satisfy']
        elif hasattr(statA, 'inquires'):
            each['statA_inquires'] = statA['inquires']
    if 'statB' in data:
        statB = data['statB']
        if 'efficacy' in statB:
            each['statB_efficacy'] = statB['efficacy']
        elif statB in statB:
            each['statB_attitude'] = statB['attitude']
    if 'statC' in data:
        statC = data['statC']
        if 'key' in statC:
            for item in statC:
                if item['key'] == '总访问':
                    each['statC_Total_visits'] = item['value']
                if item['key'] == '昨日访问':
                    each['statC_zuorifangwen'] = item['value']
                if item['key'] == '随访患者数':
                    each['statC_suifanghuanzheshu'] = item['value']
                if item['key'] == '总文章':
                    each['statC_zongwenzhang'] = item['value']
                if item['key'] == '总患者':
                    each['statC_zonghuanzhe'] = item['value']
                if item['key'] == '昨日诊后报到患者':
                    each['statC_zuorizhenghoubaodaohuanzhe'] = item['value']
                if item['key'] == '微信诊后报到患者':
                    each['statC_weixinzhenhoubaodaohuanzhe'] = item['value']
                if item['key'] == '总诊后报到患者':
                    each['statC_zongzhenhoubaodaohuanzhe'] = item['value']
                if item['key'] == '患者投票':
                    each['statC_huanzhetoupiao'] = item['value']
                if item['key'] == '感谢信':
                    each['statC_ganxiexin'] = item['value']
                if item['key'] == '心意礼物':
                    each['statC_xinyiliwu'] = item['value']
                if item['key'] == '上次在线':
                    each['statC_shangcizaixian'] = item['value']
                if item['key'] == '开通时间':
                    each['statC_kaitongshijian'] = item['value']
            each['statC_is_exist'] = 1
        else:
            each['statC_is_exist'] = 0
    meta = data['meta']
    if 'doctorId' in meta:
        each['doctorId'] = meta['doctorId']
    if 'spaceId' in meta:
        each['spaceId'] = meta['spaceId']
    if 'todayTime' in meta:
        each['todayTime'] = meta['todayTime']
    if 'allConsultCnt' in meta:
        each['allConsultCnt'] = meta['allConsultCnt']
    print(each)



def deal_small_list(small_list):
    for small_list_item in small_list:
        pool = ThreadPool(8)
        deal_json_data(small_list_item)
        pool.close()
        pool.join()



def deal_json_data(list):
    for item_path in list:
        print(item_path)
        with open(r'E:\BaiduNetdiskDownload\outputs\outputs\\' + item_path, 'r', encoding='utf-8') as fp:
            each = {}
            each['file_name'] = item_path
            data = json.load(fp)
            each['name'] = data['name']
            each['departmentName'] = item_path.split("_")[0]
            each['title'] = data['title']
            if 'educate_title' in data:
                each['educate_title'] = data['educate_title']
            hospital = data['hospitals']
            if len(hospital) == 1:
                each['hospitals1'] = hospital[0]
            elif len(hospital) == 2:
                each['hospitals1'] = hospital[0]
                each['hospitals2'] = hospital[1]
            if 'expertise' in data:
                each['expertise'] = data['expertise']
            if 'brief' in data:
                each['brief'] = data['brief']
            if 'statA' in data:
                statA = data['statA']
                if 'hot' in statA:
                    each['statA_hot'] = statA['hot']
                if 'satisfy' in statA:
                    each['statA_satisfy'] = statA['satisfy']
                if 'inquires' in statA:
                    each['statA_inquires'] = statA['inquires']
            if 'statB' in data:
                statB = data['statB']
                if 'efficacy' in statB:
                    each['statB_efficacy'] = statB['efficacy']
                if 'attitude' in statB:
                    each['statB_attitude'] = statB['attitude']
            if 'statC' in data:
                statC = data['statC']
                if 'key' in statC:
                    for item in statC:
                        if item['key'] == '总访问':
                            each['statC_Total_visits'] = item['value']
                        if item['key'] == '昨日访问':
                            each['statC_zuorifangwen'] = item['value']
                        if item['key'] == '随访患者数':
                            each['statC_suifanghuanzheshu'] = item['value']
                        if item['key'] == '总文章':
                            each['statC_zongwenzhang'] = item['value']
                        if item['key'] == '总患者':
                            each['statC_zonghuanzhe'] = item['value']
                        if item['key'] == '昨日诊后报到患者':
                            each['statC_zuorizhenghoubaodaohuanzhe'] = item['value']
                        if item['key'] == '微信诊后报到患者':
                            each['statC_weixinzhenhoubaodaohuanzhe'] = item['value']
                        if item['key'] == '总诊后报到患者':
                            each['statC_zongzhenhoubaodaohuanzhe'] = item['value']
                        if item['key'] == '患者投票':
                            each['statC_huanzhetoupiao'] = item['value']
                        if item['key'] == '感谢信':
                            each['statC_ganxiexin'] = item['value']
                        if item['key'] == '心意礼物':
                            each['statC_xinyiliwu'] = item['value']
                        if item['key'] == '上次在线':
                            each['statC_shangcizaixian'] = item['value']
                        if item['key'] == '开通时间':
                            each['statC_kaitongshijian'] = item['value']
                    each['statC_is_exist'] = 1
                else:
                    each['statC_is_exist'] = 0
            meta = data['meta']
            if 'doctorId' in meta:
                each['doctorId'] = meta['doctorId']
            if 'spaceId' in meta:
                each['spaceId'] = meta['spaceId']
            if 'todayTime' in meta:
                each['todayTime'] = meta['todayTime']
            if 'allConsultCnt' in meta:
                each['allConsultCnt'] = meta['allConsultCnt']
            statD = data['statD']
            if statD:
                for item in statD:
                    if item['key'] == '诊后服务星':
                        each['statD_zhenhoufuwuxing'] = item['value']
                    if item['key'] == '诊治后的患者数':
                        each['statD_zhenzhihouhuanzheshu'] = item['value']
                    if item['key'] == '随访中的患者数':
                        each['statD_suifanghuanzheshu'] = item['value']

            downloadDoctor(each)


def downloadDoctor(each):
    writer.writerow(each)

if __name__=='__main__':
    f = open(r'D:\study\python-test\file\csv\20201102-004-haodaifu.csv', 'w+', newline='', encoding='utf-8-sig')
    writer = csv.DictWriter(f, headers)
    writer.writeheader()
    file_path_list = file_path()
    deal_small_list_data = [file_path_list[i:i + 1000] for i in range(0, len(file_path_list), 1000)]

    pool = ThreadPool(16)
    deal_small_list(deal_small_list_data)
    pool.close()
    pool.join()
    f.close()