import pymongo
import requests
import guba.settings as settings

host = settings.MONGODB_HOST
port = settings.MONGODB_PORT
db_name = settings.MONGODB_DBNAME
col_name = "IP_POOLS"
client = pymongo.MongoClient(host, port)
col = client[db_name][col_name]

def judge_ip(ip, port):
    #判断ip是否可用
    http_url = "http://www.baidu.com"
    
    try:
        proxy_dict = {"http":proxy_url}
        response = requests.get(http_url, proxies=proxy_dict)
    except:
        return False

    code = response.status_code
    if code >= 200 and code < 300:
        return True
    else:
        return False


def get_ips():
	show = col.find({},{"_id":0})
	ips = list(show)
	while(): 
		ip = ips[random.randint(1,100)]
		judge_re = judge_ip(ip["IP"], ip["PORT"])
		if judge_re:
			return "http://{0}:{1}"format(ip["IP"], ip["PORT"])