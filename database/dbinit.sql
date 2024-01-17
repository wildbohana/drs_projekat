--create schema drs_sema;
use drs_sema;

create table user
(
    email varchar(64) unique,
    password varchar(64) not null,
    firstName varchar(32) not null,
    lastName varchar(32) not null,
    address varchar(64) not null,
    city varchar(32) not null,
	state varchar(32) not null,
    phoneNumber varchar(16) not null,
    verified tinyint not null,
    accountNumber integer primary key AUTO_INCREMENT,    
    cardNumber varchar(16)
);

create table transaction
(
    id integer primary key AUTO_INCREMENT,
    sender varchar(64) not null,
    receiver varchar(64) not null,
    amount float(12, 2) not null,
    currency varchar(3) not null,
    state varchar(32) not null,
    product integer not null
);

create table credit_card
(
    cardNumber varchar(16) primary key,
    userName varchar(32) not null,
    expirationDate varchar(5) not null,
    cvv integer not null,
    amount float(12, 2) not null,
    bankAccountNumber varchar(10) not null,
	verified tinyint not null
);

create table product
(
    id integer primary key AUTO_INCREMENT,
    name varchar(128) not null,
    price float(12, 2) not null,
    currency varchar(3) not null,
    amount float(12, 2) not null
);

create table balance
(
    pk integer primary key AUTO_INCREMENT,
    accountNumber integer not null,
    amount float(12, 2) not null,
    currency varchar(3) not null
);


-- Korisnici
-- Sifra je 123 za sve
insert into user (email, password, firstName, lastName, address, city, state, phoneNumber, verified, cardNumber) values ("drs.projekat.tim12@gmail.com", "46a2add73e416df4e6addfef69ad96497705a00fde10eb0fecbb088eb9783822", "Admin", "Admin", "Bulevar Evrope 24", "Novi Sad", "Srbija", "123456789", 1, "1212121212121212");
insert into user (email, password, firstName, lastName, address, city, state, phoneNumber, verified, cardNumber) values ("bojana123@gmail.com", "46a2add73e416df4e6addfef69ad96497705a00fde10eb0fecbb088eb9783822", "Bojana", "Mihajlovic", "Marsala Tita 124", "Lajkovac", "Srbija", "123123123", 1, "9191919191919191");

-- Njihove kartice
insert into credit_card (cardNumber, userName, expirationDate, cvv, amount, bankAccountNumber, verified) values ("1212121212121212", "Admin", "01/30", 123, 50000, 1, 1);
insert into credit_card (cardNumber, userName, expirationDate, cvv, amount, bankAccountNumber, verified) values ("9191919191919191", "Bojana", "01/28", 911, 50000, 2, 1);

-- Balansi za korisnike
insert into balance (pk, accountNumber, amount, currency) values (1, 1, 10000, "RSD");
insert into balance (pk, accountNumber, amount, currency) values (2, 1, 143, "EUR");
insert into balance (pk, accountNumber, amount, currency) values (3, 2, 150, "RSD");
insert into balance (pk, accountNumber, amount, currency) values (4, 2, 200, "EUR");
insert into balance (pk, accountNumber, amount, currency) values (5, 2, 30, "USD");

-- Proizvodi
insert into product (id, name, price, currency, amount) values (1, "Solja PawPatrol", 400, "RSD", 40);
insert into product (id, name, price, currency, amount) values (2, "Redmi Buds 4", 30, "EUR", 20);
insert into product (id, name, price, currency, amount) values (3, "NZXT H9 Flow", 300, "USD", 10);
insert into product (id, name, price, currency, amount) values (4, "Auto na daljinski", 2000, "RSD", 20);

-- Kupovine
insert into transaction (id, sender, receiver, amount, currency, state, product) values (1, "bojana123@gmail.com", "drs.projekat.tim12@gmail.com", 2, "RSD", "Approved", 1);
insert into transaction (id, sender, receiver, amount, currency, state, product) values (2, "bojana123@gmail.com", "drs.projekat.tim12@gmail.com", 1, "EUR", "Denied", 3);
insert into transaction (id, sender, receiver, amount, currency, state, product) values (3, "bojana123@gmail.com", "drs.projekat.tim12@gmail.com", 2, "EUR", "Approved", 2);

-- Query za brisanje (user)
-- DELETE FROM `drs_sema`.`user` WHERE (`accountNumber` = '6');

-- Query za menjanje (kartica)
-- UPDATE `drs_sema`.`credit_card` SET `verified` = '0' WHERE (`cardNumber` = '9988776655443322');
