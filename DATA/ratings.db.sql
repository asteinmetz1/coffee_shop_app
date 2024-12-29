BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "coffee_shops" (
	"shop_id"	INTEGER,
	"name"	TEXT,
	"location"	TEXT,
	PRIMARY KEY("shop_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ratings" (
	"rating_id"	INTEGER,
	"user_id"	INTEGER,
	"shop_id"	INTEGER,
	"coffee_rating"	INTEGER,
	"price_rating"	INTEGER,
	"food_rating"	INTEGER,
	"vibe_rating"	INTEGER,
	"convenience_rating"	INTEGER,
	PRIMARY KEY("rating_id" AUTOINCREMENT),
	FOREIGN KEY("shop_id") REFERENCES "coffee_shops"("shop_id"),
	FOREIGN KEY("user_id") REFERENCES "users"("user_id")
);
CREATE TABLE IF NOT EXISTS "users" (
	"user_id"	INTEGER,
	"username"	TEXT UNIQUE,
	"password"	TEXT,
	PRIMARY KEY("user_id" AUTOINCREMENT)
);
INSERT INTO "coffee_shops" VALUES (11,'Canary Coffee','Downtown');
INSERT INTO "coffee_shops" VALUES (12,'Anodyne','Walkers Point');
INSERT INTO "coffee_shops" VALUES (13,'Test Shop','Test Location');
INSERT INTO "ratings" VALUES (7,9,NULL,6,8,3,4,10);
INSERT INTO "ratings" VALUES (8,9,12,9,8,4,10,6);
INSERT INTO "ratings" VALUES (9,9,11,5,5,5,5,5);
INSERT INTO "users" VALUES (9,'Austin',X'243262243132244e446a467966627142356644376546646a6b657a442e732f763834745a504c54654c5435772f6f4c42732e58663076337531374275');
COMMIT;
