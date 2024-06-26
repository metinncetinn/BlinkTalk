create database db_SoruCevap
use db_SoruCevap

select * from tblSorular
select * from tblCevaplar
select * from tblSoruCevap
select * from tblOzel

delete from tblSoruCevap where soruId=10
delete from tblCevaplar where id=12
delete from tblSorular where id=10

create table tblSorular(
id int primary key identity(1,1),
soru varchar(200) 
)

create table tblCevaplar(
id int primary key identity(1,1),
cevap varchar(200)
)

create table tblOzel(
id int primary key identity(1,1),
soruId int foreign key references tblsorular(id),
cevapId int foreign key references tblcevaplar(id),
)

create table tblSoruCevap(
soruId int foreign key references tblsorular(id),
cevapId int foreign key references tblcevaplar(id),
kullanimSayisi int default 1
)
--Daha farklı sorular da eklenebilir.
insert into tblSorular values('where are you from')
insert into tblSorular values('what is your name')
insert into tblSorular values('how old are you')
insert into tblSorular values('hi')
insert into tblSorular values('hello')

insert into tblCevaplar values('I am from Konya')
insert into tblCevaplar values('My name is Metin')
insert into tblCevaplar values('I am 22 years old')
insert into tblCevaplar values('hi')
insert into tblCevaplar values('Hello')

--Sorulara karşılık cevap ekleme
INSERT INTO tblSoruCevap (soruId, cevapId)
VALUES (
    (SELECT id FROM tblSorular WHERE tblSorular.id=5),
    (SELECT id FROM tblCevaplar WHERE tblCevaplar.id=4)
);
--Ozel bilgiler ekleme.
INSERT INTO tblOzel(soruId, cevapId)
VALUES (
    (SELECT id FROM tblSorular WHERE tblSorular.id=3),
    (SELECT id FROM tblCevaplar WHERE tblCevaplar.id=3)
);

/*
SELECT cevap FROM tblOzel 
inner join tblCevaplar on tblCevaplar.id=tblOzel.cevapId
inner join tblSorular on tblSorular.id=tblOzel.soruId
WHERE soru='how old are you'


select tblSoruCevap.soruId from tblSoruCevap inner join
tblSorular on tblSorular.id=tblSoruCevap.soruId
where soru='hi'

select kullanimSayisi from tblSoruCevap where soruId=(select top 1 tblSoruCevap.soruId from tblSoruCevap inner join
tblSorular on tblSorular.id=tblSoruCevap.soruId
where soru='Hi')

select tblSoruCevap.soruId,tblSoruCevap.cevapId  from tblSoruCevap
inner join tblSorular on tblSorular.id=tblSoruCevap.soruId
inner join tblCevaplar on tblCevaplar.id=tblSoruCevap.cevapId where  soru='Hi' and cevap='Hello'

select tblCevaplar.cevap from tblSoruCevap
inner join tblCevaplar on tblCevaplar.id=tblSoruCevap.cevapId
where kullanimSayisi= (select top 2 tblSoruCevap.kullanimSayisi from tblSoruCevap inner join tblSorular on tblSorular.id=tblSoruCevap.soruId where soru='hello' order by kullanimSayisi desc)


select kullanimSayisi from tblSoruCevap where soruId=(select top 1 tblSoruCevap.soruId from tblSoruCevap
inner join tblSorular on tblSorular.id=tblSoruCevap.soruId where soru='Hi') and cevapId=(select top 1  tblSoruCevap.cevapId from tblSoruCevap
inner join tblCevaplar on tblCevaplar.id=tblSoruCevap.cevapId where cevap='Hello')

select count(soruId) from tblSoruCevap where soruId=(select id from tblSorular where soru='Hi')

select id from tblSorular where soru='Hi'
select id from tblCevaplar where cevap='Hi'
select kullanimSayisi from tblSoruCevap where cevapId=(select id from tblCevaplar where cevap='Hi') and soruId=(select id from tblSorular where soru='Hi')



select top 2 tblCevaplar.cevap from tblSoruCevap inner join tblCevaplar on tblCevaplar.id=tblSoruCevap.cevapId inner join tblSorular on tblSorular.id=tblSoruCevap.soruId where soru='hello' ORDER BY kullanimSayisi DESC
*/
