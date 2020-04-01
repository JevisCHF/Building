import requests, re
from lxml import etree

for a in range(3):
    url = f'http://www.crcc.cn/module/web/jpage/dataproxy.jsp?startrecord={a*60 + 1}&perpage=20'

    data = {
        'col': 1,
        'appid': 1,
        'webid': 1,
        'path': '/',
        'columnid': '1577',
        'sourceContentType': '1',
        'unitid': '12006',
        'webname': '中国铁建股份有限公司',
        'permissiontype': '0',
    }

    req = requests.post(url, data=data)

    # print(req.text)

    period_date = re.findall(r'<recordset>(.+)</recordset>', req.text)[0]
    # print(period_date[0])
    p = period_date.replace(r'<record><![CDATA[', '').replace(r']]></record>', '')
    # print(p)

    html = etree.HTML(p)
    # print(html)
    lis = html.xpath('//li')
    n = 1
    for i in lis:
        # print(i.xpath('./span/text()'))
        issue_time = i.xpath('./span/text()')[0]
        title = i.xpath('./a/@href')[0]
        link = i.xpath('./a/text()')[0]
        print(title, issue_time, link)
        n += 1
    print(n)
