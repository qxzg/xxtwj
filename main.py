from requests import get, post
from bs4 import BeautifulSoup
from time import sleep
from random import randint
from os import system


max_sleep = 30  # 两次请求间隔最长时间，越大耗时越久，但被检测到的风险越小
min_sleep = 10  # 两次请求间隔最短时间

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0',
    'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://i.chaoxing.com/',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'iframe',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-site',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
}
cookies = {}
questionnaire_list = []
fid = ''
uid = ''
home_url = 'https://i.chaoxing.com/base'
questionnaire_list_url = 'https://newes.chaoxing.com/newesReception/ajaxRatedHome'  # 从https://newes.chaoxing.com/newesReception/ratedHome页面获取的
save_questionnaire_url = 'https://newes.chaoxing.com/newesReception/saveQuestionnaire'
questionnaire_remain = 0

def check_cookie():
    req = BeautifulSoup(get(home_url, cookies=cookies, headers=headers).text, features='lxml')
    if req.title.string == '用户登录':
        print("给定的cookie无法登录学习通，请检查")
        exit(2333)
    for name in req.find_all('h3'):
        try:
            a = name['aria-label']
        except KeyError:
            pass
        else:
            print("以 %s 的身份登陆成功。" % name.string)
def raw_cookie_to_dist():
    global cookies, fid, uid
    cookie_list = cookie.split('; ')
    for data in cookie_list:
        data = data.split('=')
        cookies[data[0]] = data[1]
    del cookies['JSESSIONID']  # JSESSIONID仅在i.chaoxing.com中存在
    fid = cookies['fid']
    uid = cookies['_uid']
    check_cookie()

def get_questionnaire_list():
    global questionnaire_list, questionnaire_remain
    req = get(
        questionnaire_list_url + "?uId=%s&fid=%s&questionnaireType=4&courseInfo=&classificationId=&currentPage=1" % (uid, fid),
        cookies=cookies, headers=headers
    ).json()
    page_count = req['pageCount']
    print("正在获取第 1/%s 页的问卷" % page_count)
    for i in range(1, page_count):
    # for i in range(1, 2):
        if i != 1:  # i=1时无需重复请求
            sleep(randint(min_sleep, max_sleep))
            print("正在获取第 %s/%s 页的问卷" % (i, page_count))
            req = get(
                questionnaire_list_url + "?uId=%s&fid=%s&questionnaireType=4&courseInfo=&classificationId=&currentPage=%d" % (uid, fid, i),
                cookies=cookies, headers=headers
            ).json()

        questionnaire_count = req['html'].count('<tr>')
        soup = BeautifulSoup(req['html'], features='lxml').find_all('td')

        n = 0
        for j in range(questionnaire_count):
            questionnaire_data = {}
            n = n + 1
            questionnaire_data['title'] = soup[n].string
            n = n + 2
            questionnaire_data['course'] = soup[n].string
            n = n + 2
            questionnaire_data['teacher'] = soup[n].string
            n = n + 3
            link_data = soup[n]
            n = n + 1
            if link_data.string == "已过期" or link_data.string is None:
                continue
            else:
                questionnaire_remain = questionnaire_remain + 1
                link_info = link_data.a['onclick'][18:-2].split(',')
                questionnaire_data['alreadyId'] = link_info[0]
                questionnaire_data['grantId'] = link_info[1]
                questionnaire_data['questionnaireId'] = link_info[2]
            questionnaire_list.append(questionnaire_data)

def do_questionnaire(questionnaire_data: dict):
    payload = \
    "uId=%s&fid=%s&questionnaireId=%s&alreadyId=%s&grantId=%s" % (uid, fid, questionnaire_data['questionnaireId'], questionnaire_data['alreadyId'], questionnaire_data['grantId']) +\
    "&groupTargetIds=616111&616111_type=1&616111_chooseSetUp=-1&616111=2&groupTargetIds=616112&616112_type=1&\
616112_chooseSetUp=-1&groupTargetIds=616113&616113_type=1&616113_chooseSetUp=-1&groupTargetIds=616114&616114_type=1&\
616114_chooseSetUp=-1&groupTargetIds=616115&616115_type=1&616115_chooseSetUp=-1&groupTargetIds=616116&616116_type=1&\
616116_chooseSetUp=-1&groupTargetIds=616117&616117_type=1&616117_chooseSetUp=-1&groupTargetIds=616118&616118_type=1&\
616118_chooseSetUp=-1&groupTargetIds=616119&616119_type=1&616119_chooseSetUp=-1&groupTargetIds=616120&616120_type=1&\
616120_chooseSetUp=-1&groupTargetIds=616121&616121_type=1&616121_chooseSetUp=-1&groupTargetIds=616122&616122_type=3&\
616122_chooseSetUp=1&616122_fillNum=1&616122_1=0&groupTargetIds=616123&616123_type=3&616123_chooseSetUp=1&\
616123_fillNum=1&616123_1=0&groupTargetIds=616124&616124_type=1&616124_chooseSetUp=-1&616124=1&\
groupTargetIds=616125&616125_type=1&616125_chooseSetUp=-1&616125=1&groupTargetIds=616126&616126_type=1&\
616126_chooseSetUp=-1&616126=2&groupTargetIds=616127&616127_type=1&616127_chooseSetUp=-1&616127=1&\
groupTargetIds=616128&616128_type=1&616128_chooseSetUp=-1&616128=1&groupTargetIds=616129&616129_type=1&\
616129_chooseSetUp=-1&616129=1&groupTargetIds=616130&616130_type=1&616130_chooseSetUp=-1&616130=1&\
groupTargetIds=616131&616131_type=11&616131_chooseSetUp=1&616131=100&groupTargetIds=616132&616132_type=1&\
616132_chooseSetUp=-1&616132=2&groupTargetIds=616133&616133_type=10&616133_chooseSetUp=1&\
groupTargetIds=616134&616134_type=4&616134_chooseSetUp=1&jumpInfo=%7B&616134=%E6%97%A0&saveType=2&submitreasons="
    headers['Content-Type'] = "application/x-www-form-urlencoded; charset=UTF-8"
    req = post(
        save_questionnaire_url,
        cookies=cookies,
        headers=headers,
        data=payload
    )
    if req.status_code != 200:
        print("========================================")
        print("填写问卷时出现错误，请及时反馈给开发人员")
        print(req.text)
        print(req.status_code)
        print(questionnaire_data)
        print("========================================")
    else:
        print("%s/%s 问卷已填写完成" % (n, questionnaire_remain))
    sleep(randint(min_sleep, max_sleep))


# cookie默认使用firefox开发者工具中“网路”里请求头中的Cookie格式。即为"key1=value1; key2=value2"
cookie = input("请在浏览器中登录i.chaoxing.com，然后单击F12，选择“网络”，然后刷新页面，选择base?开头的第一个请求，点击该请求，并在弹出的对话框的“请求头”一栏下找到Cookie: ，右键选择“复制值”，然后粘贴到这里，单击回车\n")
system("cls")
raw_cookie_to_dist()
get_questionnaire_list()
if questionnaire_remain == 0:
    print("你都填完了啊，没我什么事了，我走了")
    exit()
print("您还有%d个问卷未填（已排除已过期的问卷），请按回车键确认：" % questionnaire_remain)
n = 1
for questionnaire in questionnaire_list:
    print("%d. %s - %s - %s" % (n, questionnaire['title'], questionnaire['course'], questionnaire['teacher']))
    n = n + 1
n = 1
input("")
for questionnaire in questionnaire_list:
    if questionnaire['title'] != '课堂教学状态反馈表':
        print("本脚本目前仅支持“课堂教学状态反馈表”的填写，其他反馈表暂时无法填写（懒qwq），自动跳过")
        continue
    do_questionnaire(questionnaire)
    n = n + 1
print("全部问卷填写完成！")
input("按任意键退出程序")
