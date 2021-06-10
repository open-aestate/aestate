# -*- utf-8 -*-
# @Time: 2021/6/10 14:28
# @Author: CACode
from example.tables.demoModels import Write, WriteCp


def test_left_join():
    """
    SELECT * FROM `write` as w LEFT JOIN write_cp wcp on wcp.id = w.id
    """
    WriteOrm = Write().orm
    WriteCpOrm = WriteCp().orm
    sql = WriteOrm.find('COUNT(*)', h_func=True, asses=['c']).alias('w') \
        .left_join(sql_orm=WriteCpOrm, name='wcp') \
        .on(from_where='w.id', to_where='wcp.id', symbol='=').group_by('wcp.id', 'w.id', text=True)
    result = sql.end()
    print(result)
    return result


if __name__ == '__main__':
    test_left_join()
