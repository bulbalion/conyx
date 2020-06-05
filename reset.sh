cp ./db/conyx.db ..
cp -R tmp ~/upload
rm -rf ./tmp
sqlite3 `pwd`/db/conyx.db << EOF
update auth set auth_key = 'CONFIRM YOUR IDENTITY FIRST';
update nick set nickname = '';
delete from last;
insert into last values (1);
delete from klub_cache;
delete from prispevek_cache;
delete from mail;
update config set value = '.' where key = 'soubory';
vacuum
EOF
rm -rf lib/*.pyc
rm -rf lib/.*
rm -rf .*.swp
find . | xargs touch
rm -rd lib/__pycache__/
rm profile_tui.txt
cp -R ./depana ..
rm -rf ./depana
./dist.sh
