# django_hockey_shop

# To check the deployment result:
- https://django-hockey-shop-proj.ru 

## About project:
This is an e-commerce web application for online sales of hockey equipment. It features the ability to add products through 
the admin panel, register as a buyer, register using a GitHub account, sending email verification, add products to the shopping cart, add products to favorites, search for products by name or description, place orders for selected products, and make payments.

### Stack:
- Python 
- Django
- DRF
- PostgreSQL
- Redis
- Celery
- Stripe API
- HTML
- CSS
- Bootstrap
- Deploy with VDS server (NGINX, Gunicorn)

### Local Developing

All actions should be executed from the source directory of the project and only after installing all requirements.

1. Firstly, create and activate a new virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```
2. Install packages:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
3. Run project dependencies, migrations, fill the database with the fixture data etc.:
```
./manage.py migrate
./manage.py loaddata <path_to_fixture_files>
./manage.py runserver 
```
4. Run [Redis Server](https://redis.io/docs/getting-started/installation/)
```bash
redis-server
```
or
```bash
brew services start redis
```
5.Run Celery:
```bash
celery -A store worker --loglevel=INFO
```

