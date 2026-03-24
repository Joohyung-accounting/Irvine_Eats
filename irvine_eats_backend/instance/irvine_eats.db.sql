BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "hours" (
	"hours_id"	INTEGER,
	"restaurant_id"	INTEGER NOT NULL,
	"day"	INT NOT NULL,
	"open_time"	TIME NOT NULL,
	"close_time"	TIME NOT NULL,
	PRIMARY KEY("hours_id" AUTOINCREMENT),
	FOREIGN KEY("restaurant_id") REFERENCES "restaurants"("restaurant_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "menu" (
	"item_id"	INTEGER,
	"restaurant_id"	INTEGER NOT NULL,
	"item_name"	TEXT NOT NULL,
	"description"	TEXT,
	"price"	REAL,
	PRIMARY KEY("item_id" AUTOINCREMENT),
	FOREIGN KEY("restaurant_id") REFERENCES "restaurants"("restaurant_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "restaurants" (
	"restaurant_id"	INTEGER,
	"place_id"	TEXT NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"address"	TEXT,
	"hours"	TEXT,
	"category"	TEXT,
	"phone"	TEXT,
	"url"	TEXT,
	PRIMARY KEY("restaurant_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "reviews" (
	"review_id"	INTEGER,
	"user_id"	INTEGER NOT NULL,
	"restaurant_id"	INTEGER NOT NULL,
	"rating"	INTEGER CHECK("rating" >= 1 AND "rating" <= 5),
	"comment"	TEXT,
	PRIMARY KEY("review_id" AUTOINCREMENT),
	FOREIGN KEY("restaurant_id") REFERENCES "restaurants"("restaurant_id") ON DELETE CASCADE,
	FOREIGN KEY("user_id") REFERENCES "users"("user_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "users" (
	"user_id"	INTEGER,
	"id"	TEXT NOT NULL,
	"pw"	TEXT NOT NULL,
	"name"	TEXT NOT NULL,
	"email"	TEXT NOT NULL,
	PRIMARY KEY("user_id" AUTOINCREMENT)
);
INSERT INTO "users" VALUES (1,'joohyung','1234','Joohyung','joohyuo@uci.edu');
INSERT INTO "users" VALUES (2,'joohyung','1234','Joohyung','joohyuo@uci.edu');
COMMIT;
