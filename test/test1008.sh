#!/usr/bin/expect -f
set CONYX $env(CONYX)
set timeout 10
cd $CONYX
spawn ./tui.sh
expect "veda"
sleep 1
send "z"
expect "]=-"
sleep 1
send "q"
expect "veda"
sleep 1
send "q"
