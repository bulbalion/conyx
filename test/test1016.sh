#!/usr/bin/expect -f
set CONYX $env(CONYX)
set timeout 10
cd $CONYX
spawn ./tui.sh
expect "veda"
sleep 1
send "l"
expect "]=-"
sleep 1
send "\x18"
expect "veda"
sleep 1
send "q"
