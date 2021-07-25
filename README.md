# opticca
<h1>How to install and setup</h1>
- clone the repo to your machine
- In your project folder. Open the terminal and run:
    
   * python -m venv env

   * source env/bin/activate
   
   * pip install -r requirements.txt

- In your MySQL shell run the Following commands
  
  * create database OpticaDB character set utf8;

  * create user adminopt@localhost identified by 'opticcaDBpass';

  * GRANT ALL PRIVILEGES ON OpticaDB.* TO adminopt@localhost;

  * flush privileges;

  * exit
- In the .env file edit the values to match you database settings
- In the main project folder run:
  * python manage.py runserver
  
   
