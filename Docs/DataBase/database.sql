CREATE DATABASE Project;
use Project;
CREATE TABLE "user_profile_user" (
	"id"	integer NOT NULL,
	"last_login"	datetime,
	"username"	varchar(25) NOT NULL UNIQUE,
	"password"	varchar(25) NOT NULL,
	"firstname"	varchar(30) NOT NULL,
	"lastname"	varchar(30) NOT NULL,
	"patronymic"	varchar(30) NOT NULL,
	"email"	varchar(30) NOT NULL UNIQUE,
	"registration"	datetime NOT NULL,
	"is_active"	bool NOT NULL,
	"is_admin"	bool NOT NULL,
	"country"	varchar(30) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "posts_post" (
	"id"	integer NOT NULL,
	"text"	varchar(300) NOT NULL,
	"created_date"	datetime NOT NULL,
	"is_active"	bool NOT NULL,
	"is_favourite"	bool NOT NULL,
	"user_id"	bigint NOT NULL,
	FOREIGN KEY("user_id") REFERENCES "user_profile_user"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "posts_hashtag_post" (
	"id"	integer NOT NULL,
	"hashtag_id"	bigint NOT NULL,
	"post_id"	bigint NOT NULL,
	FOREIGN KEY("hashtag_id") REFERENCES "posts_hashtag"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("post_id") REFERENCES "posts_post"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "posts_hashtag" (
	"id"	integer NOT NULL,
	"name"	varchar(100) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);