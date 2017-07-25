# flask-vue-example
> The web project structure

## Build Setup api
```bash
# install python packages
pip install -r requirements.txt
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
