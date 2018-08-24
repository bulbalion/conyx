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

Prompt by mel vypadat takto:

[ ./conyx.sh # (pokud je spravne nastaven alias z popisu instalace, tak staci jenom conyx)
Jsem pripojen...
[ KLUB: -1 ]
|->

Conyx je na prikladech popsan takto (prikazy jsou oznaceny |->)

|-> diskuze ZX
5184|ZX Spectrum - gumak a plusko, nostalgie, emulatory, gameseni :o))))
pouzit filter diskuzi ZX

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
