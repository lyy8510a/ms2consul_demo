#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by liaoyangyang1 on 2018/9/19 下午3:07.
"""
import os
import sys
import time
import uuid
import signal
import subprocess
import threading
import multiprocessing
from flask import current_app as app

from utils.consulclient import ConsulClient

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


# 获取一个唯一操作码
def get_uid():
    return uuid.uuid4()


# 异步执行任务
def async_task(func, *args):
    p = multiprocessing.Process(target=func, args=args)
    p.start()


# 上传文件允许的类型
def allowed_file(filename):  # 通过将文件名分段的方式查询文件格式是否在允许上传格式范围之内
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


# 获取当前时间
def get_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def get_salt():
    return time.strftime('%Y%m%d', time.localtime(time.time()))


# 字符串转列表
def str2list(param):
    list = []
    if param and isinstance(param, str):
        if ',' in param:
            list = param.split(',')
        else:
            list.append(param)

    return list


# 读文件
def readFile(filedir):
    try:
        with open(filedir, 'r', encoding='utf8') as f:
            str = f.read()
        return str
    except Exception as e:
        app.logger.error(e)


# 写文件
def writeFile(filedir, content):
    try:
        with open(filedir, 'w', encoding='utf8') as f:
            f.write(str(content))
    except Exception as e:
        app.logger.error(e)


# 模型转字典
def modelobj2dict(object):
    result = []
    for record in object:
        dict = {}
        for k, v in record.__dict__.items():
            if not k == '_sa_instance_state':
                dict[k] = '' if v == None else v
        result.append(dict)

    return result


# 字典转字符串等式
def dict2str(dict):
    return ",".join(["{0}='{1}'".format(k, v) for k, v in dict.items()])


def get_pid_file_path(service):
    return os.path.join(BASE_DIR, '{}.pid'.format(service))


def get_log_file_path(service):
    try:
        os.makedirs(os.path.join(BASE_DIR, "logs"))
    except:
        pass

    LOG_DIR = os.path.join(BASE_DIR, "logs")

    return os.path.join(LOG_DIR, '{}.log'.format(service))


def check_pid(pid):
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


def get_pid(service):
    pid_file = get_pid_file_path(service)
    if os.path.isfile(pid_file):
        with open(pid_file) as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return 0
    return 0


def is_running(s, unlink=True):
    pid_file = get_pid_file_path(s)

    if os.path.isfile(pid_file):
        with open(pid_file, 'r') as f:
            pid = get_pid(s)
        if check_pid(pid):
            return True

        if unlink:
            os.unlink(pid_file)
    return False


def parse_service(s):
    if s == 'all':
        return [s]
    else:
        return [s]


def start_gunicorn():
    app.logger.info("\n- Start Gunicorn WSGI HTTP Server")
    service = 'gunicorn'
    bind = '{}:{}'.format(app.config['HOST'], app.config['PORT'])
    log_format = '%(h)s %(t)s "%(r)s" %(s)s %(b)s '
    pid_file = get_pid_file_path(service)
    log_file = get_log_file_path(service)

    cmd = [
        'gunicorn',
        '-b', bind,
        'apps:create_app()',
        '-k', 'eventlet',
        '-w', str(app.config['WORKERS']),
        '--access-logformat', log_format,
        '-p', pid_file,
    ]

    if app.config['DAEMON']:
        cmd.extend([
            '--access-logfile', log_file,
            '--daemon',
        ])
    else:
        cmd.extend([
            '--access-logfile', '-'
        ])
    if app.config['DEBUG']:
        cmd.append('--reload')

    p = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr, cwd=BASE_DIR)
    return p


def start_service(s):
    app.logger.info(time.ctime())

    services_handler = {
        "gunicorn": start_gunicorn
    }

    services_set = parse_service(s)
    processes = []
    for i in services_set:
        if is_running(i):
            show_service_status(i)
            continue
        func = services_handler.get(i)
        p = func()
        processes.append(p)

    now = int(time.time())
    for i in services_set:
        while not is_running(i):
            if int(time.time()) - now < app.config['START_TIMEOUT']:
                time.sleep(1)
                continue
            else:
                app.logger.error("Error: {} start error".format(i))
                stop_multi_services(services_set)
                return

    stop_event = threading.Event()

    if not app.config['DAEMON']:
        signal.signal(signal.SIGTERM, lambda x, y: stop_event.set())
        while not stop_event.is_set():
            try:
                time.sleep(10)
            except KeyboardInterrupt:
                stop_event.set()
                break

        app.logger.info("Stop services")
        for p in processes:
            p.terminate()

        for i in services_set:
            stop_service(i)
    else:
        print()
        show_service_status(s)


def stop_service(s, sig=15):
    services_set = parse_service(s)
    for s in services_set:
        if not is_running(s):
            show_service_status(s)
            continue
        print("Stop service: {}".format(s))
        pid = get_pid(s)
        os.kill(pid, sig)


def stop_multi_services(services):
    for s in services:
        stop_service(s, sig=9)


def stop_service_force(s):
    stop_service(s, sig=9)


def show_service_status(s):
    services_set = parse_service(s)
    for ns in services_set:
        if is_running(ns):
            pid = get_pid(ns)
            print("{} is running: {}".format(ns, pid))
        else:
            print("{} is stopped".format(ns))


def register_consul():
    try:
        httpcheck = 'http://' + app.config['HOST'] + ':' + str(app.config['PORT']) + '/check'
        service_id = app.config['PROJECTNAME'] + app.config['HOST'] + ':' + str(app.config['PORT'])
        # 注册服务到consul,不需要则注释
        ConsulClient(host=app.config['CONSUL_HOST'], port=app.config['CONSUL_PORT']).register(
            name=app.config['PROJECTNAME'], service_id=service_id,
            address=app.config['HOST'],
            port=app.config['PORT'], tags=app.config['CONSUL_TAG'],
            interval='30s',
            httpcheck=httpcheck)
    except Exception as e:
        app.logger.error(e)

def deregister_consul():
    try:
        service_id = app.config['PROJECTNAME'] + app.config['HOST'] + ':' + str(app.config['PORT'])
        ConsulClient(host=app.config['CONSUL_HOST'], port=app.config['CONSUL_PORT']).deregister(service_id)
    except Exception as e:
        app.logger.error(e)

if __name__ == '__main__':
    print(get_pid_file_path('messer'))
