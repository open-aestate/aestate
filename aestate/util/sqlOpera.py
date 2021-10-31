# -*- utf-8 -*-
import re


class TextUtil(object):
    """
    sql操作工具
    """

    @staticmethod
    def replace_antlr(sql, **kwargs):
        """
        :param sql:具有特殊含义的sql语句
        """
        # #{}使用%s隔离
        sub_sql = re.sub(r'#{(.*?)}', '%s', sql)
        context_hashtag = re.findall(r'#{(.*?)}', sql)
        new_args = [kwargs[i] for i in context_hashtag]

        # ${}直接替换
        context_dollar = re.findall(r'\${(.*?)}', sub_sql)
        for cd in context_dollar:
            # 只有int需要转换
            if isinstance(kwargs[cd], int):
                kwargs[cd] = str(kwargs[cd])
            sub_sql = sub_sql.replace('${' + cd + '}', kwargs[cd])
        return sub_sql, new_args
