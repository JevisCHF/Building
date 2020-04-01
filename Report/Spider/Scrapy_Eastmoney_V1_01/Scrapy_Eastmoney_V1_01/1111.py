import requests, json

url = 'http://reportapi.eastmoney.com/report/list'

headers = {
    'Host': 'reportapi.eastmoney.com',
    'Referer': 'http://data.eastmoney.com/report/industry.jshtml',
}
parameters = {
    # 'cb': 'datatable2472393',
    # 'industryCode': 728,
    'pageSize': 50,
    'beginTime': '2018-02-25',
    # 'endTime': '2020-02-25',
    'pageNo': 2,
    'qType': 1,

}
req = requests.get(url=url, params=parameters, headers=headers)

print(req.text)
print(req.status_code)
# req.raise_for_status()

# a = eval(req.text[17:-1])
#
# n = 0
# for i in a['data']:
#     print(i)
#     n += 1
#
# print(n)
# import requests
#
# link = 'http://pdf.dfcfw.com/pdf/H3_AP201803061099567744_1.PDF'
# with requests.get(url=link, stream=True) as f:
#     f.raise_for_status()
#     # self.logger.info('请求状态码为{},开始下载'.format(f.status_code))
#
#     with open('./11.pdf', 'wb') as file:
#         for chunk in f.iter_content(chunk_size=1024):
#             if chunk:
#                 file.write(chunk)