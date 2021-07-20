create database OpticaDB character set utf8;

create user adminopt@localhost identified by 'opticcaDBpass';

GRANT ALL PRIVILEGES ON OpticaDB.* TO adminopt@localhost;

flush privileges;

exit