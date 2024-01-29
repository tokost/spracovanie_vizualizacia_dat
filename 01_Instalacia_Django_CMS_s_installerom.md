>## Inštalácia Django CMS pomocou batch mode (dávkového režimu)

Inštalácia Djngo CMS pomocou batch mode je jednou s možnpostí ako nainštalovať Django CMS s minimálnou námahou. Tento postup patrí do do skupiny inštalácie pomocou [CMS Installera](https://djangocms-installer.readthedocs.io/en/latest/) ktorého popis najdete na príslušnom odkaze. Inštalátor **djangocms** vytvára kompletný a plne funkčný projekt django CMS, ktorý obsahuje nasledovné:

* vytvorí projekt
* nainštaluje požiadavky
* vytvára databázu
* (voliteľne) vytvorí vzorovú databázu
* (voliteľne) skopírujte poskytnutú sadu šablón
* zapíšte súbor požiadaviek do adresára projektu

**Inštalačný program djangocms** funguje ako dávkový skript a ako sprievodca príkazovým riadkom.

### Vlastná inštalácia v dávkovom režime (batch mode)

je predvolenou inštaláciou a obnáša minimálne požiadavky na užívateľa. V dávkovom režime inštalátor djangocms použije poskytnuté argumenty na vytvorenie a konfiguráciu projektu. Uplný zoznam odkazov na argumenty najdete [**tu**](https://djangocms-installer.readthedocs.io/en/latest/reference.html#arguments). **Pri vyvolaní inštalačného programu djangocms ** musíte vždy poskytnúť minimálne nasledujúci argument ktorým je meno vašeho projektu:
~~~
$ djangocms project_name
~~~
**project_name**: je názov projektu, ktorý sa má vytvoriť. Voliteľne môžete poskytnúť iný adresár projektu, ale potom sa v aktuálnom adresári vytvorí adresár pomenovaný podľa iného názvu projektu. 
**POZOR** adresár projektu dir je hlavný adresár projektu (ten, kde sa vytvorí**manage.py**)  V predvolenom nastavení inštalačný program skontroluje, či nie je tento adresár prázdny (bez skrytých súborov), aby sa zabezpečilo, že používate čisté prostredie. Ak chcete použiť neprázdny adresár, použite k v príkaze djangocms prízna **-s**.

Existujú aj ďalšie možnosti inštalácie ako napr. Wizard mode, Config file mode, Dump mode a Custom settings ktoré sú popísané [**tu**].

### Celý postup inštalácie v dávkovom režime

1./ Nastavte sa do adresára v ktorom chcete vytvoriť adresár projektu s menom **project_name** (napr. tutorial-project) Váš kmeňový adresár v ktorom to urobíme je PriezviskoM. Adresár projektu možeme vytvoriť v CLI:
~~~
$ cd project_name 
~~~
Ale môžeme na to použiť prieskumníka (Explorer) že na pravú myš zvolíme New -> Folder  (Novy -> Adresar)

* otvoriť adresár vo VS-Code
* otvorit terminál cez menu->view->terminal
* prejdeme do Git bash cez lištu terminálu na pravej strane šipka dole

2./ Vytvorte tu virtuálne prostredie:
~~~
$ python -m venv myvenv
~~~
3./ Aktivujte virtualne prostredie:
~~~
$. myvenv/scripts/activate
~~~
4./ [Stiahnite](https://pypi.org/project/djangocms-installer/) si a nainštalujte si djangocms-installer:
~~~
$ pip install djangocms-installer
~~~
alebo to môžete urobiť aj cez GitHub:
~~~
$ pip install https://github.com/nephila/djangocms-installer/archive/master.zip
~~~

5./ Spustite sprievodcu:
~~~
$ djangocms aplication_name
~~~
Ak nám to vzhodí chybu že nevie importovať nejakú knižnicu napr. pytz tak je to signal nainstalovať okrem tejto knižnice aj všetky ostatné uvedené v requirements.txt pomocou príkazu:
~~~
$ python -m pip install -r requirements.txt
~~~
 Poto znovu opakujeme príkaz **$ djangocms aplication_name**

6./ Odpovedzte ev. na zadané otázky ak sú položené a pokračujte ďalej na bod 7./

7./ Prejdite do adresára aplikácie:
~~~
cd application_name
~~~

8./ Ev. upravte poskytnuté nastavenia. Budete asi chcieť minimálne upraviť aspoň jazyk a nastavenia šablóny.

9./ Spustite projekt:
~~~
(virtualenv) $ python manage.py runserver
~~~

Hotovo!

Pokiaľ pri spustení projektu nastane takáto chyba:
~~~
...
ImportError: cannot import name 'ungettext' from 'django.utils.translation'
...
~~~
[Problém môžete vyriešiť](https://stackoverflow.com/questions/72572674/importerror-cannot-import-name-ugettext-lazy-from-django-utils-translation) znížením verzie django na 3.2, kým nebude správne podporovaná verzia 4.0. Je to však iba dočasné riešenie problému.
~~~
$ pip install django==3.2 
~~~
Často tiež treba urobiť aj migráciu ako nám to červeným oznámi VS-Code:
~~~
$ python manage.py runserver
~~~

Prihlásenie do bežiaceho Django CMS urobíme menom **admin** a heslom **admin**.

Po úspešnom prihlásení dostaneme nasledovný obrázok:
![](./obrazky/Django%20CMS.png)

#### Ak použite iný adresár šablón
Pomocou parametra môžete vytvoriť základný projekt s vlastnou sadou šablón **--templates**. Uvedomte si, že zatiaľ čo inštalačný program djangocms skopíruje súbory za vás, ale neaktualizuje parameter nastavenia v **CMS_TEMPLATES**, takže ho budete musieť po inštalácii upraviť.

#### Holá inštalácia
Voliteľne môžete nainštalovať iba Django a django CMS bez akéhokoľvek dodatočného pluginu pomocou možnosti **--no-plugins**. To vám umožní ďalšie prispôsobenie vašej inštalácie.


