# Another Vintage Co. website

## Premise

Another Vintage Co.  is a web based vintage and second hand clothing company that sells clothes based on a 1 time product model, where once the product has been sold it will likely never be restocked due to the nature of how the company acquires stock

## For development

- All User Authentication code is handled in login.py.

- All other pages are handled in views.py.

- Until Models are implemented the db can be accessed by calling dbconn() in views which will generate a PyMongo client that you can use to interact with the database.

- Header.html is to be used on top of any templates that the user can access.

- The dockercompose will currently only start the database however the web server can easily be containerised by adding this code but this is not yet configured fully yet:
```
web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/code
    ports:
      - "8000:8000"
```
- A .venv has been included in the zip for ease but will not be available on the github

### Should you want to run the website to have a look you can do it like so:
1. start the docker-compose
2. mongosh into the database -u root -p rootpassword (temporary for development)
3. Run these commands
```
use AnotherVintage
db.createCollection("orders")
db.createCollection("stock")
db.stock.insertOne({"_id":1,"name":"Blanche Sporting Goods tshirt","brand":"Lee","size":"L","colour":"grey",
"bought_at":2.5,"price":7.5,"status":"sold","stocked_at":new Date()})

db.stock.insertOne({"_id":33,"name":"Calvin tshirt","brand":"Calvin Klein","size":"XL","colour":"black",
"bought_at":2.5,"price":10,"status":"stocked","stocked_at":new Date()})
db.stock.insertOne({"_id":7,"name":"Notre Dame Fighting Irish tshirt","brand":"Adidas","size":"L","colour":"green",
"bought_at":2.5,"price":7.5,"status":"stocked","stocked_at":new Date()})
db.stock.insertOne({"_id":24,"name":"Enjoy Coke tshirt","brand":"Coca Cola","size":"M","colour":"red",
"bought_at":2.5,"price":10,"status":"stocked","stocked_at":new Date()})
db.stock.insertOne({"_id":46,"name":"Muhammed Ali tshirt","brand":"Adidas","size":"S","colour":"black",
"bought_at":2.5,"price":10,"status":"stocked","stocked_at":new Date()})
db.stock.insertOne({"_id":27,"name":"Hard Rock Cafe Athens tshirt","brand":"Hard Rock Cafe","size":"XL","colour":"blue",
"bought_at":2.5,"price":10,"status":"stocked","stocked_at":new Date()})
```
This will allow basic user usage of the website

### For accessing stock control

1. Once the website is up either login to the pre existing admin -u admin -p adminpass or create a new super user with ```python manage.py createsuperuser```
2. Login to the admin account create a group called controller and a user that will you can assign to this group

3. Login to that account and view stock control pages