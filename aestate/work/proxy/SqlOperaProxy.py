# -*- utf-8 -*-
from aestate.work.Modes import EX_MODEL


class RepositoryProxy:
    """
    代理仓库的操作方式所有Repository的调用都会经过这里

    这个位置是用来方便使用type对象的Pojo类行为

    通过Repository的__get__方法获得调用时的cls值,使得

    """
    pass


class RepositoryAsyncProxy:
    """
    代理执行仓库的异步操作,详情请查看SqlOperaProxy类
    """

    async def find_all_async(self, *args, **kwargs):
        return self.find_all(*args, **kwargs)

    async def find_field_async(self, *args, **kwargs):
        return self.find_field(*args, **kwargs)

    async def find_one_async(self, *args, **kwargs):
        return self.find_one(*args, **kwargs)

    async def find_many_async(self, *args, **kwargs):
        return self.find_many(*args, **kwargs)

    async def find_sql_async(self, *args, **kwargs):
        return self.find_sql(*args, **kwargs)

    async def update_async(self, *args, **kwargs):
        return self.update(*args, **kwargs)

    async def remove_async(self, *args, **kwargs):
        return self.remove(*args, **kwargs)

    async def save_async(self, *args, **kwargs):
        return self.save(*args, **kwargs)

    async def create_async(self, pojo, **kwargs):
        return self.create(pojo, **kwargs)

    async def execute_sql_async(self, sql, params=None, mode=EX_MODEL.SELECT, **kwargs):
        return self.execute_sql(sql=sql, params=params, mode=mode, **kwargs)
