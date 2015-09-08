apt-get -qqy update
apt-get -qqy install postgresql python-psycopg2
apt-get -qqy install python-flask python-sqlalchemy
apt-get -qqy install python-pip
apt-get -qqy install node npm
apt-get -qqy install libmagickwand-dev
sudo npm install --global gulp
pip install bleach
pip install oauth2client
pip install requests
pip install httplib2
pip install Flask-SQLAlchemy
pip install python-slugify
pip install Flask-WTF
pip install Wand
su postgres -c 'createuser -dRS vagrant'
su vagrant -c 'createdb'
su vagrant -c 'createdb catalog'
su - vagrant -c "python /vagrant/catalog/seed.py"

vagrantTip="[35m[1mThe shared directory is located at /vagrant\nTo access your shared files: cd /vagrant(B[m"
echo -e $vagrantTip > /etc/motd

