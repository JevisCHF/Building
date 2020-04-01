from Scrapy_Qianzhan_V1.file import cate1


def coless(title):
    for i, c in cate1.items():
        if c in title:
            p_id = i
            print(p_id)


if __name__ == '__main__':
    title = '广州，房屋'
    coless(title)
