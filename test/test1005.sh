#!/usr/bin/expect -f
set CONYX $env(CONYX)
set timeout 10
cd $CONYX
spawn ./tui.sh
expect "veda"
sleep 1
send "k"
expect "]=-"
sleep 1
send "23330"
send "\x07"
expect "veda"
sleep 1
send "q"
