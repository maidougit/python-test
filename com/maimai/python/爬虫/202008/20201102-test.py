#-*- coding:utf8 -*-
import json,re


test = {
  "name": "潘家华",
  "title": "主任医师",
  "educate_title": "教授",
  "hospitals": [
    "中国科学技术大学附属第一医院(安徽省立医院)",
    "安徽省肿瘤医院"
  ],
  "expertise": "小儿呼吸系统疾病（哮喘、感染、结核病）、危重症、神经疾病及新生儿疾病的诊疗",
  "brief": "潘家华，中国科学技术大学附属第一医院（安徽省立医院）儿科主任，主任医师、教授、博士生导师。从事儿科医、教、研工作33年。先后任中华医学会儿科分会委员、围产医学委员、新生儿学组委员、安徽医学会理事、安徽省儿科学会主任委员。安徽省学术与技术带头人，安徽省江淮名医，安徽省优秀科技工作者，安徽省先进工作者。临床医疗技术过硬，诊疗思维综合能力强，对新生儿疾病、小儿呼吸系统疾病、小儿危重症、小儿感染性疾病的诊疗有丰富的经验，在国内享有较高声誉。主持多项科研课题，三次荣获安徽省科技奖三等奖，发表医学论文200余篇，主编著作5部。",
  "statA": {
    "hot": "5.0",
    "satisfy": "100%",
    "inquires": "11711"
  },
  "statB": {
    "efficacy": "99%",
    "attitude": "99%"
  },
  "statC": [
    {
      "key": "总访问",
      "value": "0次"
    },
    {
      "key": "昨日访问",
      "value": "0次(20-09-26)"
    },
    {
      "key": "随访患者数",
      "value": "0位"
    },
    {
      "key": "总文章",
      "value": "0篇"
    },
    {
      "key": "总患者",
      "value": "0位"
    },
    {
      "key": "昨日诊后报到患者",
      "value": "0位"
    },
    {
      "key": "微信诊后报到患者",
      "value": "0位"
    },
    {
      "key": "总诊后报到患者",
      "value": "0位"
    },
    {
      "key": "患者投票",
      "value": "0票"
    },
    {
      "key": "感谢信",
      "value": "0封"
    },
    {
      "key": "心意礼物",
      "value": "0个"
    },
    {
      "key": "上次在线",
      "value": "今天"
    },
    {
      "key": "开通时间",
      "value": "2020-01-01 00:00"
    }
  ],
  "statD": [
    {
      "key": "诊后服务星",
      "value": ""
    },
    {
      "key": "诊治后的患者数",
      "value": "9994例"
    },
    {
      "key": "随访中的患者数",
      "value": "6450例"
    }
  ]
}


def deal_item_json(data, file_name):
  each = {}
  file_name = file_name.split("_")[0]
  each['departmentName'] = file_name
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
    statD = data['statD']
    if statD:
      for item in statD:
        if item['key'] == '诊后服务星':
          each['statD_zhenhoufuwuxing'] = item['value']
        if item['key'] == '诊治后的患者数':
          each['statD_zhenzhihouhuanzheshu'] = item['value']
        if item['key'] == '随访中的患者数':
          each['statD_suifanghuanzheshu'] = item['value']
  print(json.dumps(each))




if __name__ == '__main__':
  # if 'name' in test:
  #   print("有")
  # else:
  #   print('没有')
  #
  # if hasattr(test, 'name'):
  #   print("有")
  # else:
  #   print('没有')
  deal_item_json(test, "儿科__111")
