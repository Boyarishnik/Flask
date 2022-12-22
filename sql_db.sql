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
create table if not exists posts (
id integer primary key autoincrement,
title text not null,
text text not null,
url text not null,
username text not null,
time integer not null
);
create table if not exists news (
id integer primary key autoincrement,
title text not null,
text text not null,
url text not null,
date text not null
)