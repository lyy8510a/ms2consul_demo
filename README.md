# Python Flask微服务Demo
使用Python3.6，使用方式有一点要注意，如果没consul的话，需要在manage.py注释掉runserver中register_consul()和stopserver中的deregister_consul()。
执行pip install -r requirement.txt <br>
然后python manage.py runserver即可。<br>
支持Rpc和restfull
