## 脚本起源
公司在迁移老系统(基于Django框架)时，需要新老系统并行一段时间，而因为诸多原因，老系统(数据库是mysql)无法开启binlog
并且没有条件进行多次数据迁移，进而只能开发写脚本进行数据同步  

***
## 本代码实现的方案
利用[django-simple-history](https://github.com/jazzband/django-simple-history)记录数据
量较大的表的变更记录，(后续时其他脚本实现)每隔一段时间将变更或者新增的id同步给另一个服务，另一个服务将指定id的数据dump出来，
并在新系统中进行source

***
## 脚本使用步骤
1.参考[django-simple-history](https://django-simple-history.readthedocs.io/en/latest/quick_start.html)

2.patch每个需要记录的model(针对django bulk_create or bulk_update 建议不要使用batch_size)

3.将model的objects属性置为HistoryManager()  



***
***ps:可以使用django-simple-history只记录需要的字段***


