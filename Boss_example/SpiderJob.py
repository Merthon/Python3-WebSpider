from DrissionPage import ChromiumPage
import csv

f = open('SpiderJob_data.csv',mode='w',encoding='utf-8',newline='')
#字典写入方法
csv_writer = csv.DictWriter(f, fieldnames=[
    '职位',
    '区域',
    '街道',
    '公司',
    '薪资',
    '经验', 
    '学历', 
    '技能要求', 
    '福利'
])
#写入表头
csv_writer.writeheader()

dp = ChromiumPage()
dp.listen.start('wapi/zpgeek/search/joblist.json')
dp.get('https://www.zhipin.com/web/geek/job?query=%E7%88%AC%E8%99%AB&city=101030100')

for page in range(1,4):
    #下滑页面
    dp.scroll.to_bottom()
    print(f'正在采集第{page}内容')
    #等待数据包加载
    resp = dp.listen.wait()
    #获取响应数据
    json_data = resp.response.body
    '''解析数据'''
    #提取职位信息所在列表
    jobList = json_data['zpData']['jobList']
    # for
    for index in jobList:
    # 提取相关数据，保存到字典里
     dit = {
        '职位': index['jobName'],
        '区域': index['areaDistrict'],
        '街道': index['businessDistrict'],
        '公司': index['brandName'],
        '薪资': index['salaryDesc'],
        '经验': index['jobExperience'],
        '学历': index['jobDegree'],
        '技能要求': ' '.join(index['skills']),
        '福利': ' '.join(index['welfareList']),
    }
    #写入数据
    csv_writer.writerow(dit)
    print(dit)
    # 点击下一页（元素定位）
    #<i class="ui-icon-arrow-right"></i>
    dp.ele('css:.ui-icon-arrow-right').click()
