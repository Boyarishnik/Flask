create table if not exists mainmenu (
id integer primary key autoincrement,
title text not null,
url text not null
);
create table if not exists users (
id integer primary key autoincrement,
username text not null,
password text not null
);