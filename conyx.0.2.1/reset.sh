sqlite3 `pwd`/db/conyx.db << EOF
update auth set auth_key = 'CONFIRM YOUR IDENTITY FIRST';
update nick set nickname = '';
delete from last;
insert into last values (1);
delete from klub_cache;
delete from prispevek_cache;
delete from mail;
vacuum
EOF
rm -rf lib/*.pyc
rm -rf lib/.*
touch *
touch db/*
touch doc/*
touch lib/* 
rm -rd lib/__pycache__/
