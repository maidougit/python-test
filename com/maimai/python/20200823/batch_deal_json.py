import csv,os,json
from multiprocessing.dummy import Pool as ThreadPool


json_path = 'G:\pdf\df.json\outputs'


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
    'statC_kaitongshijian'
]



def file_path():
     return os.listdir(json_path)

def deal_json_data(list):
    for item_path in list:
        print(item_path)
        with open(r'G:\pdf\df.json\outputs\\' + item_path, 'r', encoding='utf-8') as fp:
            each = {}
            data = json.load(fp)
            print(data)
            each['name'] = data['name']
            each['title'] = data['title']
            if hasattr(data, 'educate_title'):
                each['educate_title'] = data['educate_title']
            hospital = data['hospitals']
            if len(hospital) == 1:
                each['hospitals1'] = hospital[0]
            elif len(hospital) == 2:
                each['hospitals1'] = hospital[0]
                each['hospitals2'] = hospital[1]
            if hasattr(data, 'expertise'):
              each['expertise'] = data['expertise']
            if hasattr(data, 'brief'):
             each['brief'] = data['brief']
            if hasattr(data, 'statA'):
                statA = data['statA']
                if hasattr(statA, 'hot'):
                    each['statA_hot'] = statA['hot']
                elif hasattr(statA, 'satisfy'):
                    each['statA_satisfy'] = statA['satisfy']
                elif hasattr(statA, 'inquires'):
                    each['statA_inquires'] = statA['inquires']
            if hasattr(data, 'statB'):
                statB = data['statB']
                if hasattr(statB, 'efficacy'):
                    each['statB_efficacy'] = statA['efficacy']
                elif hasattr(statB, 'attitude'):
                    each['statB_attitude'] = statA['attitude']
            if hasattr(data, 'statC'):
                statC = data['statC']
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
            downloadDoctor(each)


def downloadDoctor(each):
    writer.writerow(each)

if __name__=='__main__':
    f = open(r'F:\python-test\file\csv\20201101-haodaifu.csv', 'w+', newline='', encoding='utf-8-sig')
    writer = csv.DictWriter(f, headers)
    writer.writeheader()
    file_path_list = file_path()
    pool = ThreadPool(8)
    deal_json_data(file_path_list)
    pool.close()
    pool.join()
    f.close()