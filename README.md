# SweetSpot
# run commmands
# venv\Scripts\activate

# python manage.py makemigrations
# python manage.py migrate 
# python manage.py runserver

<!-- CREATE DATABASE sweetspot_db;
CREATE USER sweetspot_user WITH PASSWORD 'your_password';
ALTER ROLE sweetspot_user SET client_encoding TO 'utf8';
ALTER ROLE sweetspot_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE sweetspot_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE sweetspot_db TO sweetspot_user;
 GRANT ALL PRIVILEGES ON SCHEMA public TO sweetspot_user;
ALTER USER sweetspot_user SET search_path TO public;

-->

<!-- git add .
git commit -m "done with order api with cake id in cart "
git push origin main
 -->
# View Customers:
# SELECT * FROM sweetspot_app_customer;

# View Cakes:
# SELECT * FROM sweetspot_app_cake;

# View Cake Customizations:
# SELECT * FROM sweetspot_app_cakecustomization;

# View Carts:
# SELECT * FROM sweetspot_app_cart;

# View Orders:
# SELECT * FROM sweetspot_app_order;
