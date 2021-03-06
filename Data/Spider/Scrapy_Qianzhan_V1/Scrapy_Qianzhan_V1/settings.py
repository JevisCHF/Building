# -*- coding: utf-8 -*-

# Scrapy settings for Scrapy_Qianzhan_V1 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Scrapy_Qianzhan_V1'

SPIDER_MODULES = ['Scrapy_Qianzhan_V1.spiders']
NEWSPIDER_MODULE = 'Scrapy_Qianzhan_V1.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Scrapy_Qianzhan_V1 (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

import random

DOWNLOAD_DELAY = random.uniform(4, 6)
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

MONGO_URI = "127.0.0.1:27017"
MONGO_DB = "Building_new"  # 库名
RETRY_ENABLED = True  # 打开重试开关
RETRY_TIMES = 3  # 重试次数
DOWNLOAD_TIMEOUT = 10  # 超时
RETRY_HTTP_CODES = [503, 500, 502, 404, 400, 403]

SPIDER_MIDDLEWARES = {
    'Scrapy_Qianzhan_V1.middlewares.ProxyMiddleWare': 543,
    # 'Scrapy_Qianzhan_V1.middlewares.ScrapyRobodatabaseV115SpiderMiddleware': 543,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,

}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'Scrapy_Qianzhan_V1.middlewares.ProxyMiddleWare': 543,
    # 'Scrapy_Qianzhan_V1.middlewares.ScrapyRobodatabaseV115DownloaderMiddleware': 543,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,

}

ITEM_PIPELINES = {
    'Scrapy_Qianzhan_V1.pipelines.ScrapyRobodataV102Pipeline': 300,
}

# 日志等级
# LOG_LEVEL = 'INFO'

COUNTRY = [
    "中国", "蒙古", "朝鲜", "韩国", "日本", "越南", "老挝", "柬埔寨", "缅甸", "泰国", "马来西亚", "新加坡", "印尼"
                                                                                "文莱", "菲律宾", "印度尼西亚", "东帝汶", "尼泊尔",
    "不丹", "孟加拉国", "印度", "斯里兰卡", "马尔代夫",
    "智利", "巴基斯坦", "阿富汗", "伊朗", "科威特", "沙特阿拉伯", "巴林", "卡塔尔", "阿联酋", "阿曼", "也门",
    "伊拉克", "叙利亚", "黎巴嫩", "约旦", "巴勒斯坦", "以色列", "塞浦路斯", "土耳其", "乌兹别克斯坦", "哈萨克斯坦",
    "吉尔吉斯斯坦", "塔吉克斯坦", "亚美尼亚", "土库曼斯坦", "阿塞拜疆", "格鲁吉亚", "冰岛", "丹麦", "挪威", "刚果(布)"
                                                                          "瑞典", "芬兰", "俄罗斯", "乌克兰", "白俄罗斯", "摩尔多瓦",
    "立陶宛", "爱沙尼亚", "拉脱维亚", "巴拿马", "几内亚",
    "波兰捷克", "匈牙利", "德国", "奥地利", "列支敦士登", "瑞士", "荷兰", "比利时", "卢森堡", "英国", "爱尔兰", "法国",
    "摩纳哥", "安道尔", "西班牙", "葡萄牙", "意大利", "梵蒂冈", "圣马力诺", "马耳他", "克罗地亚", "斯洛伐克", "斯洛文尼亚",
    "波黑", "马其顿", "塞尔维亚", "黑山", "科索沃", "罗马尼亚", "保加利亚", "阿尔巴尼亚", "希腊", "埃及", "利比亚",
    "突尼斯", "阿尔及利亚", "摩洛哥", "毛里塔尼亚", "塞内加尔", "冈比亚", "马里", "布基纳法索", "佛得角", "几内亚比绍",
    "几内亚", "塞拉里昂", "利比里亚", "科特迪瓦", "加纳", "多哥", "贝宁", "尼日尔", "尼日利亚", "喀麦隆", "赤道几内亚",
    "乍得", "中非", "苏丹", "埃塞俄比亚", "吉布提", "索马里", "肯尼亚", "乌干达", "坦桑尼亚", "卢旺达", "布隆迪", "刚果(金)",
    "加蓬", "圣多美和普林西比", "安哥拉", "赞比亚", "马拉维", "莫桑比克", "科摩罗", "马达加斯加", "塞舌尔", "毛里求斯",
    "津巴布韦", "博茨瓦纳", "纳米比亚", "南非", "斯威士兰", "莱索托", "厄立特里亚", "澳大利亚", "新西兰", "巴布亚新几内亚",
    "所罗门群岛", "瓦努阿图", "斐济", "基里巴斯", "瑙鲁", "密克罗尼西亚", "马绍尔群岛", "图瓦卢", "萨摩亚", "西萨摩亚",
    "纽埃", "帕劳", "汤加", "加拿大", "美国", "墨西哥", "危地马拉", "伯利兹", "萨尔瓦多", "洪都拉斯", "尼加拉瓜", "哥斯达黎加",
    "巴哈马", "古巴", "牙买加", "海地", "多米尼加", "圣基茨和尼维斯", "安提瓜和巴布达", "多米尼克国", "圣卢西亚", "圣文森特和格林纳丁斯",
    "巴巴多斯", "格林纳达", "特立尼达和多巴哥", "哥伦比亚", "委内瑞拉", "圭亚那", "苏里南", "厄瓜多尔", "秘鲁", "巴西", "玻利维亚",
    "阿根廷", "巴拉圭", "乌拉圭"]

PROVINCES = {
    "all": [
        "北京", "上海", "重庆", "天津", "香港", "澳门",
        "河南", "安徽", "福建", "甘肃", "贵州", "海南", "河北", "黑龙江", "湖北",
        "湖南", "吉林", "江苏", "江西", "辽宁", "青海", "山东", "山西", "陕西",
        "四川", "云南", "浙江", "台湾", "广东", "广西", "内蒙古", "宁夏", "西藏", "新疆", "全国"],
    'city': ['亳州', '六安', '合肥', '安庆', '宣城', '宿州', '巢湖', '池州', '淮北', '淮南', '滁州', '芜湖', '蚌埠', '铜陵', '阜阳', '马鞍山', '黄山',
             '澳门', '北京', '重庆', '三明', '南平', '厦门', '宁德', '泉州', '漳州', '福州', '莆田', '龙岩', '临夏', '兰州', '嘉峪关', '天水', '定西',
             '平凉', '庆阳', '张掖', '武威', '甘南', '白银', '酒泉', '金昌', '陇南', '东莞', '中山', '云浮', '佛山', '广州', '惠州', '揭阳', '梅州', '汕头',
             '汕尾', '江门', '河源', '深圳', '清远', '湛江', '潮州', '珠海', '肇庆', '茂名', '阳江', '韶关', '北海', '南宁', '崇左', '来宾', '柳州', '桂林',
             '梧州', '河池', '玉林', '百色', '贵港', '贺州', '钦州', '防城港', '六盘水', '安顺', '毕节', '贵阳', '遵义', '铜仁', '黔东南', '黔南', '黔西南',
             '三亚', '海口', '青海州', '保定', '唐山', '廊坊', '张家口', '承德', '沧州', '石家庄', '秦皇岛', '衡水', '邢台', '邯郸', '七台河', '伊春', '佳木斯',
             '双鸭山', '哈尔滨', '大兴安岭', '大庆', '牡丹江', '绥化', '鸡西', '鹤岗', '黑河', '齐齐哈尔', '三门峡', '信阳', '南阳', '周口', '商丘', '安阳',
             '平顶山', '开封', '新乡', '洛阳', '济源', '漯河', '濮阳', '焦作', '许昌', '郑州', '驻马店', '鹤壁', '仙桃', '十堰', '咸宁', '天门', '孝感',
             '宜昌', '恩施', '武汉', '潜江', '神农架', '荆州', '荆门', '襄樊', '鄂州', '随州', '黄冈', '黄石', '娄底', '岳阳', '常德', '张家界', '怀化',
             '株洲', '永州', '湘潭', '湘西', '益阳', '衡阳', '邵阳', '郴州', '长沙', '南京', '南通', '宿迁', '常州', '徐州', '扬州', '无锡', '泰州', '淮安',
             '盐城', '苏州', '连云港', '镇江', '上饶', '九江', '南昌', '吉安', '宜春', '抚州', '新余', '景德镇', '萍乡', '赣州', '鹰潭', '吉林', '四平',
             '延边', '松原', '白城', '白山', '辽源', '通化', '长春', '丹东', '大连', '抚顺', '朝阳', '本溪', '沈阳', '盘锦', '营口', '葫芦岛', '辽阳',
             '铁岭', '锦州', '阜新', '鞍山', '乌兰察布', '乌海', '兴安盟', '包头', '呼伦贝尔', '呼和浩特', '巴彦淖尔', '赤峰', '通辽', '鄂尔多斯', '锡林郭勒',
             '阿拉善', '中卫', '吴忠', '固原', '石嘴山', '银川', '果洛', '海东', '海北', '海南州', '海西', '玉树', '西宁', '黄南', '东营', '临沂', '威海',
             '德州', '日照', '枣庄', '泰安', '济南', '济宁', '淄博', '滨州', '潍坊', '烟台', '聊城', '莱芜', '菏泽', '青岛', '上海', '咸阳', '商洛', '安康',
             '宝鸡', '延安', '榆林', '汉中', '渭南', '西安', '铜川', '太原市', '大同市', '阳泉市', '长治市', '晋城市', '朔州市', '忻州市', '晋中市', '临汾市',
             '吕粱市', '运城市', '原平市', '潞城市', '候马市', '古交市', '孝义市', '介休市', '永济市', '汾阳市', '乐山', '内江', '凉山', '南充', '宜宾', '巴中',
             '广元', '广安', '德阳', '成都', '攀枝花', '泸州', '甘孜', '眉山', '绵阳', '自贡', '资阳', '达州', '遂宁', '阿坝', '雅安', '台湾', '天津',
             '香港', '乌鲁木齐', '五家渠', '伊犁', '克孜勒苏', '克拉玛依', '博尔塔拉', '吐鲁番', '和田', '哈密', '喀什', '图木舒克', '塔城', '巴音郭楞', '昌吉',
             '石河子', '铁门关', '阿克苏', '阿勒泰', '阿拉尔', '山南', '拉萨', '日喀则', '昌都', '林芝', '那曲', '阿里', '临沧', '丽江', '保山', '大理', '德宏',
             '怒江', '文山', '昆明', '昭通', '普洱', '曲靖', '楚雄', '玉溪', '红河', '西双版纳', '迪庆', '丽水', '台州', '嘉兴', '宁波', '杭州', '温州',
             '湖州', '绍兴', '舟山', '衢州', '金华'],
}

Dir = {
    '5001': '房屋建筑',
    '5002': '土木工程建筑',
    '5003': '建筑安装业',
    '5004': '建筑装饰、装修和其他建筑业',
}
