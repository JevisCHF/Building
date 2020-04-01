# -*- coding: utf-8 -*-

urls1 = {
    '中国宏观-215': 'https://d.qianzhan.com/xdata/xsearch?q=%e5%bb%ba%e7%ad%91&cls=01&page=',
    # '行业经济-1214': 'https://d.qianzhan.com/xdata/xsearch?q=%e5%bb%ba%e7%ad%91&cls=02&page=',
    # '区域宏观-198': 'https://d.qianzhan.com/xdata/xsearch?q=%e5%bb%ba%e7%ad%91&cls=04&page=',
}
urls2 = {
    # '中国宏观-215': 'https://d.qianzhan.com/xdata/xsearch?q=%e5%bb%ba%e7%ad%91&cls=01&page=',
    '行业经济-1214': 'https://d.qianzhan.com/xdata/xsearch?q=%e5%bb%ba%e7%ad%91&cls=02&page=',
    # '区域宏观-198': 'https://d.qianzhan.com/xdata/xsearch?q=%e5%bb%ba%e7%ad%91&cls=04&page=',
}
urls3 = {
    # '中国宏观-215': 'https://d.qianzhan.com/xdata/xsearch?q=%e5%bb%ba%e7%ad%91&cls=01&page=',
    # '行业经济-1214': 'https://d.qianzhan.com/xdata/xsearch?q=%e5%bb%ba%e7%ad%91&cls=02&page=',
    '区域宏观-198': 'https://d.qianzhan.com/xdata/xsearch?q=%e5%bb%ba%e7%ad%91&cls=04&page=',
}

def get_url(data):
    # save_url = []
    for c, u in data.items():
        cs = c.split('-')
        for i in range(int(cs[1])):
        # for i in range(1):
            url = f'{u}{i + 1}'
            yield url


if __name__ == '__main__':
    # get_url(urls)
    print(get_url(urls))
