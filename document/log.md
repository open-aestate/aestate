# 日志篇

## 路径问题

如果你是用一个新的类作为父类去编写模板pojo，例如:

```python
class BaseDatabaseConfig(Pojo):
    def __init__(self, **kwargs):
        super(BaseDatabaseConfig, self).__init__(
            config_obj=BaseDataBase(),
            log_conf={
                # 确认保存
                'save_flag': True,
                # 保存位置
                'path': '/cacode/cacode.ren/blog_logs/',
                # 日志最大100MB清除
                'max_clear': 100,
            }
        )
```

那么`path`参数一定要写上绝对路径,并且尾部需要加上`/`，因为你需要表示的是在这个文件夹下存放日志，而不是在这个文件夹编写日志

## 保存问题

当日志没有正确保存时，你应该检查配置类的`save_flag`是否为`True`,其次检查当前系统是否有权限对 文件夹/文件 进行创建、修改和删除权限

检查有没有配置日志，当然你也可以不配，但是最好是配一个日志

## 清除问题

设置`max_clear`时需要注意，这里的大小是以`mb`为单位的，也就是`1024kb`。日志到达或超过设置的大小但是没有删除的原因可能有两种，一是系统没有权限，二是刚刚超过日志的阈值，下一次有日志时才会新键一个日志

## 日志的格式

目前固定日志格式：

2021-11-27 10:36:27.818178 ERROR 344 0x204607b7ef0 [  ERROR] aestate.util.Log.ALog : message  
时间 级别 行号 内存地址 类型 执行类 : 消息

## 关于banner

1.0.4a4目前banner不允许修改