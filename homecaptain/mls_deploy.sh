source ../env/bin/activate
git checkout feature/HC-358-MLS_integration
git pull origin feature/HC-358-MLS_integration
pip install -r ../requirements.txt
./manage.py migrate

cd /etc/supervisor/conf.d/
sudo ln -s /home/app/home-captain-dev/homecaptain/homecaptain/celeryd.conf .
sudo ln -s /home/app/home-captain-dev/homecaptain/homecaptain/celerybeatd.conf .

sudo mkdir /run/homecaptain
sudo chown -R app /run/homecaptain

sudo mkdir /var/log/homecaptain
sudo chown -R app /var/log/homecaptain

sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl reload
sleep 10
#facing some anomalies with restart so adding a bruteforce reload + restart all
sudo supervisorctl restart all
