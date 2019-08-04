from lxml import html
from multiprocessing.dummy import Pool as ThreadPool
import  requests, json, sys,importlib

#于defaultencoding来做转换。
importlib.reload(sys)
#sys.setdefaultencoding('utf-8')

def towrite(contentdict):
    f.writelines(u'回帖时间:' + str(contentdict['topic_play_time']) + '\n')
    f.writelines(u'回帖内容:' + contentdict['topic_play_content'] + '\n')
    f.writelines(u'回帖人:' + contentdict['user_name'] + '\n')


def spider(url) :
    urltext = requests.get(url)
    selector = html.etree.HTML(urltext.text)
    content_field = selector.xpath('//div[@class="l_post j_l_post l_post_bright  "]')
    item = {}
    print(content_field)
    for each in content_field:
        replay_info = json.load(each.xpath('@data-field')[0].replace('&quot',''))
        print(replay_info)
        author = replay_info['author']['user_name']
        content = '黎明'
        replay_time = replay_info['content']['date']
        print(replay_time)
        # item['user_name'] = author
        # item['topic_replay_time'] = replay_time
        # item['topic_replay_content'] = content
        # towrite(item)

if __name__ == '__main__':
    pool = ThreadPool(4)
    f = open('F:\\python-test\\file\\tieba.txt', 'a')
    page = []
    for i in range(1, 2):
        newpage = 'http://tieba.baidu.com/p/6213577912?pn=' + str(i)
        page.append(newpage)

    #print(page)
    results = pool.map(spider ,page)
    pool.close()
    pool.join()
    f.close()