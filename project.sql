create database project;
use project;

create table LogIn(
USER_NAME varchar(100),
PASS varchar(8),
ROOM_NUMBER int,
primary key(USER_NAME,ROOM_NUMBER),
foreign key(ROOM_NUMBER) references register(room_no)
);

create table register(
user_name varchar(100),
pass varchar(8),
namee varchar(30),
mail varchar(255) not null,
room_no int primary key
);

delete from complaints where room_number=1;
delete from register where room_no=1;
select*from register;
select* from complaints;

update register 
set pass="4567" where room_no=0;
SHOW TRIGGERS LIKE 'register';


insert into register values("Admin","3458","Shiva Raj","shivarajgurajala@gmail.com",0);

create table complaints(
ROOM_NUMBER int,
PROBLEM varchar(20)
);
drop table complaints;

create table menu(
items varchar(20)
);

create table orders(
room_no int,
items varchar(20)
);

DELIMITER $$
create trigger tri
after insert on register
for each row
begin
insert into LogIn values(NEW.user_name,NEW.pass,NEW.room_no);
END$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER tri_update
AFTER UPDATE ON register
FOR EACH ROW
BEGIN
  UPDATE LogIn
  SET USER_NAME = NEW.user_name,
      PASS = NEW.pass,
      ROOM_NUMBER = NEW.room_no
  WHERE USER_NAME = OLD.user_name
    AND ROOM_NUMBER = OLD.room_no;
END$$
DELIMITER ;

show full processlist;
kill 686;
check table complaints;