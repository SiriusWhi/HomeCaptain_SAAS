import os
from fabric import Connection
from fabric import task

abs_dir_path = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))

user = 'app'
host = '52.14.116.20'
connect_kwargs = {
    'key_filename':'ssh-keys/id_rsa_deploy'
}

@task
def deploy_staging(ctx):
    c = Connection(host=host, user=user, connect_kwargs=connect_kwargs)
    c.run('cd home-captain-dev/homecaptain && ./deploy.sh')
    
