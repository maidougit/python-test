# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FirstScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class DataFangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    subarea = scrapy.Field()  # һ������
    area = scrapy.Field()  # ��ǰ����
    housecoord = scrapy.Field()  # ¥������
    housename = scrapy.Field()  # housename
    housename2 = scrapy.Field()  # ����
    houseproperty = scrapy.Field()  # ¥�̱�ǩ
    _id = scrapy.Field()  # ¥��url
    source = scrapy.Field()  # ��Դ
    allstatus = scrapy.Field()  # �ɼ�״̬
    houseprice = scrapy.Field()  # ����
    houseatr = scrapy.Field()  # ��ҵ���
    housetype = scrapy.Field()  # �������
    years = scrapy.Field()  # ��Ȩ����
    decoration = scrapy.Field()  # װ��״��
    developer = scrapy.Field()  # ������
    houseaddress = scrapy.Field()  # ¥�̵�ַ
    salestatus = scrapy.Field()  # ����״̬
    startSaleString = scrapy.Field()  # ����ʱ��
    endSaleString = scrapy.Field()  # ����ʱ��
    saleaddress = scrapy.Field()  # ��¥��ַ
    landarea = scrapy.Field()  # ռ�����
    housearea = scrapy.Field()  # �������
    plotratio = scrapy.Field()  # �ݻ���
    greenrate = scrapy.Field()  # �̻���
    carsite = scrapy.Field()  # ͣ��λ
    housecount = scrapy.Field()  # ¥������
    allcount = scrapy.Field()  # �ܻ���
    managecompany = scrapy.Field()  # ��ҵ��˾
    managefee = scrapy.Field()  # ��ҵ��
    floorCondition = scrapy.Field()  # ¥��״��
    fetch_time = scrapy.Field()  # �ɼ�ʱ��
    insoect = scrapy.Field()  # �ɼ�״̬

    startsaletime = scrapy.Field()  # ¥������
    endsaletime = scrapy.Field()  # ¥������


class DataDynamicJson(scrapy.Item):
    dynamicJson = scrapy.Field()  # ¥�̶�̬
    soutse = scrapy.Field()  # ¥�̶�̬
    title = scrapy.Field()  # ¥�̶�̬
    content = scrapy.Field()  # ¥�̶�̬
    publishDate = scrapy.Field()  # ¥�̶�̬
    _id = scrapy.Field()  # ¥�̶�̬


class DataDynamicJson1(scrapy.Item):
    dynamicJson = scrapy.Field()
    _id = scrapy.Field()


class DataCommentJson(scrapy.Item):
    commentJson = scrapy.Field()  # ¥������
    sourceUrl = scrapy.Field()  # ¥������
    source = scrapy.Field()  # ¥������
    content = scrapy.Field()  # ¥������
    createDate = scrapy.Field()  # ¥������
    userNick = scrapy.Field()  # ¥������
    _id = scrapy.Field()  # ¥������


class DataHouseapartment(scrapy.Item):
    houseapartment = scrapy.Field()  # ����json
    houseUrl = scrapy.Field()  # ����json
    name = scrapy.Field()  # ����json
    salesStatus = scrapy.Field()  # ����json
    roomNum = scrapy.Field()  # ����json
    hallNum = scrapy.Field()  # ����json
    toiletNum = scrapy.Field()  # ����json
    constructSpace = scrapy.Field()  # ����json
    price = scrapy.Field()  # ����json
    propertyType = scrapy.Field()  # ����json
    remark = scrapy.Field()  # ����json
    imgs = scrapy.Field()  # ����json
    totalPrices = scrapy.Field()  # ����json
    _id = scrapy.Field()  # ����json


class DataPicJson(scrapy.Item):
    picJson = scrapy.Field()
    picUrl = scrapy.Field()
    _id = scrapy.Field()
    type = scrapy.Field()


class Image(scrapy.Item):
    _id = scrapy.Field()  # url
    content = scrapy.Field()  # img
    fileSaveFlag = scrapy.Field()  # �Ƿ����سɹ�
    file_source = scrapy.Field()  # ��Դ


class ImageItem(scrapy.Item):
    _id = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()


class QiubaiProjItem(scrapy.Item):
    # define the fields for your item here like:
    # ����ͷ������
    image_url = scrapy.Field()
    # ��������
    name = scrapy.Field()
    # ��������
    age = scrapy.Field()
    # ��������
    content = scrapy.Field()
    # ��Ц�ĸ���
    haha_count = scrapy.Field()


class WeiyiItem(scrapy.Item):
    id = scrapy.Field()
    tlDoctorName = scrapy.Field()
    provinceName = scrapy.Field()
    teamDoctorActivityList = scrapy.Field()
    tlExpertPhoto = scrapy.Field()
    tlExpertUuid = scrapy.Field()
    totalConsultCount = scrapy.Field()
    totalOrderCount = scrapy.Field()
    provinceId = scrapy.Field()
    plusDemand = scrapy.Field()
    photo = scrapy.Field()
    name = scrapy.Field()
    link = scrapy.Field()
    isPlus = scrapy.Field()
    introduction = scrapy.Field()
    hospitalNameList = scrapy.Field()
    expertIdList = scrapy.Field()
    expertCount = scrapy.Field()
    diseaseMap = scrapy.Field()
    diseaseList = scrapy.Field()
    consultStarExpert = scrapy.Field()
    cityName = scrapy.Field()
    cityId = scrapy.Field()
    chatId = scrapy.Field()
    activityId = scrapy.Field()
    departmantName = scrapy.Field()
