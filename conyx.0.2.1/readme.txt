   ____ ___  _   ___   ____  __
  / ___/ _ \| \ | \ \ / /\ \/ /
 | |  | | | |  \| |\ V /  \  /
 | |__| |_| | |\  | | |   /  \
  \____\___/|_| \_| |_|  /_/\_\

       Console Nyx Client

Pro spusteni je nutne predem definovat systemovou promennou.

Napriklad takto:

export CONYX='/home/user/conyx'

Spravnost nastaveni muzeme overit napriklad takto:

[ echo $CONYX
/home/user/conyx

# AUTORIZACE

Nastavime aktualni adresar na $CONYX.

[ cd $CONYX

a spustime pomoci ./conyx.sh

Pote, co se poprvi klient spusti, tak se musi standardni cestou autorizovat.

# PRIKAZOVA RADKA

Conyx je na prikladech popsan takto (prikazy jsou oznaceny |->)

$ conyx

Nejdrive stahneme zahlavi klubu pro dalsi praci

|-> sk
[ KLUB: 532 ]
Stazeno 229 zahlavi klubu.

A potom si z cache zobrazime neprectene kluby

|-> np
[ KLUB: 532 ]
0|10425|3. světová válka aneb kam náš svět směřuje?  Status: SPACE FORCE|5|0
1|20020|3D tiskárny|1|0
10|18792|Android development|11|0
...
203|17068|tržiště / počítače a elektro|3|0
208|17123|tržiště / práce a služby - NABÍDKA (nabízím práci, hledám pracanty)|1|0
216|17877|Věci Veřejné - StB sledovalo hlavně to, jestli někdo nepodepisuje nevýhodné kontakty|61|0
|->

Anebo kluby s reakcemi pro tebe

|-> r
[ KLUB: 532 ]
532|Brno - Šalingrad ... xchat - Tady jde o šedesátosm okupantů.|1|1

Zobrazi se pouze kluby, ve kterych mas reakci.

|-> klub 5184
Zvolen klub: 5184

|-> cti
Ctu klub 5184
XXXX|kdyz se tady resi ty joysticky, nasel jsem doma 2x original didakti
...
...
XXXX|Zemřel Rick Dickinson, designér ZX Spectra - Root.cz
https://www.root.cz/zpravicky/zemrel-rick-dickinson-designer-zx-spectra/
XXXX|CH_IN_A: Zrovna sem s tim jdu.
R.I.P. Rick.

|-> pis to je mi lito. je to dobre navrzeny stroj
prispevek zaslan

# TEXTOVY UZIVATELSKY INTERFACE

pokud na prikazove radce zadame prikaz:

|-> tui

provede se pokus o inicializaci textoveho uzivatelskeho rozhrani

V nem lze pomoci stisku klaves provadet nasledujci operace

(k)lub - vyber klubu
(c)ti - cti prispevky ve vybranem klubu
(p)is - posli prispevek do vybraneho klubu
(s)ledovaneho - nove prispevky ve sledovanych klubech
(z)meny - posledni zmeny v CONYXu

Prijemnou zabavu s CONYXem
