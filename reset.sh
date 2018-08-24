sqlite3 `pwd`/db/conyx.db << EOF
update auth set auth_key = 'CONFIRM YOUR IDENTITY FIRST';
update nick set nickname = '';
delete from last;
insert into last values (1);
EOF
rm -rf lib/*.pyc
rm -rf lib/.*
touch -r *
touch *; touch db/* touch doc/* touch lib/*
