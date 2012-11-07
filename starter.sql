BEGIN TRANSACTION;
CREATE TABLE association (
	author_id INTEGER, 
	book_id INTEGER, 
	FOREIGN KEY(author_id) REFERENCES authors (id), 
	FOREIGN KEY(book_id) REFERENCES books (id)
);
INSERT INTO association VALUES(1,1);
INSERT INTO association VALUES(1,4);
INSERT INTO association VALUES(3,2);
INSERT INTO association VALUES(3,4);
INSERT INTO association VALUES(2,3);
CREATE TABLE authors (
	id INTEGER NOT NULL, 
	name VARCHAR(50), 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
INSERT INTO authors VALUES(1,'Пушкин А.С.');
INSERT INTO authors VALUES(2,'Терри Пратчетт');
INSERT INTO authors VALUES(3,'Mark Lutz');
CREATE TABLE books (
	id INTEGER NOT NULL, 
	title VARCHAR(50), 
	PRIMARY KEY (id), 
	UNIQUE (title)
);
INSERT INTO books VALUES(1,'Евгений Онегин');
INSERT INTO books VALUES(2,'Learning Python');
INSERT INTO books VALUES(3,'Мор. Ученик Смерти');
INSERT INTO books VALUES(4,'One Book to Rule Them All');
COMMIT;
