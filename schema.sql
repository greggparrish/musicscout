-- Schema for musicscout

-- Sources are media providers that work with youtube-dl
create table source (
    id              integer primary key autoincrement not null,
    name            string,
);

-- Pending, retrieved, error
create table status (
    id              integer primary key autoincrement not null,
    name            string,
);

-- Feeds are individual URLS we want to check for media
create table feed (
    id              integer primary key autoincrement not null,
    url             string,
    last_checked    date
);

-- Tasks are steps that can be taken to complete a project
create table song (
    id           integer primary key autoincrement not null,
    status       integer not null references status(id)
    found        date,
    downloaded   date,
    source      integer not null references source(id),
    feed        integer not null references feed(id)
);
