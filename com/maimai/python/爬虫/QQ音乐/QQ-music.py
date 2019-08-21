from selenium import webdriver

driver = webdriver.Chrome()

url = 'https://y.qq.com/portal/search.html#page=1&searchid=1&remoteplace=txt.yqq.top&t=song&w=%E4%BC%A4%E5%BF%83%E5%A4%AA%E5%B9%B3%E6%B4%8B'
driver.get(url)
#智能等待
driver.implicitly_wait(5)
data = driver.file_detector('//*[@id="song_box"]/div[2]/ul[2]/li[1]/div/div[2]/span[1]/a/span[1]/a').get_attribute('href')

print(data)

