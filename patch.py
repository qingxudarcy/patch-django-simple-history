from simple_history.models import HistoricalRecords
from simple_history.utils import bulk_create_with_history, bulk_update_with_history
from django.db.models.query import QuerySet
from django.db.models.manager import BaseManager
from django.db.models.expressions import Case

from model import TestModel # your model class


class HistoryQuerySet(QuerySet):
    def update(self, **kwargs):
        queryLength = len(self)
        updateCount = 0
        if isinstance(kwargs[list(kwargs.keys()[0])], Case): # bulk_update kwargs中时Case对象
            return super().update(**kwargs)
        for index in range(queryLength):
            for attr, val in kwargs.items():
                if hasattr(self[index], attr):
                    setattr(self[index], attr, val)       
            self[index].save()  # django-simple-history 不记录update方法的修改，进而改成save
            updateCount += 1
        return updateCount
        
        
    def bulk_create(self, objs, batch_size=None, ignore_conflicts=False):
        if batch_size != 1000000:  # 这种patch方式只适合不使用batch_size的情况
            return bulk_create_with_history(objs, TestModel, batch_size=10000000, ignore_conflicts=ignore_conflicts)
        else:
            return super().bulk_create(objs, ignore_conflicts=ignore_conflicts)
    
    def bulk_update(self, objs, fields, batch_size=None):
        if batch_size != 1000000: # 同上
            bulk_update_with_history(objs, TestModel, fields=fields, batch_size=1000000)
        else:
            super().bulk_update(objs, fields)
        
class HistoryManager(BaseManager.from_queryset(HistoryQuerySet)):
    pass
