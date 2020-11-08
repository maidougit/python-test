# -*- coding:utf-8 -*-
import requests, json, csv
from urllib.request import Request, urlopen
from urllib import parse
from multiprocessing.dummy import Pool as ThreadPool

url = "https://mobile-api.haodf.com/patientapi/hospital_getDoctorListByFaculty?ck=2CA41DD4-E37B-4D43-88E5-4B565650591A-i687"

payload = 'hdfSignature=c776d9c3209225682f512b29c0541f43&app=haodf&b=108&cid=0&ck=2F5B358F-2D83-4C8C-B81F-B7CEBB4D99FE-i687&deviceOpenUDID=EA151ECB-CB3D-4902-A45A-E9C2EF887BFA&di=EA151ECB-CB3D-4902-A45A-E9C2EF887BFA&dt=b32d590da8e7d3d47a42b5e88b27c76a766995d939037b5bf742afeea0fc5c21&facultyId=6001000&hdfhs=36f96093b8f5f52d5868ba0f24f2d0be&hdfts=1603436578&hospitalFacultyId=&m=iPhone10%2C1&n=2&os=ios&p=0&pageId=1&pageSize=10&provinceArr=%u5168%u56FD%2C&s=APPL&sv=13.6.1&v=6.8.7'

csvheaders = ["doctorId", "name", "fullGrade", "specialize", "isCaseOpened", "isPhoneOpened", "isBookingOpened",
              "isOpenConsultation", "isOpenRegistration", "hospitalName", "hospitalFacultyName",
              "hospitalFacultyFullName", "logoUrl", "spaceId", "onLineTime", "goodVoteCount", "medalHonorUrl",
              "casePostCount2Week", "isServiceStar", "isPhoneOnline", "voteCnt", "voteCntIn2Years",
              "recommendIndex", "recommendStatus", "status4RankShow", "rankType", "effect", "attitude",
              "isOpenClinic", "replyRate24H", "replyTips", "replyValue", "isShowSurgeryAppointment",
              "isShowAppointmentTag"]


def requestData(facultyId, pageId=1):
    data = {
        "_hdfSignature": "c776d9c3209225682f512b29c0541f43",
        "app": "haodf",
        "b": "108",
        "cid": "0",
        "ck": "2F5B358F-2D83-4C8C-B81F-B7CEBB4D99FE-i687",
        "deviceOpenUDID": "EA151ECB-CB3D-4902-A45A-E9C2EF887BFA",
        "di": "EA151ECB-CB3D-4902-A45A-E9C2EF887BFA",
        "dt": "b32d590da8e7d3d47a42b5e88b27c76a766995d939037b5bf742afeea0fc5c21",
        "facultyId": facultyId,
        "hdfhs": "36f96093b8f5f52d5868ba0f24f2d0be",
        "hdfts": "1603436578",
        "hospitalFacultyId:"
        "m": "iPhone10,1",
        "n": 2,
        "os": "ios",
        "p": "0",
        "pageId": pageId,
        "pageSize": 10,
        "provinceArr": "全国",
        "s": "APPL",
        "sv": "13.6.1",
        "v": "6.8.7"
    }
    return data


headers = {
    'Host': 'mobile-api.haodf.com',
    'Cookie': 'g=HDF.54.5f927ec36ee48; loginos=IOS; __jsluid_s=4d397cb978d3b4c818c2363cb0366397',
    'Accept': '*/*',
    'Accept-Language': 'zh-Hans-CN;q=1',
    'Content-Type': 'application/x-www-form-urlencoded'
}


def request(facultyId):
    data = parse.urlencode(requestData(facultyId, 1))
    response = requests.request("POST", url, headers=headers, data=data)
    print(response.text)
    data = json.loads(response.text.encode('utf8'))
    total = data['pageInfo']['recordCount']
    pageNums = calculationPage(total)
    listPage = range(1, pageNums + 1)
    lisPartam = []
    for each in listPage:
        row = {}
        row["pageNum"] = each
        row["facultyId"] = facultyId
        lisPartam.append(row)
    pool = ThreadPool(4)
    dealresults = pool.map(requestData1, lisPartam)
    pool.close()
    pool.join()


def requestData1(row):
    data = parse.urlencode(requestData(row["facultyId"], row["pageNum"]))
    response = requests.request("POST", url, headers=headers, data=data)
    data = json.loads(response.text.encode('utf8'))
    print(data)
    if data['content'] and data["content"]["doctorList"]:
       data = data["content"]["doctorList"]
       dealEachData(data)

# 处理数据
def dealEachData(data):
    for each in data:
        row = {}
        row["doctorId"] = each["doctorId"]
        row["name"] = each["name"]
        row["fullGrade"] = each["fullGrade"]
        row["specialize"] = each["specialize"]
        row["isCaseOpened"] = each["isCaseOpened"]
        row["isPhoneOpened"] = each["isPhoneOpened"]
        row["isBookingOpened"] = each["isBookingOpened"]
        row["isOpenConsultation"] = each["isOpenConsultation"]
        row["isOpenRegistration"] = each["isOpenRegistration"]
        row["hospitalName"] = each["hospitalName"]
        row["hospitalFacultyName"] = each["hospitalFacultyName"]
        row["hospitalFacultyFullName"] = each["hospitalFacultyFullName"]
        row["logoUrl"] = each["logoUrl"]
        row["spaceId"] = each["spaceId"]
        row["onLineTime"] = each["onLineTime"]
        row["goodVoteCount"] = each["goodVoteCount"]
        row["medalHonorUrl"] = each["medalHonorUrl"]
        row["casePostCount2Week"] = each["casePostCount2Week"]
        row["isServiceStar"] = each["isServiceStar"]
        row["isPhoneOnline"] = each["isPhoneOnline"]
        row["voteCnt"] = each["voteCnt"]
        row["voteCntIn2Years"] = each["voteCntIn2Years"]
        row["recommendIndex"] = each["recommendIndex"]
        row["recommendStatus"] = each["recommendStatus"]
        row["status4RankShow"] = each["status4RankShow"]
        row["rankType"] = each["rankType"]
        row["effect"] = each["effect"]
        row["attitude"] = each["attitude"]
        row["isOpenClinic"] = each["isOpenClinic"]
        row["replyRate24H"] = each["replyRate24H"]
        row["replyTips"] = each["replyTips"]
        row["replyValue"] = each["replyValue"]
        row["isShowSurgeryAppointment"] = each["isShowSurgeryAppointment"]
        row["isShowAppointmentTag"] = each["isShowAppointmentTag"]
        downloadWeimai(row)


def downloadWeimai(each):
    print(each)
    writer.writerow(each)


# 计算页码
def calculationPage(total, limit=10):
    page = int(total) / limit
    if isinstance(page, int):
        page
    else:
        page = int(page) + 1
    return page


if __name__ == '__main__':
    f = open(r'D:\study\python-test\file\csv\haodaifu-20201023.csv', 'w+', newline='', encoding='utf-8-sig')
    writer = csv.DictWriter(f, csvheaders)
    writer.writeheader()
    list = [
        6001000,
        # 12000000,
        # 3030000,
        # 6002000,
        # 3012000,
        # 10012000,
        # 2004000
    ]
    pool = ThreadPool(4)
    dealresults = pool.map(request, list)
    pool.close()
    pool.join()
    f.close()
