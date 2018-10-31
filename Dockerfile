#基于的基础镜像
FROM python:3.6.6

# 设置code文件夹是工作目录
WORKDIR /code/demo

#代码添加到code文件夹
COPY apps /code/demo/apps
COPY config /code/demo/config
COPY utils /code/demo/utils
COPY manage.py /code/demo/
COPY requirement.txt /code/demo/

# 安装支持
RUN cd /code/demo &&\
    pip install -r requirement.txt &&\
    python manage.py create_db

CMD ["python", "/code/demo/manage.py","runserver"]