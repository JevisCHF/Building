from Scrapy_Qianzhan_V1.settings import PROVINCES
from Scrapy_Qianzhan_V1.file import cate1


# def find_region(name):
#     item = {}
#     # 国家
#     for c in COUNTRY:
#         if c in name:
#             if c != '中国':
#                 item['country'] = c
#                 item['region'] = '全国'
#             elif c == '中国':
#                 item['country'] = c
#                 item['region'] = '全国'
#
#     # 地区
#     for p in PROVINCES['all']:
#         if p in name:
#             item['country'] = '中国'
#             item['region'] = p
#             break
#     for city in PROVINCES['city']:
#         key = city.replace('市', '')
#         if key in name:
#             item['country'] = '中国'
#             item['region'] = city
#             break
#     if len(item) <= 0:
#         # 国家
#         item['country'] = None
#         # 地区
#         item['region'] = None
#     print(item)
#     return item


def region_find(title):
    item = {}

    for i, n in cate1.items():
        # print(i, n)

        if n in title:
            if len(i) < 8:
                pass
                # for p, c in prevince.items():
                #     if i in p:
                #         item['p_id'] = p
                #         item['region'] = c
            else:
                item['p_id'] = i
                item['region'] = n

            item['country'] = '中国'

            print(item)
            return item
        else:
            pass


if __name__ == '__main__':
    name = '长沙市:全社会固定资产投资完成额:累计值 (月)'
    name1 = '香港:公共财政预算收入:累计同比 (月)'
    # a = find_region(name)
    a = region_find(name1)
