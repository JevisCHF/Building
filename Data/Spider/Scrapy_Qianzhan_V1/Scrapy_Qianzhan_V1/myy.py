import pymysql


def connet():
    db = pymysql.connect("localhost", "root", "root", "building")

    cursor = db.cursor()

    return db, cursor


def select_count(parent_id):
    db, cursor = connet()

    sql = f'SELECT * FROM building_qianzhan where parent_menu_id = \'{parent_id}\''
    # print(sql)
    count = cursor.execute(sql)
    # print(count)
    cursor.close()
    db.close()

    return count


def select(isRep, title):
    db, cursor = connet()
    sql = f'SELECT * FROM building_qianzhan where isRep = \'{isRep}\' and menu_name = \'{title}\''
    # print(sql)
    count = cursor.execute(sql)
    # print(count)
    cursor.close()
    db.close()
    return count


def insert(id, menu, parent_id, isRep):
    db, cursor = connet()
    try:
        # sql = "insert into building_qianzhan_copy1(id, menu_name, parent_menu_id) values('%s','%s','%s');" % (
        #     id, menu, parent_id)
        # print(sql)

        # 这种方式可解决验证问题
        sql = "insert into building_qianzhan(id, menu_name, parent_menu_id, isRep) values(%s,%s,%s,%s);"
        info = cursor.execute(sql, (id, menu, parent_id, isRep))
        # print(info)
        db.commit()
        cursor.close()
        db.close()
        return info
    except Exception as e:
        print(e)
        db.rollback()


if __name__ == '__main__':
    parent_id = '5001000001'
    title = '行业经济>房地产及建筑业>土地交易数据库:城市>土地交易数据库:城市(季)>四川>土地交易统计:成都市(季)'
    id = '0000011'
    menu = '或者在'
    p_id = '000'
    # a = select_count(parent_id)
    # b = insert(id, menu, p_id)
    c = select(title)
    # print(type(a), a, b, c)
    print(c)