import requests
from lxml import etree
import htmlparser
import multiprocessing
import time
import json
from save_data import lagou_mysql
class Spider(object):
    def __init__(self):
        self.lagou_craw=requests.session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}
        self.city_list=""

    def handle_city(self):
        city_url='https://www.lagou.com/jobs/allCity.html'
        city_result=self.handle_requets(method="GET",url=city_url)
        xapth_html=etree.HTML(city_result)
        citys= xapth_html.xpath('''//ul[@class="city_list"]//a''')
        self.city_list=[city.text for city in citys]
        self.lagou_craw.cookies.clear()


    def handle_city_job(self,city):
        first_requets_url='https://www.lagou.com/jobs/list_python?&px=default&city=%s'%city
        first_response=self.handle_requets(method="GET",url=first_requets_url)
        first_html=htmlparser.Parser(first_response)
        try:
            page=first_html.xpath('''//div[@class="page-number"]/span[last()]''').text()
        except:
            return
        else:
            for i in range(1,int(page)+1):
                print(i)
                data = {
                    "pn": i,
                    "kd": "python"
                }

                post_url='https://www.lagou.com/jobs/positionAjax.json?px=default&city=%s&needAddtionalResult=false'%city
                refer_url='https://www.lagou.com/jobs/list_python?&px=default&city=%s'%city
                self.headers['Referer']=refer_url.encode()
                post_response=self.handle_requets(method='POST',url=post_url,data=data,info=city)
                datas=json.loads(post_response)
                job_list=datas["content"]["positionResult"]["result"]
                for job in job_list:
                    lagou_mysql.insert_item(job)

    def get_proxy(self):
        return requests.get("代理").json()

    def delete_proxy(self,proxy):
        requests.get("代理")
    def handle_requets(self,method,url,data=None,info=None):

        while True:
            retry_count = 5
            proxy = self.get_proxy().get("proxy")
            while retry_count > 0:
                try:
                    if method == "GET":
                        response=self.lagou_craw.get(url,headers=self.headers,proxies={"http": "http://{}".format(proxy)},timeout=10)
                    elif method =="POST":
                        response = self.lagou_craw.post(url, headers=self.headers,proxies={"http": "http://{}".format(proxy)},data=data,timeout=10)
                    response.encoding = 'utf-8'
                    if "频繁" in response.text:
                        self.lagou_craw.cookies.clear()#清楚cookie
                        first_requets_url = 'https://www.lagou.com/jobs/list_python?&px=default&city=%s'%info
                        self.handle_requets(method="GET", url=first_requets_url)
                        time.sleep(10)
                        continue
                    else:
                        pass
                    return response.text
                except Exception:
                    retry_count -= 1
                    self.lagou_craw.cookies.clear()  # 清楚cookie
                    first_requets_url = 'https://www.lagou.com/jobs/list_python?&px=default&city=%s' % info
                    self.handle_requets(method="GET", url=first_requets_url)
                    time.sleep(10)
                    continue
                    # 出错5次, 删除代理池中代理
            self.delete_proxy(proxy)



if __name__ == '__main__':

    spider=Spider()

    spider.handle_city()
    pool = multiprocessing.Pool(2)#多进程
    for city in spider.city_list:
        pool.apply_async(spider.handle_city_job,args=(city,))
    pool.close()
    pool.join()
