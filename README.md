# LeafLink API
This is an test API to represent LeafLink's database. To run the API follow these steps:

## Step 1: Installation
You should install virtualenv
```
pip install virtualenv
```
After installing virtualenv create a virtual environment inside the project folder
```
virtualenv venv
```
This will create a folder call `venv`. To activate the virtual environment activate it in the terminal like so:
```
source venv/bin/activate
```
Now that you're in your env install the dependencies by pip installing
```
pip install -Ur requirements.txt
```

## Step 2: Create the DB
Now that dependencies are installed, you must create the database (SQLite). Our `manage.py` has all the commands we need to run our project. To creat the DB we execute
```
python manage.py create_db
```
After the SQL has been execute we can now run the project.

## Step 3: Run the server!
To run the server it's a similar to creating the DB. Execute the command below:
```
python manage.py runserver
```

## Testing FTW

To run the tests it's just as simple as the other commands
```
python manage.py test
```
All the test files can be found in the `tests` folder.


## Example calls
For creating a company, you can do a CURL POST request like such
```
curl -d "name=Company1&description=First%20Company&company_type=buyer" localhost:5000/companies
```

To get all companies we can do a curl GET request as such
```
curl localhost:5000/companies
```