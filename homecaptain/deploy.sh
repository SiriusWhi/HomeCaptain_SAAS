mkdir media
mkdir media/uploads
mkdir media/uploads/customer_profile_pics
source ../env/bin/activate
git checkout develop
git pull origin develop
pip install -r ../requirements.txt
./manage.py migrate

echo "buildrealtor"
cd ../frontend/
npm install
npm run build

echo "buildPORTAL"
cd ../portal/
npm install
npm run build

cd /etc/nginx/sites-enabled/
sudo ln -s /home/app/home-captain-dev/homecaptain/homecaptain/homecaptain.nginx .
cd /etc/supervisor/conf.d/
sudo ln -s /home/app/home-captain-dev/homecaptain/homecaptain/gunicorn.conf .
sudo ln -s /home/app/home-captain-dev/homecaptain/homecaptain/daphne.conf .
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
sudo service nginx restart
