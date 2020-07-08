# flask-vue-example
> This a web development example.

This project includes api service, front-end and task service using
flask, vuejs, celery framework.

> 表名：dcos_cmdb.t_cmdb_server_basic_info

## Build Setup api
```bash
# install python packages
pip install -r requirements.txt
# init db
python manager.py db init
python manager.py db migrate
python manager.py db upgrade
# update db model
python manager.py db migrate
python manager.py db upgrade
# initial privileges
python manager.py init_privilege
# create superuser
python manager.py create_superuser
# run server
python manager.py runserver -h 127.0.0.1 -p 5000
```

## Build vue frontend
```bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build
```

## Run task server
```bash
celery -A celery_tasks.celery_ins worker --loglevel=info
```
