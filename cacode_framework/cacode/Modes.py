# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# File Name:        Modes
# Author:           CACode
# Version:          1.2
# Created:          2021/4/27
# Description:      Main Function:    所有用到的设计模式
#                   此文件内保存可外置的设计模式,用于让那些脑瘫知道我写的框架用了什么设计模式而不是
#                   一遍一遍问我这框架都用了什么设计模式、体现在哪里,我叼你妈
# Class List:    Singleton -- 单例模式
#                Recursion -- 深度搜索树
# History:
#       <author>        <version>       <time>      <desc>
#        CACode            1.2         2021/4/27    将设计模式迁移到此文件内
# ------------------------------------------------------------------
class Replaceable:
    pass


class Singleton:
    """
    使用单例模式
    """

    @staticmethod
    def createFactory(cls):
        with cls._instance_lock:
            if not hasattr(cls, "__instance__"):
                cls.__instance__ = cls(cls.modules)
        return cls.__instance__

    @staticmethod
    def createDbOpera(cls):
        with cls._instance_lock:
            if not hasattr(cls, "__instance__"):
                cls.__instance__ = object.__new__(cls)
        return cls.__instance__


class Recursion:
    """
    递归
    """

    @staticmethod
    def find_key_for_dict(obj_data: dict, target: str):
        """
        在字典里重复递归,直到得出最后的值,如果查不到就返回None
        """

        def parse_list(listData: list, tag: str):
            result_list = []
            if listData is not None:
                if isinstance(listData, list):
                    for i in listData:
                        if isinstance(i, list) or isinstance(i, tuple):
                            rt = parse_list(list(i), tag)
                            if rt:
                                result_list.append(rt)
                        elif isinstance(i, dict):
                            result_list.append(parse_dict(i, tag))
                        else:
                            result_list.append(parse_obj(i, tag))

                elif isinstance(listData, tuple):
                    result_list.append(parse_list(list(listData), tag))

                elif isinstance(listData, dict):
                    result_list.append(parse_dict(listData, tag))
                else:
                    result_list.append(parse_obj(listData, tag))

            else:
                return result_list
            return result_list

        def parse_dict(dictData, tag: str):
            result_dict = []
            if dictData is not None:
                if isinstance(dictData, dict):
                    if tag in dictData.keys():
                        result_dict.append(dictData.get(tag))
                        dictData.pop(tag)
                    for index, value in dictData.items():
                        if isinstance(value, list) or isinstance(value, tuple):
                            result_dict.append(parse_list(list(value), tag))
                        elif isinstance(value, dict):
                            result_dict.append(parse_dict(value, tag))
                        else:
                            result_dict.append(parse_obj(value, tag))
                elif isinstance(dictData, list):
                    result_dict.append(parse_list(list(dictData), tag))

                else:
                    result_dict.append(parse_obj(dictData, tag))
            else:
                return None
            return result_dict

        def parse_obj(objData, tag: str):

            def load(da: dict):
                obj_item_list = []
                obj_item_dict = {}
                for i, v in da.items():
                    if i == tag:
                        result_obj.append(getattr(objData, i))
                        continue
                    if isinstance(v, list):
                        obj_item_list.append(getattr(objData, i))
                    elif isinstance(v, dict):
                        obj_item_dict[i] = v

                result_obj.append(parse_list(obj_item_list, tag))
                result_obj.append(parse_dict(obj_item_dict, tag))

            result_obj = []

            if isinstance(objData, dict):
                result_obj.append(parse_dict(objData, tag))
            elif isinstance(objData, list):
                result_obj.append(parse_list(list(objData), tag))
            else:
                if isinstance(objData, object):
                    if isinstance(objData, str):
                        return None
                    elif isinstance(objData, int):
                        return None
                    elif isinstance(objData, float):
                        return None
                    else:
                        if hasattr(objData, tag):
                            result_obj.append(getattr(objData, tag))
                            load(da=objData.__dict__)
                        else:
                            load(da=objData.__dict__)
            return result_obj

        return parse_obj(obj_data, target)

        # cp_data = data
        #
        # serializer_data = JsonUtil.parse(cp_data, end_load=True)
        #
        # result = None
        # if key in serializer_data.keys():
        #     return f"{cp_data.__class__.__name__}.{key}"
        # for i in serializer_data.keys():
        #     if isinstance(serializer_data[i], dict):
        #         result = Recursion.find_key_for_dict(cp_data[i], key)
        #         # 如果在这个字段里找不到对应的键
        #         if result is None:
        #             continue
        #         else:
        #             break
        #     else:
        #         continue
        #
        # rep_list = str(result).split('.')
        # obj = data
        # for i in rep_list:
        #     if hasattr(obj, i):
        #         obj = getattr(obj, i)
        # return result


if __name__ == '__main__':
    rep = Replaceable()
    rep.a = {
        "a": "b",
        "b": "c",
        "c": [
            {
                "a": "b",
                "b": "c",
                "c": [
                ]
            }
        ],
        "d": {
            "a": "b",
            "b": "c",
            "c": [
            ]
        },
    }
    data = {
        "a": "b",
        "b": "c",
        "c": [
            {
                "a": "b",
                "b": "c",
                "c": [
                    {
                        "a": "b",
                        "b": "c",
                        "c": [
                            {
                                "a": "b",
                                "b": "c",
                                "c": [{
                                    "a": "b",
                                    "b": "c",
                                    "c": [
                                        {
                                            "a": "b",
                                            "b": "c",
                                            "c": [{
                                                "a": "b",
                                                "b": "c",
                                                "c": [
                                                    {
                                                        "a": "b",
                                                        "b": "c",
                                                        "c": [
                                                        ]
                                                    }
                                                ],
                                                "d": {
                                                    "a": "b",
                                                    "b": "c",
                                                    "c": [
                                                    ]
                                                },
                                                "e": rep
                                            }
                                            ]
                                        }
                                    ],
                                    "d": {
                                        "a": "b",
                                        "b": "c",
                                        "c": [{
                                            "a": "b",
                                            "b": "c",
                                            "c": [
                                                {
                                                    "a": "b",
                                                    "b": "c",
                                                    "c": [
                                                    ]
                                                }
                                            ],
                                            "d": {
                                                "a": "b",
                                                "b": "c",
                                                "c": [
                                                ]
                                            },
                                            "e": rep
                                        }
                                        ]
                                    },
                                    "e": rep
                                }
                                ]
                            }
                        ],
                        "d": {
                            "a": "b",
                            "b": "c",
                            "c": [{
                                "a": "b",
                                "b": "c",
                                "c": [
                                    {
                                        "a": "b",
                                        "b": "c",
                                        "c": [
                                        ]
                                    }
                                ],
                                "d": {
                                    "a": "b",
                                    "b": "c",
                                    "c": [
                                    ]
                                },
                                "e": rep
                            }
                            ]
                        },
                        "e": rep
                    }
                ]
            }
        ],
        "d": {
            "a": "b",
            "b": "c",
            "c": [
            ]
        },
        "e": rep
    }
    result = Recursion.find_key_for_dict(data, "a")
    from cacode_framework.cacode.Serialize import JsonUtil

    print(JsonUtil.parse(result))


    def dict_to_object(dict_data: dict, instance=Replaceable):
        """
        将字典转换为对象
        """
        obj = instance()

        if isinstance(dict_data, dict):
            for key, val in dict_data.items():
                setattr(obj, key, val)

        return obj
