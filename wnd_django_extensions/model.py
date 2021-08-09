import typing
from copy import deepcopy

from django.db import models
from django.db.models import Model

__all__ = [
    'WndModelMixin',
]


class WndModelMixin(object):
    def to_dict(self: models.Model, field_name_list: typing.Union[typing.List[str], None] = None):
        data = {}
        if field_name_list is None:
            # defaultは__all__
            field_name_list = []
            for default_field in self._meta.fields:
                # is_relationがTrueなら、foreignkey。many_to_manyとかは、self._meta.fieldsのプロパティ関数で弾かれてる
                if default_field.is_relation:
                    # foreignkeyは_idつける。_idなしなら、objectとして処理して返す。
                    field_name_list.append(default_field.name + '_id')
                else:
                    field_name_list.append(default_field.name)

        if 'id' not in field_name_list:
            field_name_list.insert(0, 'id')

        # field_name_list: ['a', 'b__f', 'b__d', 'b__d__p']を[['a'], ['b', 'f'], ['b', 'd'], ['b', 'd', 'p']]に変換する
        field_name_list_by_model_list: typing.List[typing.List[str]] = \
            [list(field_name.split('__')) for field_name in field_name_list]

        # 使わないし紛らわしいので消しておく
        del field_name_list

        field_name_dict_by_model: typing.Dict[str, typing.List[str]] = {}

        # [['a'], ['b', 'f'], ['b', 'd'], ['b', 'd', 'p']]を{'a': [], 'b': ['f', 'd', 'd__p']}に変換する
        for field_name_nested_list in deepcopy(field_name_list_by_model_list):
            parent_field_name = field_name_nested_list[0]
            done_file_name_list = field_name_dict_by_model.keys()
            if parent_field_name in done_file_name_list:
                continue
            # ネストがある場合
            if len(field_name_nested_list) > 1:
                child_field_name_list = []
                for field_list_by_model in field_name_list_by_model_list:
                    if parent_field_name == field_list_by_model[0]:
                        child_field_name_list.append('__'.join(field_list_by_model[1:]))
                field_name_dict_by_model[parent_field_name] = child_field_name_list
            else:
                field_name_dict_by_model[parent_field_name] = []

        all_fields_exclude_related: typing.List[str] = [field.name for field in self._meta.fields]

        for parent_field_name, child_field_name_list in field_name_dict_by_model.items():
            if parent_field_name not in all_fields_exclude_related:
                continue
            if not hasattr(self, parent_field_name):
                raise Exception(f'存在しないfieldです。parent_field_name: {parent_field_name}')
            value = getattr(self, parent_field_name)

            # ForeignKeyかどうかのやつ。いい判定方法がわからないので、Modelクラス継承してるかどうかで判断
            if isinstance(value, Model):
                if not hasattr(value, 'to_dict'):
                    raise Exception(f'WndModelMixinを継承していないので使用できません: {value}')
                value = value.to_dict(field_name_list=child_field_name_list if child_field_name_list else None)

            data[parent_field_name] = value

        related_field_list: typing.List[str] = [related_object.name for related_object in self._meta.related_objects]

        for parent_field_name, child_field_name_list in field_name_dict_by_model.items():
            if parent_field_name not in related_field_list:
                continue
            if not hasattr(self, parent_field_name):
                raise Exception(f'存在しないfieldです。parent_field_name: {parent_field_name}')
            data[parent_field_name] = [
                model_instance.to_dict(field_name_list=child_field_name_list if child_field_name_list else None)
                for model_instance in getattr(self, parent_field_name).all()]

        return data