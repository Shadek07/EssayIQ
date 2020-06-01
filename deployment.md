## EssayIQ project deployment in Digital Ocean cloud

First we need to create a **droplet** in Digital Ocean cloud. Droplet is a remote machine to host EssayIQ project. Each droplet
will be assigned a static IP address which can be used for remote login. 

In next step, I bought a domain (http://www.hdilab-essayiq.xyz/) from Namecheap. Then I had to add digital ocean nameservers to Namecheap domain.
The process of pointing to digitalocean nameserver is explained [here](https://www.digitalocean.com/community/tutorials/how-to-point-to-digitalocean-nameservers-from-common-domain-registrars).
Then, I had to create DNS record by following [this](https://www.digitalocean.com/docs/networking/dns/how-to/manage-records/) document.

A snapshot of EssayIQ dns record is provided.
![first graph](./digitalocean_dnsrecord.png)

PostgreSQL installation process in server for EssayIQ is done by following this [blog](https://linuxize.com/post/how-to-install-postgresql-on-ubuntu-18-04/).

The following commands need to execute during the process:

sudo ufw allow ‘Nginx HTTP’
sudo ufw enable
sudo ufw disable
sudo ufw allow ssh
(and try ssh login. After login)
sudo ufw enable
sudo ufw status

### Inside postgres command prompt:

postgres=# CREATE DATABASE conceptvectorDB; (database name is same as conceptvector project)
grant all privileges on database conceptvectorDB to shadek;

sudo nano /etc/postgresql/10/main/postgresql.conf
# - Connection Settings -
listen_addresses = '*'     # what IP address(es) to listen on;

### Creating python env and installing packages:

conda create -n essayiq python=2.7 anaconda
sudo apt-get install python-psycopg2
sudo apt-get install libpq-dev
sudo apt-get install python-dev
sudo apt-get install gcc
sudo apt-get install postgresql-client-common
sudo apt-get install postgresql-common
conda install -c travis uwsgi

sudo npm install -g npm@latest
sudo bower install bower@latest --allow-root
sudo npm install -g grunt-cli --force
sudo npm install grunt --force
sudo chown -R 1000:1000 "/home/shadek/.npm"
sudo rm /home/shadek/EssayIQ/client/node_modules/.bin/phantomjs
sudo rm -r /home/shadek/EssayIQ/client/node_modules/phantomjs/lib/phantom

sudo npm install phantomjs-prebuilt@2.1.7 --ignore-scripts (if you see phantom related error: npm ERR! phantomjs@2.1.7 install: `node install.js`)
sudo npm install phantomjs-prebuilt@2.1.7 -g --unsafe-perm
npm i -g phantomjs-prebuilt --unsafe-perm --silent

before bower install:
sudo chown -R shadek:shadek ~/.config
sudo chown -R shadek:shadek ~/.cache
bower install
grunt build --force

sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"
**delete ‘migrations' folder and delete all the rows from ‘alembic_version’ table (DELETE from alembic_version;). then run the followings inside server directory:**
python manage.py db init
python manage.py db migrate
python manage.py db upgrade

(then replace content of env.py with conceptvector/env.py)

Restart postgresql service if you change any settings like password or authentication method.
sudo ufw allow 5000

sudo ufw allow 9000
sudo ufw delete allow 'Nginx HTTP'

export APP_SETTINGS=config.DevelopmentConfig
export DATABASE_URL=postgresql://postgres:postgres@localhost/conceptvectorDB
sudo ufw allow 'Nginx HTTP'



