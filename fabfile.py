from fabric.api import local
from fabric.api import cd,run,env,prefix

env.hosts=[
    'services@10.111.0.169:22'
]
env.passwords = {
    'services@10.111.0.169:22' : 'services',
}

def commit():
    local('git add -A && git commit -m "update" && git push -u origin master')

def init():
    with cd('~/taojinqiu'):
        # install virtual environment
        run('rm -rf env')
        run('virtualenv env')

        # install ks3sdk
        run('rm -rf ks3-python-sdk')
        run('git clone https://github.com/ks3sdk/ks3-python-sdk.git')
        with cd('ks3-python-sdk'), prefix('source ~/taojinqiu/env/bin/activate'):
            run('python setup.py install')
        run('rm -rf ks3-python-sdk')

        # download the source code
        run('rm -rf video_service')
        run('git clone https://git.yidian-inc.com:8021/crawler/video_service.git')
        run('mkdir video_service/log')

        # install packages
        with prefix('source ~/taojinqiu/env/bin/activate'):
            run('pip install -U -r video_service/requirements.txt --proxy=http://10.101.1.184:8080')

def stop():
    pass

def start():
    with cd('~/taojinqiu/video_service'), prefix('source ~/taojinqiu/env/bin/activate'):
        run('nohup python manage.py tornado 10.111.0.169 5007 &')

def restart():
    pass

