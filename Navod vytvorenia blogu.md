>## Vytvorenie webovej aplikácie blogu
https://tutorial.djangogirls.org/en/ 

![](/obrazky/djangogirls01.png)

>### Inštalácia a príprava

1. Pre túto aplikáciu vytvoríme pomocou prieskumníka nový adresár **djangogirls** z vášho domovského adresára.
2. Vytvoríme virtuálne prostredie s názvom **myvenv** pomocou príkazu **$ python -m venv myvenv** v termináli Git Bash VS-Code
3. Aktivujeme virtualne prostredie príkazom **$ . myvenv/scripts/activate**
4. Nainštalujeme Django
    a. najprv aktualizujeme inštalačný program pythonu pip príkazom **$ python -m pip install --upgrade pip**
    b. potom nainštalizujeme programové knižice a balíky
        1. vytvoríme si súbor requirements.txt vo VS-Code
        2. zapíšeme do neho názov a verziu inštalovaného balíka **Django~=3.2.10**
        náš adresárový strom teraz bude vyzerať takto:
        
        DJANGOGIRLS
        │
        ├── myvenv
        │   └── ...
        └───requirements.txt

        3. Spustite inštaláciu Django príkazom **$ pip install -r requirements.txt**.
5. Vytvoríme adresár našej aplikácie príkazom **django-admin.exe startproject mysite .** a dostaneme novú adresárovú štruktúru:

DJANGOGIRLS
│
├── manage.py
├── mysite
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── myvenv
│   └── ...
└── requirements.txt

6. Vykonáme zmeny v nastavení v súbore settings.py
   1. nájdeme riadok, ktorý obsahuje TIME_ZONE, a upravíme ho tak, aby sme si vybrali svoje vlastné časové pásmo napr. TIME_ZONE = 'Europe/Berlin'
   2. ak chcete iný jazyk, zmeňte kód jazyka zmenou nasledujúceho riadku LANGUAGE_CODE = 'sk-sk'
   3. budeme tiež musieť pridať cestu pre statické súbory pod STATIC_URL vložíme STATIC_ROOT
   ~~~
    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR / 'static'
    ~~~

7. keď DEBUGje True a ALLOWED_HOSTS je prázdne, hostiteľ je overený voči ['localhost', '127.0.0.1', '[::1]']. Po nasadení našej aplikácie na PythonAnywhere sa to ale nebude zhodovať s naším názvom hostiteľa, takže zmeníme nasledujúce nastavenie na :
~~~
ALLOWED_HOSTS = ['127.0.0.1', '.pythonanywhere.com']
~~~
8. Nastavenie databázy. Keďže použijeme predvolenú databázu SQLlite3 nemusíme pri tejto položke nič meniť a dopĺňať.
9. Ak chcete vytvoriť databázu pre náš blog, spustite v konzole nasledovné: **python manage.py migrate** (pritom musíme byť v adresári djangogirls, ktorý obsahuje súbor manage.py). Ak to pôjde dobre, mali by ste vidieť niečo takéto:
~~~
(myvenv) ~/djangogirls$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK
~~~
Máme hotovo! Je čas spustiť webový server a zistiť, či náš web funguje!
10. Spustenie webového servera. Musíte byť v adresári, ktorý obsahuje súbor manage.py(adresár djangogirls) a napíšeme **$ python manage.py runserver cislo_portu**

>### Modely Django

To, čo chceme teraz vytvoriť, je niečo, čo bude uchovávať všetky príspevky v našom blogu. Aby sme to však dokázali, musíme sa zoznámiť s vecami ktoré súvisia s pojmom **objects**.

### Objekty

V programovaní existuje koncept s názvom object-oriented programming. Myšlienka je taká, že namiesto toho, aby sme všetko písali ako nudnú sekvenciu programovacích inštrukcií, môžeme veci modelovať a definovať, ako sa navzájom ovplyvňujú.

Čo je teda **objekt**? Je to **súbor vlastností a akcií**. Znie to zvláštne, ale uvedieme príklad.

Ak chceme modelovať mačku, vytvoríme objekt ***Cat***, ktorý má nejaké vlastnosti ako color, age, mood (nálada: dobrá, zlá alebo ospalá) a ***owner*** (ktorý by mohol byť priradený objektu ***Person*** – resp. v prípade zatúlania mačky, by táto vlastnosť bola prázdna).

Potom nad objektom Cat možno registrovať niekoľko aktivít - akcií: purr (pradie), scratch (škrábe), alebo feed (žerie) (v takom prípade dáme mačke nejaké CatFood (mačacie žrádlo), čo môže byť samostatný objekt s vlastnosťami, napríklad taste (chuť)).
~~~
Cat
--------
color
age
mood
owner
purr()
scratch()
feed(cat_food)
~~~
~~~
CatFood
--------
taste
~~~

Takže v podstate ide o opísanie skutočných vecí v pragramovom kóde s vlastnosťami (nazývanými **object properties**) a akciami (nazývanými **methods**).

Ako potom budeme modelovať blogové príspevky? Chceme si totiž vytvoriť vytvoriť aplikáciu na písanie a komentovanie blogu.

Preto si musíme odpovedať na otázku: Čo je to blogový príspevok? Aké vlastnosti by mal mať?

Náš blogový príspevok určite bude obsahovať nejaký text s obsahom a názvom. Bolo by tiež dobré vedieť, kto to napísal – takže potrebujeme autora. Nakoniec chceme vedieť aj to, kedy bol príspevok vytvorený a publikovaný t.j. vložený na web. Jeho vlastnosti potom možno zhrnúť takto:
~~~
Post
--------
title
text
author
created_date
published_date
~~~

Ešte však potrebujeme vedieť aké veci resp. činnosti (metódy) by sa mali robiť s blogovým príspevkom. Bolo by dobré mať niekoho method (funkcii), ako napr. kto uverejní príspevok a pod.
Za týmto účelom budeme teda potrebovať metódu ktorú nazveme **publish**. Keďže už vieme, čo chceme dosiahnuť, začnime to modelovať v Django!

### Model Django

Keď vieme, čo je objekt, môžeme vytvoriť  model Djanga pre náš blogový príspevok.

[**Model**](https://docs.djangoproject.com/en/5.0/topics/db/models/) v Django **je špeciálny druh objektu** – ktorý je uložený v database vo forme samostatnej tabuľky. Aj tento model si môžeme predstaviť ako tabuľku so stĺpcami (poliami) a riadkami (údajmi). Pre model v OOP ktorý je jediný zdroj informácií o našich údajoch je charakteristické to že **obsahuje nielen základné polia o vlastnostiach objektov** ale aj **údaje o ich správaní**. Každý model je trieda Pythonu, ktorá má svoje podtriedy **django.db.models.Model**.

Ako vieme Databáza je súbor údajov a teda miesto, kde budeme ukladať informácie o používateľoch, príspevky na blogu a pod. V tejto aplikácii na ukladanie údajov budeme používať databázu SQLite ktorá je predvoleným databázový adaptérom aj pre Django.

### Vytvorenie aplikácie

Aby sme mali vo všetkom poriadok, vytvoríme v našom projekte **djangogirls** samostatnú aplikáciu s názvom **blog**. Na vytvorenie tejto aplikácie musíme v konzole Git Bash spustiť nasledujúci príkaz (z adresára djangogirls, kde je súbor manage.py):
~~~
$ python manage.py startapp blog
~~~
Tým sa vytvoril nový adresár **blog** ktorý obsahuje množstvo súborov. Adresáre a súbory v našom projekte by mali potom vyzerať takto:
~~~
DJANGOGIRLS
│
├── blog
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── db.sqlite3
├── manage.py
├── mysite
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── myvenv
│   └── ...
└── requirements.txt
~~~
Keď  vytvoríme adresár novej aplikácie musíme to tiež povedať Djangovi aby ju mohol použiť. Urobíme to v súbore mysite/settings.py. Musíme v ňom nájsť čast INSTALLED_APPSa pridať riadok obsahujúci 'blog',tesne nad ]. Takže konečný produkt by mal vyzerať takto:
~~~
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
]
~~~

### Vytvorenie modelu blogového príspevku

To čo sme si vyššie spomenuli, teraz budeme aplikovať v praxi a tým si doplníme predstavu o modeloch Djanga.
Začneme tým že v súbore blog/models.py definujeme všetky používané objekty **Models** – toto je miesto, v ktorom budeme definovať náš blogový príspevok.

Otvoríme vo VS-Code súbor blog/models.py, všetko z neho odstránime a napíšeme tam tento kód:
~~~
from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
~~~
Poznámka: Skontrolujte, či na každej strane str používame dva znaky podčiarknutia ( _) . Táto konvencia sa v Pythone často používa a niekedy ju nazývame aj „dunder“ (skratka pre „double-underscore“).

#### V ďalšom vysvetlíme čo tieto riadky znamenajú

Všetky riadky začínajúce na **from** alebo **import** sú riadkami, ktoré pridávajú nejaké kódy z iných súborov. Takže namiesto kopírovania a vkladania kódov ktoré sa opakujú do iných súborov môžeme niektoré časti zahrnúť do príkazového riadku **from ... import ...**
~~~
class Post(models.Model):– tento riadok definuje náš model (je to object).
~~~
* **class** je špeciálne kľúčové slovo, ktoré označuje, že definujeme objekt.
* **Post** je názov nášho modelu. Môžeme mu dať iný názov (musíme sa však vyhnúť špeciálnym znakom a medzerám). Názov triedy vždy začínajte veľkým písmenom.
* **models.Model** znamená, že príspevok je model Django, takže Django vie, že by sa mal uložiť do databázy.

Teraz definujeme vlastnosti, o ktorých sme hovorili: title, text, created_date, published_date a author. Aby sme to dosiahli, musíme definovať typ každého poľa (Je to text? Číslo? Dátum? Vzťah k inému objektu, napríklad k Používateľovi ?)

* **models.CharField** – takto definujete text s obmedzeným počtom znakov.
* **models.TextField** – toto je pre dlhý text bez obmedzenia. Je to vhodné na to aby sme neobmedzovali obsah blogových príspevkov.
* **models.DateTimeField** – toto je dátum a čas.
* **models.ForeignKey** – toto je odkaz na iný model.

Nebudeme tu vysvetľovať každý kúsok kódu, pretože by to zabralo príliš veľa času. Pokiaľ by vás to však z nejakého dôvodu ale zaujímalo môžete sa pozrieť na dokumentáciu Django, ak sa chcete napr. dozvedieť viac o poliach modelu a o tom, ako definovať aj ine veci ako sme spomínali vyššie ( https://docs.djangoproject.com/en/3.2/ref/models/fields/#field ).

Čo sa týka metódy na publikovanie môžeme použiť **def publish(self)**. Je to presne tá metóda **publish** o ktorej sme hovorili predtým. def znamená, že ide o funkciu/metódu a **publish** je názov metódy.

**Pravidlom** pre pomenovanie funkcie(metody) je, že namiesto medzier používame malé písmená a podčiarkovníky. Napríklad metóda, ktorá vypočíta priemernú cenu, sa môže nazývať calculate_average_price.

Metódy často niečo vrátia (**return**). V našej metóde je to aj prípad __str__. V tomto scenári totiž keď zavoláme __str__() chceme dostať text ( reťazec ) s názvom príspevku.

Všimnite si tiež, že obidve funkcie **def publish(self)** a **def __str__(self)** sú odsadené v našej triede. Je to preto, lebo **Python je citlivý na medzery** a tak musíme v triede naše metódy odsadiť. V opačnom prípade metódy nebudú patriť do triedy a môžeme získať neočakávané správanie.

### Vytvoríme tabuľky pre modely v databáze

Posledným krokom je pridanie nášho nového modelu do našej databázy.  Najprv však musíme dať Djangovi vedieť, že máme nejaké zmeny v našom modeli models.py, ktorý sme práve vytvorili. Prejdime preto do okna konzoly a napíšte **python manage.py makemigrations blog**. Oznam vo forme príkazu bude vyzerať takto:
~~~
(myvenv) ~/djangogirls$ python manage.py makemigrations blog
Migrations for 'blog':
  blog/migrations/0001_initial.py
    - Create model Post
~~~

**Poznámka**: Nezabudnite vždy uložiť súbory, ktoré upravujete. V opačnom prípade váš počítač spustí predchádzajúcu verziu, ktorá vám môže poskytnúť neočakávané chybové hlásenia.

Na základe vyššieho príkazu Django pre nás pripravil migračný súbor 0001_initial.py, ktorý teraz musíme použiť na vlastnú migráciu v našej databáze. Urobíme to príkazom **python manage.py migrate blog** a výstup by mal byť nasledovný:
~~~
(myvenv) ~/djangogirls$ python manage.py migrate blog
Operations to perform:
  Apply all migrations: blog
Running migrations:
  Applying blog.0001_initial... OK
~~~

Náš Post model je teraz v našej databáze db.sqlite3 ako tabuľka  blog_post a možeme si jej štruktúru pozrieť cez SQLite Viewer. Ešte by bolo dobré vidieť aj to ako vyzerá náš príspevok, ale to uvidíme aź nižśie.

### admin Django

Ak chcete pridať, upraviť a odstrániť príspevky, ktoré sme práve vymodelovali, použijeme na to správcu - administrátora Djanga.

Otvorme preto súbor blog/admin.py a nahraďme jeho obsah týmto kedy použijeme avizovanú konštrukciu from ... import ...:
~~~
from django.contrib import admin
from .models import Post

admin.site.register(Post)
~~~

Ako uvidíme, importujeme (zahrnieme) Post model definovaný v predchádzajúcej kapitole. Aby bol náš model viditeľný na stránke správcu, musíme ho zaregistrovať u **admin.site.register(Post)**.

Už je čas pozrieť sa na náš Post model. Nezabudnite na konzole spustiť **$ python manage.py runserverv cislo_portu**, aby sme spustili webový server. Prejdite do prehliadača a zadajte adresu http://127.0.0.1:cislo_portu/admin/ . Zobrazí sa nám prihlasovacia stránka, ktorá vyzerá takto:

![](/obrazky/djangogirls02.png)

Pre prihlásenie je potrebné vytvoriť superužívateľa, ktorý má kontrolu nad všetkým na stránke. Prerušme chod web servera CTRL-C a vráťme sa na príkazový riadok terminálu kde nápíšeme, **python manage.py createsuperuser** a vyplníme požadované údaje.

**POZOR**: Nezabudnite, že ak chceme písať nové príkazy, kým je webový server spustený je potrebné jeho činnosť ukončiť.
~~~
(myvenv) C:\Users\Name\djangogirls> python manage.py createsuperuser
~~~
Po zobrazení výzvy zadajte svoje používateľské meno (malé písmená, bez medzier), e-mailovú adresu a heslo. Nebojte sa, že nevidíte heslo, ktoré zadávate – tak to má byť. Zadajte ho a stlačením tlačidla enter pokračujte. Výstup by mal vyzerať takto (kde používateľské meno a e-mail by mali byť vaše vlastné):
~~~
Username: admin
Email address: info@comto.sk
Password: admin
Password (again): admin
Superuser created successfully.
~~~

Potom sa vráťte do prehliadača. Prihláste sa pomocou poverení superužívateľa, ktoré ste si vybrali. Mali by ste vidieť Django admin dashboard.
![](/obrazky/djangogirls03.png)

Prejdime na Post (príspevky) a trochu s nimi poexperimentujme. Pridajtme päť alebo šesť blogových príspevkov. Nerobte si pri tom starosti s ich obsahom – je viditeľný iba pre vás na lokálnom počítači. Aby ste ušetrili čas môžete aj skopírovať a prilepiť nejaký text z tohto návodu.

Uistite sa, že aspoň dva alebo tri príspevky (ale nie všetky) majú nastavený dátum zverejnenia - publikovania. Neskôr to budeme potrebovať.

![](/obrazky/djangogirls04.png)

Ak sa chcete dozvedieť viac o Django adminovi, mali by ste si pozrieť dokumentáciu Django: https://docs.djangoproject.com/en/3.2/ref/contrib/admin/

### Nasadenie do produkcie

Nasadenie do produkcie je dôležitou súčasťou procesu vývoja webových stránok. Táto kapitola je umiestnená v strede návodu a vyžaduje určitú námahu naviac ktorú si môžeme aj odpustiť a teda túto kapitolu preskočiť viď. https://tutorial.djangogirls.org/en/deploy/ 

### Django URL

Pokračujeme vo vývoji našej webovej aplikácie blogu. Najprv sa však musíme niečo dozvedieť o adresách URL Django.

#### Čo je to adresa URL?

URL je webová adresa. Adresu URL môžete vidieť pri každej návšteve webovej stránky – je viditeľná v paneli s adresou vášho prehliadača. (Áno! 127.0.0.1:8000je URL. A https://djangogirls.orgje tiež URL.)

![](/obrazky/djangogirls05.png)

Každá stránka na internete potrebuje svoju vlastnú URL. Vaša aplikácia tak vie, čo má kedy ukázať používateľovi, ktorý otvorí danú adresu URL. V Django používame niečo, čo sa nazýva **URLconf**(konfigurácia URL). URLconf je sada vzorov, ktoré sa Django pokúsi priradiť k požadovanej adrese URL, aby našiel správne zobrazenie.

### Ako fungujú adresy URL v Django?

Otvorme súbor mysite/urls.py v VS-Code a uvidíme ako vyzerá jeho obsah:

~~~
"""mysite URL Configuration

[...]
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
~~~

Ako vidíme, Django nám sem už niečo dal. Riadky medzi trojitými úvodzovkami ( ''' riadky textu """) sa nazývajú docstring – môžete ich napísať na začiatok súboru, triedy alebo metódy, aby ste opísali, čo robí. Nebude ich spúšťať Python.

Administrátorská adresa URL, ktorú ste navštívili v predchádzajúcej kapitole, je už tu:
~~~
path('admin/', admin.site.urls),
~~~
Tento riadok znamená, že pre každú adresu URL, ktorá začína reťazcom admin/, Django nájde zodpovedajúce zobrazenie . V tomto prípade zahrnieme veľa adries URL pre správcov, takže to všetko nie je zabalené do tohto malého súboru – je to čitateľnejšie a čistejšie.

#### Vaša prvá adresa URL Django

Je čas vytvoriť si našu prvú adresu URL. Chceme, aby ' http://127.0.0.1:8000/ ' bol domovskou stránkou nášho blogu a zobrazoval zoznam príspevkov.

Chceme tiež zachovať v **mysite/urls.py** čistotu súboru, čo znamená že budeme importovať adresy URL z našej aplikácie blog do hlavného súboru **mysite/urls.py**.

Pokračujeme tak, že pridáme riadok, ktorý bude importovať **blog.urls**. Budeme tiež musieť zmeniť **from django.urls…riadok**, pretože tu používame  **include**, takže tento import budete musieť pridať do nového riadku.

Náš súbor mysite/urls.py by mal teraz vyzerať takto:
~~~
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]
~~~
Django teraz presmeruje všetko, čo príde do 'http://127.0.0.1:8000/' na **blog.urls**, a hľadá tam ďalšie informácie kam ísť.

#### blog.urls

Vytvoríme si nový prázdny súbor s názvom **urls.py** v adresári **blog** a otvoríme si ho v VS-Code. Následne pridáme do neho tieto prvé dva riadky:
~~~
from django.urls import path
from . import views
~~~
Tu importujeme funkciu Djanga **path** a všetky naše views zaplikácie **blog**. (Zatiaľ žiadne views nemáme, ale o chvíľu sa k tomu dostaneme tiež.)

Potom môžeme pridať do blog/urls.py náš prvý vzor adresy URL:
~~~
urlpatterns = [
    path('', views.post_list, name='post_list'),
]
~~~

Ako vidíte, ku koreňovej adrese URL teraz priraďujeme adresy ktoré sú volané z **view. post_list**. Tento vzor adresy URL sa bude zhodovať s prázdnym reťazcom a Django URL resolver bude ignorovať názov domény (tj http://127.0.0.1:8000/ ), ktorý je predponou celej cesty URL. Tento vzor povie Djangovi, že **views.post_list** je to správne miesto, kam má ísť, ak niekto vstúpi na vašu webovú stránku na adrese ' http://127.0.0.1:8000/ '.

Posledná časť, **name='post_list'**, je názov adresy URL, ktorá sa použije na identifikáciu zobrazenia. Môže byť rovnaký ako názov zobrazenia, ale môže to byť aj niečo úplne iné. Pomenované adresy URL budeme v projekte používať neskôr, preto **je dôležité pomenovať každú adresu URL v aplikácii**. Mali by sme sa tiež snažiť, aby názvy adries URL boli jedinečné a ľahko zapamätateľné.

Ak sa teraz pokúsite navštíviť stránku http://127.0.0.1:8000/, nájdeme tu správu „webová stránka nie je k dispozícii“. Je to preto, že server (pamätáte si, že ste napísali runserver?) už nie je spustený. Pozrite sa do okna konzoly servera a zistite prečo. Uvidíte tam niečo takéto:
~~~
   return _bootstrap._gcd_import(name[level:], package, level)
  File "<frozen importlib._bootstrap>", line 1030, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1007, in _find_and_load
  File "<frozen importlib._bootstrap>", line 986, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 680, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 850, in exec_module
  File "<frozen importlib._bootstrap>", line 228, in _call_with_frames_removed
  File "/Users/ola/djangogirls/blog/urls.py", line 5, in <module>
    path('', views.post_list, name='post_list'),
AttributeError: module 'blog.views' has no attribute 'post_list'
~~~

Vaša konzola zobrazuje chybu, ale nebojte sa – v skutočnosti je tento oznam veľmi užitočný. Hovorí vám totiž, že neexistuje **atribút 'post_list'** . Tak sa totiž volá view (pohľad), ktorý sa Django snaží nájsť a použiť, no ešte sme ho nevytvorili, takže ho najisť ani nemôže. V tejto fáze nebude fungovať ani **/admin/**. Žiadny strach – dostaneme sa tam. Ak sa zobrazí iná chybová správa, skúste reštartovať webový server. Ak to chcete urobiť, v okne konzoly, na ktorej je spustený webový server, tak ho najprv zastavte stlačením klávesov Ctrl+C (spolu kláves Control a C). V systéme Windows možno budete musieť stlačiť kombináciu klávesov Ctrl+Break. Potom musíme reštartovať webový server spustením príkazu **python manage.py runserver**.

#### Django views

V tejto fáze začína čas na kreatívnu tvorbu. Najprv sa zbavíme chyby, ktorú sme vytvorili v predchádzajúcej časti.

Views je miesto, kam vložíme „logiku“ našej aplikácie. Požiada o informácie zo súboru **model** ktorý bol predtým vytvorený a odošle ich do **template**. V ďalšej kapitole vytvoríme k tomu teda prislušný template (šablónu). Views (zobrazenia) sú len funkcie Pythonu, ktoré sú o niečo komplikovanejšie ako tie, ktoré sme spomínali v rámci základov Pythonu .

Views sú umiestnené v súbore views.py. A do tohoto súboru blog/views.py pridáme naše views.

#### blog/views.py

Keď otvoríme tento súbor v našom editore kódu tak uvidíme niečo takéto:
~~~
from django.shortcuts import render

# Create your views here.
~~~

Zatiaľ tu nie je príliš veľa vecí a riadky začínajúce s # sú komentáre – to znamená, že tieto riadky nebude Python spracovávať tak ako !!! text !!!.

Poďme teda vytvoriť view a pridajme nasledujúci minimálny pohľad:
~~~
def post_list(request):
    return render(request, 'blog/post_list.html', {})
~~~
Ako vidieť vytvorili sme funkciu ( def) **post_list**, ktorá preberá **request** a bude  vracať (**return**) hodnotu, ktorú získa z volania inej funkcie **render**, ktorá spracuje našu šablónu **blog/post_list.html**.

Uložte súbor, prejdite na http://127.0.0.1:8000/ a pozrite sa, čo sa stane. Ďalšia chyba! Tak si prečítajme, čo sa teraz deje:

![](/obrazky/djangogirls06.png)

Text hovorí, že server beží, ale stále existujú nejaké problémy. Nebojte sa, je to len chybová stránka, niet sa čoho báť. Rovnako ako chybové hlásenia v konzole aj tieto hlásenia sú skutočne veľmi užitočné. Môžete si prečítať, že **TemplateDoesNotExist** . Poďme opraviť túto chybu a vytvoriť chýbajúcu šablónu (template).
<a href="#section2">
### Miesto pre vytvorenie súboru HTML
</a>
Ak by sme sa spýtali čo je to šablóna, odpoveď by bola.

**Šablóna resp. template** je súbor, ktorý môžeme opätovne použiť na prezentovanie rôznych informácií v konzistentnom formáte – môžete napríklad použiť šablónu, ktorá vám pomôže napísať list, pretože hoci každý list môže obsahovať inú správu a byť adresovaný inej osobe, oba budú zdieľať rovnaký formát.

Formát šablóny Django je opísaný v jazyku zvanom HTML (HyperText Markup Language ) ktorý je skriptovací jazyk používaný webovými prehliadačmi na vykresľovanie stránok v celosvetovej sieti www (world wide web).

#### Čo je HTML?
HTML je kód, ktorý interpretuje váš webový prehliadač – napríklad Chrome, Firefox alebo Safari – na zobrazenie webovej stránky pre používateľa.

HTML je skratka pre „HyperText Markup Language“. HyperText znamená, že ide o typ textu, ktorý podporuje hypertextové prepojenia medzi stránkami. Označenie znamená, že sme vzali dokument a označili ho kódom, ktorý niečomu (v tomto prípade prehliadaču) povie, ako má stránku interpretovať. HTML kód je vytvorený pomocou značiek , z ktorých každá začína < a končí na >. Tieto značky predstavujú prvky označovania .

#### Vaša prvá šablóna

Vytvorenie šablóny znamená vytvorenie súboru šablóny.

Naše šablóny sú uložené v adresári **blog/templates/blog**. Takže najprv vytvoríme adresár s názvom **templates** v adresári vášho blogu. Potom vytvorte ďalší adresár s názvom **blog** v tomto adresári šablón:
~~~
blog
└───templates
    └───blog
~~~

Možno by ste sa mohli čudovať, prečo potrebujeme dva adresáre s názvom **blog**. Ako neskôr zistíme, je to užitočná konvencia pomenovania, ktorá nám zvýši prehladnsť keď sa veci začnú komplikovať.

A teraz vytvorte v adresári **blog/templates/blog** avizovaný súbor šablóny **post_list.html** (zatiaľ ho však necháme prázdny)  .

Pozrite sa, ako náš web vyzerá teraz: http://127.0.0.1:8000/

Ak chyba **TemplateDoesNotExist** pretrváva, skúste reštartovať server. Prejdite na príkazový riadok, zastavte server stlačením Ctrl+C (klávesy Control a C spolu) a spustite ho znova spustením príkazu **python manage.py runserver**.

![](/obrazky/djangogirls07.png)

Ak chyba pominula, tak náš web nezverejňuje nič okrem prázdnej stránky, pretože aj naša šablóna je prázdna. To musíme ale napraviť. Otvorte preto post_list.html a pridajme nasledujúci kód:
~~~
<!DOCTYPE html>
<html>
<body>
    <p>Hi there!</p>
    <p>It works!</p>
</body>
</html>
~~~

Teraz náš web vyzerá takto. Navštívte ho a zistite použitím príkazu http://127.0.0.1:8000/

![](/obrazky/djangogirls08.png)

* Riadok <!DOCTYPE html> nie je značka HTML. Deklaruje iba typ dokumentu. Tu informuje prehliadač, že typ dokumentu je HTML5 . Toto je vždy začiatok akéhokoľvek súboru HTML5.
* Najzákladnejšia značka, <html>, je vždy začiatkom html obsahu a </html>je vždy koncom. Ako vidíte, celý obsah webovej stránky sa nachádza medzi počiatočnou značkou <html>a záverečnou značkou</html>
* <p> je značka pre prvky odseku; </p>zatvorí každý odsek

<h3 id="section2"> Hlava a telo HTML súboru</h3>

Každá stránka HTML je tiež rozdelená na dve časti: hlavu a telo .

* **hlava** je časť, ktorá obsahuje informácie o dokumente, ktoré sa nezobrazujú na obrazovke.

* **telo** je časť, ktorá obsahuje všetko ostatné, čo sa zobrazuje ako súčasť webovej stránky.

Používame na to <head>, aby sme prehliadaču oznámili konfiguráciu stránky a <body> aby sme mu povedali, čo sa na stránke vlastne nachádza.

Môžete napríklad do post_list.html vložiť prvok názvu webovej stránky do súboru <head>, takto:
~~~
<!DOCTYPE html>
<html>
    <head>
        <title>Ola's blog</title>
    </head>
    <body>
        <p>Hi there!</p>
        <p>It works!</p>
    </body>
</html>
~~~
Uložte súbor a obnovte stránku čím dostaneme:

![](/obrazky/djangogirls09.png)

Na základe toho prehliadač pochopil, že názov vašej stránky je „Olin blog“. Interpretoval totiž riadok **<title>Ola's blog</title>** a umiestnil text do záhlavia vášho prehliadača (bude tiež použitý pre záložky atď.).

Ku každému úvodnému tagu (značke) v súbore post_list.html zodpovedá uzatváracia značka , s /, a že prvky sú vnorené (tj nemôžete zavrieť konkrétny tag, kým sa nezatvoria aj všetky, ktoré boli v ňom).

Je to ako dávať veci do krabíc. Máte jednu veľkú krabicu, <html></html>; vnútri je <body></body>, a to obsahuje ešte menšie boxy: <p></p>.

Musíme dodržiavať tieto pravidlá zatvárania značiek a vkladania prvkov, lebo ak tak neurobíme, prehliadač ich nemusí vedieť správne interpretovať a vaša stránka sa bude zobrazovať nesprávne.

#### Prispôsobenie šablóny

Teraz nastal čas aby sme upravili, doplnili a prispôsobili našu šablónu. Tu je niekoľko užitočných značiek:
~~~
* <h1>A heading</h1> pre váš najdôležitejší nadpis
* <h2>A sub-heading</h2>pre nadpis na ďalšej úrovni
* <h3>A sub-sub-heading</h3>…a tak ďalej, až<h6>
* <p>A paragraph of text</p>
* <em>text</em>zdôrazní váš text
* <strong>text</strong>silne zdôrazní váš text
* <br>prejde na iný riadok (do br nemôžete vložiť nič a nie je tam žiadna uzatváracia značka)
* <a href="https://djangogirls.org">link</a> vytvorí odkaz
* <ul><li>first item</li><li>second item</li></* ul>vytvorí zoznam, ako je tento!
* <div></div>definuje časť stránky
* <nav></nav>definuje množinu navigačných odkazov
* <article></article>špecifikuje nezávislý, samostatný obsah
* <section></section>definuje sekciu v dokumente
* <header></header>určuje hlavičku dokumentu alebo sekcie
* <main></main>určuje hlavný obsah dokumentu
* <aside></aside>definuje nejaký obsah okrem obsahu, do ktorého je umiestnený (napríklad bočný panel)
* <footer></footer>definuje pätu dokumentu alebo sekcie
* <time></time>definuje konkrétny čas (alebo dátum a čas)
~~~

Tu je príklad použitia niektorých príkazov v našej šablóne. Skopírujeme ho a vložíme do **blog/templates/blog/post_list.html**:

~~~
<!DOCTYPE html>
<html>
    <head>
        <title>Django Girls blog</title>
    </head>
    <body>
        <header>
            <h1><a href="/">Django Girls Blog</a></h1>
        </header>

        <article>
            <time>published: 14.06.2014, 12:14</time>
            <h2><a href="">My first post</a></h2>
            <p>Aenean eu leo quam. Pellentesque ornare sem lacinia quam venenatis vestibulum. Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus.</p>
        </article>

        <article>
            <time>published: 14.06.2014, 12:14</time>
            <h2><a href="">My second post</a></h2>
            <p>Aenean eu leo quam. Pellentesque ornare sem lacinia quam venenatis vestibulum. Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut f.</p>
        </article>
    </body>
</html>
~~~

Vytvorili sme jednu sekciu **header** a dve sekcie.**article**

* Časť **header** obsahuje názov nášho blogu – je to nadpis a odkaz
* Tieto dve časti **article** obsahujú naše blogové príspevky s dátumom zverejnenia v prvku **time**, **h2** prvok s názvom príspevku, na ktorý sa dá kliknúť, a **p** prvok (odsek) pre text nášho blogového príspevku.

Čo nám vytvorí tento efekt:

![](/obrazky/djangogirls10.png)

V tomto štádiu je možné znovu nasadiť našu stránku do produkcie vybranému ISP ktorý ponúka prostredie na báze Pythonu a Django. Taktiež je vhodné výtvoriť zálohu nášho projektu na Git resp. GitHub.

<div id="section1">
<h3> Django ORM a QuerySets</h3>
</div>


V tejto časti sa budeme zaoberať problematikou ako sa Django pripája k databáze a ukladá do nej údaje.
Skôr však si povedzme čo je to QuerySets.

QuerySet je v podstate zoznam objektov daného modelu. QuerySets nám umožňujú čítať dáta z databázy, filtrovať ich a objednávať.

Najjednoduchšie je poznať túto problematiku prostredníctvom príkladu ktorý si najprv priblížime prostredníctvom Django Shell-u.

#### Django Shell

Otvorte teda lokálnu konzolu Pythonu a zadajte tento príkaz:

~~~
(myvenv) ~/djangogirls$ python manage.py shell
~~~

Účinok by mal byť takýto:

~~~
(InteractiveConsole)
>>>
~~~

Čím sme sa dostali do interaktívnej konzoly Django. Je to ako výzva Pythonu, ale s rozˇˇsíreniami a špecifikami Django. To znamená že tu môžete použiť všetky príkazy Pythonu.

#### Ako vypísať všetky objekty

Skúsme najprv takto zobraziť všetky naše príspevky Post. Môžete to urobiť pomocou nasledujúceho príkazu:
~~~
>>> Post.objects.all()
Traceback (most recent call last):
      File "<console>", line 1, in <module>
NameError: name 'Post' is not defined
~~~
Objavila sa chyba ktorá nám hovorí že neexistuje žiadny príspevok. Je to správne lebo sme to zabudli importovať. Urobíme to príkazom
~~~
>>> from blog.models import Post
~~~
Model importuje **Post** z **blog.models**. Potom skúsime znova zobraziť všetky príspevky:
~~~
>>> Post.objects.all()
<QuerySet [<Post: my post title>, <Post: another post title>]>
~~~

A dostávame zoznam príspevkov, ktoré sme už skôr vytvorili. Tieto príspevky sme vytvorili ale manuálne pomocou administratívneho rozhrania Django. My teraz ale chceme vytvárať nové príspevky pomocou kódu Pythonu.

#### Vytvorenie objektu

My si vytvoríte nový objekt Post v databáze príkazom:
~~~
>>> Post.objects.create(author=me, title='Sample title', text='Test')
~~~

Chýba nám tu však jedna ingrediencia **me** t.j. že práve my/ja (me) sme  tvorcami príspevku. Modelu totiž chceme tiež odovzdať inštanciu **User** ktorá identifikuje autora príspevku.

Najprv teda importujme model žívateľa :
~~~
>>> from django.contrib.auth.models import User
~~~

V tejto súvislosti sa pozrime akých všetkých užívateľov v databáze máme:
~~~
>>> User.objects.all()
<QuerySet [<User: admin>]>
~~~

Toto je superužívateľ, ktorého sme predtým vytvorili! Poďme teraz získať inštanciu používateľa (upravte tento riadok tak, aby používal svoje vlastné používateľské meno):
~~~
>>> me = User.objects.get(username='admin')
~~~

Ako môžeme predpokladať, teraz pri použití príkazu **get** by sme dostali odpoveď ktorá sa rovná 'admin'. User sa rovná username a to 'admin'.

Teraz už môžeme konečne vytvoriť náš príspevok:
~~~
>>> Post.objects.create(author=me, title='Sample title', text='Test')
<Post: Sample title>
~~~
Tak to skontrolujme či to zafungovalo.
~~~
>>> Post.objects.all()
<QuerySet [<Post: my post title>, <Post: another post title>, <Post: Sample title>]>
~~~
Ak áno môžeme pokračovať a pridať ďalšie príspevky, aby sme videli, ako to funguje. Pridajme teda ďalšie dve alebo tri pomocou 
~~~
>>> Post.objects.create(author=me, title='Sample title', text='Test')
<Post: Sample title>
~~~
a potom prejdite na ďalšiu časť. 

#### Filtrovanie objektov

Veľkým prínosom QuerySets je možnosť filtrovania. Povedzme, že chceme nájsť všetky príspevky, ktoré napísal používateľ ola. Budeme používať **filter** namiesto **all** v **Post.objects.all()**. V zátvorkách uvádzame, aké podmienky musí blogový príspevok spĺňať, aby skončil v našej sade dotazov. V našom prípade je podmienkou to, že **author** by sa mal rovnať **me**. Spôsob, ako to napísať v Django, je **author=me**. Teraz náš kúsok kódu vyzerá takto:
~~~
>>> Post.objects.filter(author=me)
<QuerySet [<Post: Sample title>, <Post: Post number 2>, <Post: My 3rd post!>, <Post: 4th title of post>]>
~~~

Ak chceme vidieť všetky príspevky, ktoré obsahujú slovo „title“ v poli **title**.

~~~
>>> Post.objects.filter(title__contains='title')
<QuerySet [<Post: Sample title>, <Post: 4th title of post>]>
~~~
Poznámka: Medzi **title** a **contains** sú dva znaky podčiarknutia (_). ORM Django používa toto pravidlo na oddelenie názvov polí („title“) a operácií alebo filtrov („contains“). Ak použijete iba jedno podčiarknutie, zobrazí sa chyba ako „FieldError: Cannot resolve keyword title_contains"

Môžeme tiež získať zoznam všetkých uverejnených príspevkov. Robíme to filtrovaním všetkých príspevkov, pre ktoré bolo v minulosti nastavené **published_date**:

~~~
>>> from django.utils import timezone
>>> Post.objects.filter(published_date__lte=timezone.now())
<QuerySet []>
~~~

Príspevok ktorý sme pridali z konzoly Python zatiaľ nie je zverejnený. Ale môžeme to zmeniť tak že najprv získame inštanciu príspevku, ktorý chceme zverejniť. Platí to však iba pre prípad ak máme iba jednu inštanciu modelu (my však máme dve a dokonca rovnaké "Sample title")

<h4 id="section3">Príklad</h4>

~~~
>>> post = Post.objects.get(title="Sample title") je pre jednu inštanciu modelu
>>> posts = Post.objects.filter(title="Sample title") je pre viacero inštancii modelu
~~~
V náväznosti na predchádzajúcu situáciu tu vzniká chyba a operácia sa neuskutoční. Riešenie by vyžadovalo odlíšenie inštancii modelu ako napr. "Sample title 01" a "Sample title 02"
A potom ich publikovať ppostupne našou metódou publish:
~~~
>>> post.publish() možno použiť ak ide iba o jednu inštanciu ktorú priradíme premmenej post
~~~

Teraz teda skúsme znova získať zoznam publikovaných príspevkov (trikrát stlačte kláves so šípkou nahor a stlačte enter):

~~~
>>> Post.objects.filter(published_date__lte=timezone.now())
<QuerySet [<Post: Sample title>]>
~~~

#### Zoraďovanie objektov

QuerySets vám tiež umožňujú usporiadať zoznam objektov. Skúsme ich zoradiť podľa poľa **created_date**:
~~~
>>> Post.objects.order_by('created_date')
<QuerySet [<Post: Sample title>, <Post: Post number 2>, <Post: My 3rd post!>, <Post: 4th title of post>]>
~~~
Poradie môžeme zmeniť aj tak, že na začiatok pridáme -:
~~~
>>> Post.objects.order_by('-created_date')
<QuerySet [<Post: 4th title of post>,  <Post: My 3rd post!>, <Post: Post number 2>, <Post: Sample title>]>
~~~

#### Komplexné dotazy (queris) prostredníctvom zreťazenia metód (method-chaining)

Ako ste videli, niektoré metódy QuerySet vracajú **Post.objects**. Podobné metódy môžu byť tiež volané na QuerySet a potom vrátia nový QuerySet. Ich účinok teda môžeme spojiť ich reťazením :

~~~
>>> Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
<QuerySet [<Post: Post number 2>, <Post: My 3rd post!>, <Post: 4th title of post>, <Post: Sample title>]>
~~~

Je to veľmi silný nástroj a umožňuje nám písať pomerne zložité dotazy (queries). Ak chceme zatvoriť shell, zadajte toto:
~~~
>>> exit()
$
~~~~

### Dynamické údaje v šablónach

Zatiaľ máme v našej aplikácii tieto tri rôzne časti: 
* model **Post** ktorý je definovaný v models.py
* **post_list** ktorý je definovaný v **views.py **a 
* pridali sme aj jednu šablónu **post_list.html**. 
  
Ako ale zabezpečíme, aby sa naše príspevky zobrazovali v našej šablóne HTML? Veď to je to, čo vlastne **chceme urobiť, vziať nejaký obsah (model uložený v databáze) a pekne ho zobraziť v našej šablóne**.

A to je presne to, čo majú **views** (zobrazenia) robiť: **spájajú modely a šablóny**. Na základe toho budeme musieť vziať modely podľa nášho **post_list**, ktoré chceme zobraziť, a odovzdať ich šablóne. Vo view sa rozhoduje, čo sa (resp. čo model) zobrazí v šablóne.

Dosiahneme to tak že otvoríme **blog/views.py** v našom editore kódu kde vidíme ako doterajší views post_list-u:
~~~
from django.shortcuts import render

def post_list(request):
    return render(request, 'blog/post_list.html', {})
~~~

Teraz aplikujeme myšlienku, keď sme hovorili o prepojení kódu napísaného v rôznych súboroch pomocou from... import... . Teraz je ten moment, kedy musíme prepojiť model pre **Post**, ktorý sme napísali do **models.py**. Urobíme to v **blog/views.py** pridaním riadku **from .models import Post** takto:

~~~
from django.shortcuts import render
from .models import Post
~~~

Bodka pred **models** znamená ***aktuálny adresár alebo aktuálnu aplikáciu*** . Oba súbory **views.py** a **models.py** sú pritom v rovnakom adresári. To znamená, že môžeme použiť **.** a iba názov súboru (bez **.py**). Takto importujeme názov modelu ( **Post** ).

Ale čo treba urobiť ďalej aby sme z modelu prevzali skutočné blogové príspevky **Post** ? Potrebujeme niečo také ako **QuerySet** s ktorým sme sa zoznámi vyššie a nezaškodí nám keď sa do tejto časti znovu pozrieme.

### QuerySet

Vyššie sme sa oboznámili ako QuerySets fungujú. Hovorili sme o nich v kapitole <a href="#section1">Django ORM a QuerySets</a> .

Takže teraz už vieme ako zoradiť publikované blogové príspevky podľa published_date. Urobili sme to už aj v časti QuerySets! Do blog/views.py pridáme riadok :
~~~
Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
~~~

Takže otvormíe súbor **blog/views.py** a tento kúsok kódu pridáme do funkcie **def post_list(request)**. Nezabudnime však najprv pridať aj **from django.utils import timezone**. Aktuálny obsah **blog/views.py** potom bude :
~~~
from django.shortcuts import render
from django.utils import timezone
from .models import Post

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {})
~~~
Ak chceme zobraziť našu sadu príspevkov v celom v zozname príspevkov nášho blogu pomocou QuerySet, musíme urobiť dve veci:

1. Treba odovzdat **posts** QuerySet-u do kontextu šablóny. To teraz aj urobíme a urobíme to zmenou volania funkcie **render**.
2. Upravíme šablónu, aby sa zobrazila sada **posts** QuerySet-u. Ale tomu sa budeme venovať v ďalšej časti.
   
>**posts** je premenná pre správy ktorú vytvárame pre náš QuerySet a môžeme ju považovať za názov našej QuerySet a odteraz ho môžeme označovať týmto názvom.

Vo funkcii render máme jeden parameter **request** (čo je všetko to, čo dostaneme ako požiadavku cez internet na server backendu od užívateľa ). Druhým parametrom je súbor ktorý udáva šablónu ( **'blog/post_list.html'**). Posledným parameterom sú **{}**. Je to miesto, do ktorého môžeme pridať nejaké informácie, ktoré má šablóna použiť. Sú to predovšetkým názvy príspevkov ktoré im musíme dať ( príspevky nateraz pomenujeme ako **'posts'**). Tento parameter potom bude vyzerať takto: **{'posts': posts}**. Časť pred **:** je reťazec obsahujúci názov príspevku a preto ho treba zabaliť do úvodzoviek **''**. **post** je ako sme už spomenuli premenná vyjadrujúca jednotlivé príspevky.

Takže náš  **blog/views.py** by mal nakoniec vyzerať takto:
~~~
from django.shortcuts import render
from django.utils import timezone
from .models import Post

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})
~~~

To je ku QuerySets v Django pre naše potreby všetko. Ak by ste sa chceli s touto problematikou zoznámiť trochu viac mali by ste sa pozrieť na stránku : https://docs.djangoproject.com/en/3.2/ref/models/querysets/

### Šablóny (templates) Django

Nastal čas aby sme v našom projekte zobrazili nejaké údaje. Django nám za týmto účelom poskytuje pre šablóny niekoľko užitočných tagov (značiek) ktoré sú vstavané v Djangu.

#### Čo sú značky šablón?

Asi nám je zrejmé, že do HTML súborov nemôžeme písať kód Pythonu. Je to preto, že prehliadače mu nerozumejú. Kódu Python rozumejú iba interprety Pythonu. Internetové prehlaidače ktoré používame na spúšťanie weboývý aplikácii poznajú iba HTML. Vieme, že HTML je skôr statický (obsah súboru a jeho interpretácia sú nemenné) nástroj, zatiaľ čo Python je nástrojom oveľa dynamickejším.

Značky šablón Django nám umožňujú prenášať do HTML veci ktoré sú podobné Pythonu. Takže tým môžeme rýchlejšie vytvárať dynamické (menitelné) webové stránky bez nutnosti opakovania statických stránok s odlišným obsahom a prejavom.

#### Zobrazenie šablóny so zoznamom príspevkov

V predchádzajúcej časti sme poskytli našej šablóne zoznam príspevkov v premennej **posts**. A teraz zoznam príspevkov zobrazíme v HTML.

Na tlač premennej v šablónach Django používame dvojité zložené zátvorky s názvom premennej vo vnútri, napríklad v takto:
~~~
{{ posts }}
~~~

Vyskúšajme to v našej šablóne **blog/templates/blog/post_list.html**. Otvorme ju v editore kódu a nahraďme existujúce prvky **<article** s **{{ posts }}**. Uložme súbor a obnovme stránku, aby sme videli výsledky:

![](/obrazky/djangogirls11.png)

Ako vidieť, všetko, čo máme v **blog/templates/blog/post_list.html**, je toto:
~~~
<QuerySet [<Post: My second post>, <Post: My first post>]>
~~~
To znamená, že Django to chápe príspevky - post ako zoznam objektov. Zo základov Pythonu by sme si mali pamätať ako môžeme takéto zoznamy zobraziť . Áno, so slučkami v cykle for. V šablóne Django ich však robíte so zloženými zátvorkami a percentami %:
~~~
{% for post in posts %}
    {{ post }}
{% endfor %}
~~~

![](/obrazky/djangogirls12.png)

Funguje to ale my chceme aby sa príspevky zobrazovali ako statické príspevky, ktoré sme vytvorili už predtým v časti kde sa zaoberáme <a href="#section2">úvodom do HTML</a> . Tagy HTML však môžete kombinovať so šablónami. Naše **body** v **blog/templates/blog/post_list.html** bude vyzerať takto:
~~~
<header>
    <h1><a href="/">Django Girls Blog</a></h1>
</header>

{% for post in posts %}
    <article>
        <time>published: {{ post.published_date }}</time>
        <h2><a href="">{{ post.title }}</a></h2>
        <p>{{ post.text|linebreaksbr }}</p>
    </article>
{% endfor %}
~~~

Všetko, čo vložíte medzi **{% for %}** a **{% endfor %}** sa bude opakovať pre každý objekt v zozname. Obnovte svoju stránku a mali by sme dostať niečo takéto:

![](/obrazky/djangogirls13.png)

Môžeme si všimnúť, že sme tentoraz sme použili trochu iný zápis ( **{{ post.title }}** alebo **{{ post.text }}** ). Takto pristupujeme k údajom v každom z polí ktoré je definované v našom modeli **Post**. **|linebreaksbr** vyjadruje že text príspevkov prechádza cez filter, aby takto ukončenie riadkov previedli na odseky.

## CSS nám pomôže urobiť stránku krajšiu

Náš blog zatiaľ vyzerá dosť škaredo. Preto je čas urobiť našu stránku trochu krajšou a použijeme na to CSS.

#### Čo je CSS ?

Cascading Style Sheets (CSS) je jazyk používaný na popis vzhľadu a formátovania webovej stránky napísaný v jazyku používajúcom tagy (značky) ako v HTML. Môžeme to chápať ako make-up pre našu webovú stránku.

Keďže nechceme ani v tejto časti začínať od nuly, môžeme použiť niečo čo programátori uvoľnili na internet zadarmo. Strácať čas a energiu riešením niečoho čo už je vytvorené nie je rozumné ani v tejto oblasti. Tu sa nám ponúka knižnica Bootstrap.

### Použitie Bootstrap

Bootstrap je jedným z najpopulárnejších frameworkov HTML a CSS na vývoj krásnych webových stránok: https://getbootstrap.com/ Napísali ho programátori, ktorí pracovali pre Twitter. Teraz je vyvýjaní dobrovoľníkmi z celého sveta.

#### Nainštalujeme si Bootstrap

Ak chcete nainštalovať Bootstrap, otvoríme svoj blog/templates/blog/post_list.html súbor v editore kódu a Bootstrap pridáme do sekcie **head** :
~~~
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
~~~

Týmto sa do nášho projektu síce nepridajú žiadne súbory ale získame odkaz na súbory ktoré existujú na internete a ktoré môžeme takto použiť. Takže pokračujme tým že otvoríme svoj web a obnovíme svoju stránku.

![](/obrazky/djangogirls14.png)

Zmena je tu evidentne batatelná.

### Statické súbory v Django

Nakoniec je potrebné aby sme sa bližšie pozreli na komponenty, ktoré nazývame statické súbory. **Statické súbory** sú všetky vaše CSS prvky a obrázky. Ich obsah nezávisí od kontextu požiadavky a bude stále rovnaký pre každého užívateľa.

#### Kam umiestniť statické súbory pre Django

Django už vie, kde nájsť statické súbory pre vstavanú aplikáciu „admin“. Teraz musíme pridať nejaké statické súbory pre našu vlastnú aplikáciu ktorou je **blog**.

Urobíme to vytvorením priečinka s názvom **static** v aplikácii blogu:
~~~
djangogirls
│
├── blog
│   ├── migrations
│   ├── static
│   └── templates
└── mysite
~~~

Django automaticky nájde všetky priečinky nazývané „statické“ vo všetkých priečinkoch vašich aplikácií. Potom bude môcť použiť ich obsah ako statické súbory.

### Váš prvý súbor CSS

Poďme teraz vytvoriť súbor CSS, aby sme na našu webovú stránku pridali náš vlastný štýl dizajnu. Vytvorme v našom adresári **blog** nový adresár **static** a v ňom nový adresár s názvom **css**. V tomto adresári vytvorme css súbor s názvom **blog.css** tak aby sme dostali nasledovnú štruktúru. 

~~~
DJANGOGIRLS
│
├── blog
│     └─── static
          └─── css
               └─── blog.css
~~~

Týmto máme vytvorené podmienky napísať nejaké CSS. Otvorte preto súbor **blog/static/css/blog.css**.

Aj keď táto problematika je klúčovou pre vizuál a umelecký dojem nebudeme tu zachádzať príliš hlboko do prispôsobovania a učenia sa o CSS. Na konci tejto časti je však uvedené odporúčanie na bezplatný kurz CSS a tu sa môžeme o CSS dozvedieť viac.

Pri tejto príležitosti však urobíme pre CSS aspoň trochu kódu aby sa načrtli väzby a dôsledky ktoré CSS má na jednotlivé stránky. 

Možno by sme napr. mohli zmeniť farbu našich hlavičiek? Na pochopenie farieb používajú počítače špeciálne kódy. Tieto kódy začínajú znakom **#** za ktorým nasleduje 6 písmen (A–F) a čísla (0–9). Napríklad kód pre modrú farbu je **#0000FF**. Kódy farieb ostatných farieb nájdeme tu: http://www.colorpicker.com/ . Môžete tiež použiť [preddefinované farby](http://www.w3schools.com/colors/colors_names.asp), ako napríklad red a green.

Do súboru **blog/static/css/blog.css** by sme mali potom pridať nasledujúci kód :
~~~
h1 a, h2 a {
    color: #F79100;
}
~~~

**h1 a** je selektor CSS. To znamená, že naše štýly aplikujeme na akýkoľvek  prvok **a** vo vnútri prvku **h1** . Selektor **h2 a** urobí to isté pre prvky **h2**. Takže keď máme niečo ako 
~~~
<h1><a href="">link</a></h1>
~~~
použije sa štýl **h1 a**. V tomto prípade mu povieme, aby zmenil svoju farbu na **#C25100**, čo je farba tmavooranžová. Alebo si sem môžeme dať aj inú, svoju vlastnú farbu. Je však potrebné sa uistiť, že má dobrý kontrast na bielom pozadí.

V súbore CSS určujeme štýly pre prvky v súbore HTML. Prvý spôsob, ako identifikujeme prvky, je názov prvku. Možno si ich pamätáte ako značky (tagy) zo sekcie o HTML. Veci ako **a**, **h1**, a **body** sú ďalšie príklady názvov prvkov. Prvky identifikujeme aj podľa atribútu **class** alebo atribútu **id**. Class a id sú názvy, ktoré prvku zadáme my sami. Triedy definujú skupiny prvkov a identifikátory poukazujú na konkrétne prvky. Napríklad nasledujúci prvok môžete identifikovať pomocou názvu prvku **a**, triedy **external_link** alebo id **link_to_wiki_page**:

~~~
<a href="https://en.wikipedia.org/wiki/Django" class="external_link" id="link_to_wiki_page">
~~~

Viac o [CSS Selectoroch](http://www.w3schools.com/cssref/css_selectors.asp) si môžeme prečítať na w3schools .

To že sme pridali nejaké CSS musíme tiež povedať našej šablóne HTML. Otvorme súbor **blog/templates/blog/post_list.html** súbor v editore kódu a pridajme na jeho úplný začiatok tento riadok :
~~~
{% load static %}
~~~

Práve takto totiž načítavame statické súbory. Medzi značky **<head>** a **</head>** za odkaz na súbory CSS Bootstrap pridajme tento riadok:
~~~
<link rel="stylesheet" href="{% static 'css/blog.css' %}">
~~~

Prehliadač číta súbory v poradí, v akom sú zadané, takže sa musíme uistiť, že príslušné riadky sú na správnom mieste. V opačnom prípade môže byť kód v našom súbore prepísaný kódom v súboroch Bootstrap. Práve sme povedali našej šablóne, kde sa nachádza náš súbor CSS a náš súbor **blog/templates/blog/post_list.html** by mal teraz vyzerať takto:

~~~
{% load static %}
<!DOCTYPE html>
<html>
    <head>
        <title>Django Girls blog</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
        <link rel="stylesheet" href="{% static 'css/blog.css' %}">
    </head>
    <body>
        <header>
            <h1><a href="/">Django Girls Blog</a></h1>
        </header>

        {% for post in posts %}
            <article>
                <time>published: {{ post.published_date }}</time>
                <h2><a href="">{{ post.title }}</a></h2>
                <p>{{ post.text|linebreaksbr }}</p>
            </article>
        {% endfor %}
    </body>
</html>
~~~

Keď súbor uložíme súbor a obnovíme stránku dostaneme toto:
![](/obrazky/djangogirls15.png)

Vo vzhľade našej stránky sme už pokročili, ale možno by sme ju mohli trochu prevzdušniť a zvýšiť odstup od ľavého okraja. Skúsme preto v **blog/static/css/blog.css** pridať toto:
~~~
body {
    padding-left: 15px;
}
~~~
![](/obrazky/djangogirls16.png)

Možno by sme chceli ďalej prispôsobiť písmo v hlavičke. Urobíme to tak, že do hlavičky <**head**> v súbore **blog/templates/blog/post_list.html** pridáme toto:
~~~
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Lobster&subset=latin,latin-ext">
~~~

Tento riadok iba importuje font s názvom **Lobster** z Google Fonts ( https://www.google.com/fonts ) a tak ho ešte musíme v súbore blog.css použiť.

V ďalšom kroku nájdeme **h1 a** v súbore **CSS blog/static/css/blog.css** a tam deklaračý blok (kód medzi zloženými zátvorkami **{a }** ) . Sem pridáme riadok **font-family: 'Lobster'** a obnovíme stránku:
~~~
h1 a, h2 a {
    color: #f79100;
    font-family: 'Lobster';
}
~~~
![](/obrazky/djangogirls17.png)

Ako už bolo spomenuté vyššie, CSS má koncept tried. Tieto nám umožňujú pomenovať časť kódu HTML a použiť štýly iba na túto časť bez ovplyvnenia ostatných častí. To môže byť veľmi užitočné. Možno máte dva <**div**>-y, ktoré robia niečo iné (napríklad vaša hlavička a váš príspevok). Trieda vám môže pomôcť, aby vyzerali inak. Pokračujme teda týmto smerom a pomenujme niektoré časti kódu HTML. Nahraďme v <**header**> v súbore **blog/templates/blog/post_list.html**, všetko to čo sa tam nachádza týmto vrátane označenia bloku <**header**> <**/header**> a v prípade potreby upravte odstupy aby zodpovedali tomuto kódu:
~~~
<header class="page-header">
    <div class="container">
        <h1><a href="/">Django Girls Blog</a></h1>
    </div>
</header>
~~~
a následne sem pridáme triedu **post**, ktorá obsahuje príspevok blogu **article** a tiež upravíme odstupy.

~~~
<article class="post">
    <time>published: {{ post.published_date }}</time>
    <h2><a href="">{{ post.title }}</a></h2>
    <p>{{ post.text|linebreaksbr }}</p>
</article>
~~~

Následne pridáme do rôznych selektorov bloky deklarácií. Selektory začínajúce na **.** sa pritom týkajú tried. Na webe je na túto tému veľa dobrých návodov a článkov o CSS ako napr. na [freeCodeCamp](https://learn.freecodecamp.org/). Tieto môžu pomôcť pochopiť  aj nasledujúci kód. Zatiaľ ho iba skopírujeme a vložíme na koniec do súboru **blog/static/css/blog.css**:

~~~
.page-header {
    background-color: #f79100;
    margin-top: 0;
    margin-bottom: 40px;
    padding: 20px 20px 20px 40px;
}

.page-header h1,
.page-header h1 a,
.page-header h1 a:visited,
.page-header h1 a:active {
    color: #ffffff;
    font-size: 36pt;
    text-decoration: none;
}

h1,
h2,
h3,
h4 {
    font-family: 'Lobster', cursive;
}

.date {
    color: #828282;
}

.save {
    float: right;
}

.post-form textarea,
.post-form input {
    width: 100%;
}

.top-menu,
.top-menu:hover,
.top-menu:visited {
    color: #ffffff;
    float: right;
    font-size: 26pt;
    margin-right: 20px;
}

.post {
    margin-bottom: 70px;
}

.post h2 a,
.post h2 a:visited {
    color: #000000;
}

.post > .date,
.post > .actions {
    float: right;
}

.btn-secondary,
.btn-secondary:visited {
    color: #f79100;
    background: none;
    border-color: #f79100;
}

.btn-secondary:hover {
    color: #FFFFFF;
    background-color: #f79100;
}
~~~

Potom ešte zmeňme tento HTML kód v súbore **blog/templates/blog/post_list.htm**, ktorý zobrazuje príspevky s deklaráciami tried. 
~~~
{% for post in posts %}
    <article class="post">
        <time>published: {{ post.published_date }}</time>
        <h2><a href="">{{ post.title }}</a></h2>
        <p>{{ post.text|linebreaksbr }}</p>
    </article>
{% endfor %}
~~~

za tento kód a upravme odstupy. Súbor uložme a obnovme web!

~~~
<main class="container">
    <div class="row">
        <div class="col">
            {% for post in posts %}
                <article class="post">
                    <time class="date">
                        published: {{ post.published_date }}
                    </time>
                    <h2><a href="">{{ post.title }}</a></h2>
                    <p>{{ post.text|linebreaksbr }}</p>
                </article>
            {% endfor %}
        </div>
    </div>
</main>
~~~

Súbory uložte a obnovte svoj web aby sme dostali niečo takéto.
![](/obrazky/djangogirls18.png)

Ak sa pozrieme na kód, ktorý sme práve vložili, tak by sme našli miesta, kde sme pridali  triedy a použili ich v CSS. Napr. kde by ste potom urobili zmenu, ak by ste chceli, aby bol dátum inej farby a bol napr. tyrkysový ?

Nebojte sa v tomto CSS trochu pohrať a skúsiť niektoré veci zmeniť. Hranie sa s CSS vám môže iba pomôcť lepšie pochopiť, čo jednotlivé skripty a bloky robia. Ak niečo pokazíte, nebojte sa, vždy to môžete vrátiť späť !

### Rozšírenie šablóny

Ďalšou užitočnou vecou, ​​ktorú má pre nás Django poskytuje, je **rozšírenie šablóny**. Čo to znamená? Znamená to, že **môžeme použiť rovnaké časti HTML kódu pre rôzne stránky** nášho webu.

Šablóny nám pomáhajú aj vtedy, keď chceme použiť rovnaké informácie alebo rozloženie informácii na viacero ako jednom mieste. Nemusíte potom totiž opakovať rovnaký kód v každom súbore znova a znova. A ak chceme niečo zmeniť, nemusíte to robiť v každej šablóne a stačí nám keď to urobíme iba v jednej. Za týmto účelom si vytvoríme tzv. základnú (base) šablónu.

#### Vytvorme základnú šablónu

Base šablóna je základnou šablónou, ktorú rozširujete na každú stránku nášho webu.

Vytvorme teda **base.html** súbor v adresári **blog/templates/blog/**:
~~~
DJANGOGIRLS
│
blog
└───templates
    └───blog
            base.html
            post_list.html
~~~

Potom ho otvorte v editore kódu a skopírujte všetko zo súboru **post_list.html** do **base.html**:

~~~
{% load static %}
<!DOCTYPE html>
<html>
    <head>
        <title>Django Girls blog</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Lobster&subset=latin,latin-ext">
        <link rel="stylesheet" href="{% static 'css/blog.css' %}">
    </head>
    <body>
        <header class="page-header">
          <div class="container">
              <h1><a href="/">Django Girls Blog</a></h1>
          </div>
        </header>

        <main class="container">
            <div class="row">
                <div class="col">
                {% for post in posts %}
                    <article class="post">
                        <time class="date">
                            published: {{ post.published_date }}
                        </time>
                        <h2><a href="">{{ post.title }}</a></h2>
                        <p>{{ post.text|linebreaksbr }}</p>
                    </article>
                {% endfor %}
                </div>
            </div>
        </main>
    </body>
</html>
~~~
Potom v **base.html**, nahraďte svoju časť <**body**> (všetko medzi <**body**> a <**/body**>) týmto a upravte odstupy:

~~~
<body>
    <header class="page-header">
      <div class="container">
          <h1><a href="/">Django Girls Blog</a></h1>
      </div>
    </header>
    <main class="container">
        <div class="row">
            <div class="col">
            {% block content %}
            {% endblock %}
            </div>
        </div>
    </main>
</body>
~~~

Môžeme si všimnúť, že to nahradilo všetko od **{% for post in posts %}** po **{% endfor %}** s týmto:
~~~
{% block content %}
{% endblock %}
~~~

Je to preto že sme práve vytvorili tzv. block. Pomocou značky-tagu šablóny **{% block %}** sme vytvorili oblasť, do ktorej bude vložený kód HTML. Tento HTML kód bude pochádzať z inej šablóny, a týmto rozširuje túto šablónu ( base.html). O chvíľu si ukážeme, ako na to.

Najprv **base.html** uložme a znova otvorme v editore kódu **blog/templates/blog/post_list.html**. Chystáme sa totiž odstrániť všetko nad **{% for post in posts %}** a pod **{% endfor %}**. Keď tak urobíme súbor post_list.html bude vyzerať takto:

~~~
{% for post in posts %}
    <article class="post">
        <time class="date">
            published: {{ post.published_date }}
        </time>
        <h2><a href="">{{ post.title }}</a></h2>
        <p>{{ post.text|linebreaksbr }}</p>
    </article>
{% endfor %}
~~~

Urobili sme to preto lebo to chceme použiť ako súčasť našej šablóny **post_list.html** za účelom použitia aj pre všetky ostatné bloky nášho obsahu. Tým nastal čas pridať do tohto súboru značky bloku. Pritom chceme aby sa naša značka bloku zhodovala so značkou v našom súbore **base.html**. Tiež chceme, aby tento súbor obsahoval všetok kód, ktorý patrí do našich blokov obsahu. Ak to chcete urobiť, vložíme všetok kód vyššie medzi príkazy **{% block content %}** a **{% endblock %}** čím dostaneme v post_list.html takýto skript:

~~~
{% block content %}
    {% for post in posts %}
        <article class="post">
            <time class="date">
                published: {{ post.published_date }}
            </time>
            <h2><a href="">{{ post.title }}</a></h2>
            <p>{{ post.text|linebreaksbr }}</p>
        </article>
    {% endfor %}
{% endblock %}
~~~

Nakoniec nám ešte zostala jedna vec. A to je to že tieto **dve šablóny musíme spojiť**. O tom totiž **je to rozšírenie šablón**. Urobíme to pridaním značky **extends** na začiatok súboru. 

~~~
{% extends 'blog/base.html' %}

{% block content %}
    {% for post in posts %}
        <article class="post">
            <time class="date">
                published: {{ post.published_date }}
            </time>
            <h2><a href="">{{ post.title }}</a></h2>
            <p>{{ post.text|linebreaksbr }}</p>
        </article>
    {% endfor %}
{% endblock %}
~~~

To je všetko. Uložme súbor a skontrolujme, či náš web stále správne funguje.

Poznámka: Ak sa zobrazí chyba TemplateDoesNotExist, znamená to to, že neexistuje žiadny súbor blog/base.html a v konzole máte spustený runserver. Skúste ho zastaviť (stlačením Ctrl+C – kláves Control a C spolu) a znovu reštartovať spustením príkazu python manage.py runserver.

## Rozširovanie našej webovej aplikácie

Keď sme dokončili všetky kroky potrebné na vytvorenie našej webovej stránky t.j vieme, **ako napísať model, URL, views a šablónu**. A vieme tiež, **ako urobiť našu webovú stránku pomocou HTML a CSS peknou**. Nastal čas na rozširovanie našej webovej stránky.

Prvá vec, ktorú v našom blogu potrebujeme, je stránka na zobrazenie iba jedného vybraného príspevku. Model príspevku už máme (Post), takže sa môžeme vrátiť k súboru models.py.

### Vytvorenie odkazu na šablónu pre zobrazenie podrobností príspevku

Začneme pridaním odkazu do súboru **blog/templates/blog/post_list.html**. Otvorte ho v editore kódu a zatiaľ by jeho obsah mal vyzerať takto:
~~~
{% extends 'blog/base.html' %}

{% block content %}
    {% for post in posts %}
        <article class="post">
            <time class="date">
                {{ post.published_date }}
            </time>
            <h2><a href="">{{ post.title }}</a></h2>
            <p>{{ post.text|linebreaksbr }}</p>
        </article>
    {% endfor %}
{% endblock %}
~~~

Chceme mať odkaz na stránku s podrobnosťami o príspevku cez názov príspevku ktorý sa nachádza v zozname príspevkov. Zmeňme teda 
~~~
<h2><a href="">{{ post.title }}</a></h2>
~~~
 tak, aby sa odkazovalo na stránku s podrobnosťami o príspevku:
~~~
<h2><a href="{% url 'post_detail' pk=post.pk %}">{{ post.title }}</a></h2>
~~~

Žiada sa však, aby sme konštrukciu **{% url 'post_detail' pk=post.pk %}** vysvetlili. Ako možno tušíte zápis medzi **{% %}** znamená, že používame značky šablón Django. Tentokrát ale použijeme taký, ktorý nám vytvorí URL adresu. URL adresu na stránku detailov príspevku.

Zápis **post_detail** znamená, že Django bude očakávať URL zo súboru **blog/urls.py** kde bude mať meno **name=post_detail**

A čo takto použiť **pk=post.pk** ? **pk** je totiž skratka pre **primárny kľúč**, čo je jedinečný identifikátor pre každý záznam v databáze. Každý model Django má pole, ktoré slúži ako jeho primárny kľúč, a nech už má akýkoľvek iný názov, môže byť tiež označovaný ako „pk“. Pretože sme v našom modeli nešpecifikovali primárny kľúč pre **Post**, Django nám ho vytvorí (štandardne je to pole s názvom „id“ obsahujúce číslo, ktoré sa zvyšuje pre každý záznam, t.j. nadobúda hodnoty 1, 2, 3). Pridá nám ho ako pole na každý náš príspevok. **K primárnemu kľúču pristupujeme zápisom post.pk**, je to rovnakým spôsobom, akým pristupujeme v našom objekte **Post** aj k iným poliam ( napr. title, author, atď.).

Keď prejdeme v tomto štádiu vývoja na adresu http://127.0.0.1:8000/, zobrazí sa chyba (podľa očakávania, pretože ešte nemáme pre post_detail ani URL adresu ani view ). Bude to vyzerať nejako takto:

![](/obrazky/djangogirls19.png)

### Vytvorenie URL adresy pre zobrazenie (views) podrobností príspevku

Poďme vytvoriť **urls.py** v ktorom umiestníme URL pre naše zobrazenie **post_detail**. Pritom 
chceme, aby sa podrobnosti nášho prvého príspevku zobrazovali na adrese ktorá bude mať takýto tvar URL : http://127.0.0.1:8000/post/1/

V súbore **blog/urls.py** zadáme URL adresu, ktorá nasmeruje Djanga na views s názvom **post_detail** a to zobrazí celý príspevok blogu. Otvorte súbor **blog/urls.py** v editore kódu a pridajme do neho riadok **path('post/<int:pk>/', views.post_detail, name='post_detail')**, tak aby súbor vyzeral takto:

~~~
from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
]
~~~

Časť **post/<int:pk>/** špecifikuje vzor URL adresy čo si vysvetlíme v ďalšom:

* post/ znamená, že URL adresa by mala začínať slovom **post**, za ktorým nasleduje znak **/** .
* <int:pk> – vyjadruje trochu zložitejšiu časť. Znamená to, že Django očakáva celočíselnou hodnotu a prenesie ju do views ako premennú s názvom **pk** (ide o spomínaný primary key).
* / – potrebujeme znova umiestniť pred dokončením URL adresy.
* 
To znamená, že ak vstúpime v prehliadači na adresu http://127.0.0.1:8000/post/5/, Django pochopí, že hľadáme views s názvom **post_detail** a prenesie do príslušnej šablóny informácie (zázanam z DB tabuľky), ktoré prislúchajú tomuto views s identifikátorom **pk** rovnému hodnote číslo 5 (t.j. 5.-mu riadku tabuľky)

Do **blog/urls.py ** sme teda pridali nový vzor URL adresy. Obnovme stránku: http://127.0.0.1:8000/ a opäť zistíme že server prestal bežať. Pozrieme sa na konzolu a ako sme mohli po zásahu do url.py očakávať je tu ďalšia chyba.

~~~
return _bootstrap._gcd_import(name[level:], package, level)
  File "<frozen importlib._bootstrap>", line 1030, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1007, in _find_and_load
  File "<frozen importlib._bootstrap>", line 986, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 680, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 850, in exec_module
  File "<frozen importlib._bootstrap>", line 228, in _call_with_frames_removed
  File "/Users/ola/djangogirls/blog/urls.py", line 6, in <module>
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
AttributeError: module 'blog.views' has no attribute 'post_detail'
~~~

Chyba nám napovedá že problém sa týka views a upozorňuje nás na potrebu pridať nový views pre post_detail.

### Vytvorenie views na podrobnosti príspevku

Tento krát je nášmu views priradený ďalší parameter - **pk**. Náš views ho musí prijať a spracovať. Preto vytvoríme funkciu s návratovou hodnotou, ktorú zadefinujeme ako **def post_detail(request, pk):**. Všimnime si, že tento parameter **pk** musí mať presne rovnaký názov ako ten, ktorý sme zadali v **urls(pk)**. Vynechanie tejto premennej **pk** je nesprávne a bude mať za následok chybu!

Najprv sa budeme zaoberať postupom ako získať len jeden blogový príspevok. Na tento účel môžeme použiť známy <a href="#section3">QuerySets</a> ako je tento:
~~~
Post.objects.get(pk=pk)
~~~

Ale tento kód má problém. Ak tam nie je žiadne **Post** s daným primary key (**pk**), dostaneme veľkú chybu.

![](/obrazky/djangogirls20.png)

To však nechceme, ale našťastie Django prichádza s niečím, čo to zvládne za nás. Je to pomoc pri ošetrení chyby **get_object_or_404**. V prípade, že tam nie je **Post** s daným **pk**, zobrazí sa oveľa krajšia stránka, **Page Not Found 404** ktorá nás nasmeruje na príčinu chyby.

![](/obrazky/djangogirls21.png)

Tento nástroj, ktorý nám Django poskytuje nám umožní vytvoriť aj svoju vlastnú stránku na hlásenie chyby (s inou správou ako Page not found) a urobiť ju tak ako chceme. To v+sak teraz nebude predmetom nášho riešenia a tak túto tému preskočíme.

Čo je dôležitejšie je to aby sme pridali do nášho súboru **views.py** nový views.

V **blog/urls.py** sme vytvorili pravidlo URL s názvom **post_detail**, ktoré odkazuje na views s názvom **views.post_detail**. To znamená, že Django bude očakávať funkciu views (zobrazenia) s názvom **post_detail** vo vnútri súboru **blog/views.py**.

Mali by sme preto otvoriť **blog/views.py** v editore kódu a pridať nasledujúci kód za ostatné riadky s from ... import ...:
~~~
from django.shortcuts import render, get_object_or_404
~~~
A na koniec súboru **blog/views.py pridáme náš view (pohľad) :
~~~
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
~~~

Keď obnovíme stránku: http://127.0.0.1:8000/ dostaneme síce známy vizuál, 

![](/obrazky/djangogirls22.png)

ale po nakliknutí na názov príspevku dostaneme zase chybu.

![](/obrazky/djangogirls23.png)

S takouto chybou sme sa však už stretli skôr a tak sa s ňou už vieme vysporiadať. Ak si spomenieme, musíme pridať pre post_detail šablónu!

### Vytvorenie šablóny pre podrobnosti v príspevku

Vytvoríme si súbor s názvom **post_detail.html** v adresári **blog/templates/blog** a otvoríme ho v editore kódu. Potom zadáme nasledujúci kód:

~~~
{% extends 'blog/base.html' %}

{% block content %}
    <article class="post">
        {% if post.published_date %}
            <time class="date">
                {{ post.published_date }}
            </time>
        {% endif %}
        <h2>{{ post.title }}</h2>
        <p>{{ post.text|linebreaksbr }}</p>
    </article>
{% endblock %}
~~~
Opäť v ňom využijeme base.html. V bloku **content*  chceme zobraziť dátum zverejnenia príspevku (ak existuje), názov príspevku a jeho obsah. Skôr než tak urobíme mali by sme podiskutovať o niektorých dôležitých veciach.

**{% if ... %} ... {% endif %}** je značka šablóny, ktorú môžeme použiť, keď chceme niečo skontrolovať. (Spomínate si if ... else ...zo základov Pythonu ?) V tejto časti chceme napr. skontrolovať, či príspevok **published_date** nie je prázdny. OK, tak obnovme našu stránku a zistime, či je chyba **TemplateDoesNotExist** preč.

![](/obrazky/djangogirls24.png)

## Formuláre s Djangom

Posledná vec, ktorú chceme na našej webovej stránke urobiť, je vytvoriť vhodný spôsob pridávania a úpravy blogových príspevkov. Djangoý **admin** je síce fajn, ale je príliš jednoduchý a je dosť náročné ho prispôsobiť na lepší design. Djangove **forms** však bude vhodnejším riešením rozhrania s užívateľom a budeme s ním môcť robiť takmer všetko čo potrebujeme.

Zaujímavou vlastnosťou na formulároch Django je aj to, že môžeme ho vždy vytvárať od samotného začiatku alebo môžeme vytvoriť formulár ktorý sa prostredníctvom **ModelForm** uloží do modelu k opakovanému použitiu. A to je presne to, čo chceme urobiť. Vytvoriť formulár pre náš model **Post**.

Ako každá dôležitá časť Djanga, aj formuláre majú svoj vlastný súbor ktorým je **forms.py**. Ten vytvoríme v adresári blog .

~~~
DJANGOGIRLS
│
blog
   └── forms.py
~~~

Kód, ktorý do neho zapíšeme bude vyzerať nasledovne:

~~~
from django import forms
from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)
~~~

Najprv musíme importovať formuláre Django ( **from django import forms**) a náš model **Post** ( from .models import Post).

**PostForm**, ako pravdepodobne tušíte, je názov nášho formulára. V tejto súvislosti musíme Djangovi povedať, že tento formulár je **ModelForm** takže Django zabezpečí že za to bude zodpovedný **forms.ModelForm** .

Ďalej budeme pracovať s **class Meta**, kde povieme Djangovi, ktorý model by sa mal použiť na vytvorenie nášho formulára ( **model = Post**).

Nakoniec ešte musíme povedať povedať, ktoré pole (polia) databázovej tabuľky by mali byť v našom formulári napĺňané. V tomto scenári chceme len **title**, **text**, **author** ktorým je osoba, ktorá je práve prihlásená (napr. Vy) a **created_date** by mal byť už vytváraný automaticky pri inicializácii písania príslušného príspevku.

Všetko, čo teraz musíme urobiť, je použiť formulár vo views a prepojiť ho na šablónu. Ešte raz si teda budeme musieť v urls.py vytvoriť na stránku odkaz, zadať URL, vytvoriť views a šablónu.

### Odkaz na stránku s formulárom

Pred pridaním odkazu potrebujeme na naše stránky zabudovať nejaké ikony, ktoré použijeme ako tlačidlá pre aktivovanie odkazu. Pre tento návod si stiahneme [súbor-earmark-plus.svg](https://icons.getbootstrap.com/icons/file-earmark-plus/) a uložíme si ho do priečinka **blog/templates/blog/icons/** ktorý si tu najprv  musíme vytvoriť napr. prieskumníkom. Stiahnutý súbor ikony má základný rozmer ktorý je pre naše účely veľmi malý. Rozmery ikony zväčšíme zmenou hodnôt v súbore file-earmark-plus.svg napr. na hodnoty width="50" height="50" a v súbore pencil-fill.svg na hodnoty width="15" height="15"

Je čas otvoriť v editore kódu **blog/templates/blog/base.html**. Teraz môžeme použiť tento súbor ikony v základnej šablóne nasledovne. Vo  vnútri sekcie **header** a v elemente **div** pridáme pred  **h1**  odkaz:

~~~
<a href="{% url 'post_new' %}" class="top-menu">
    {% include './icons/file-earmark-plus.svg' %}
</a>
~~~

Dohodnime sa že náš nový view by bolo vhodné nazvať **post_new**. Ikony nám poskytuje [Bootstrap](https://icons.getbootstrap.com/) vo formáte SVG a tá naša ktorú sme si stiahli zobrazí stránku so znamienkom plus. 

![](/obrazky/djangogirls25.png)

Použijeme direktívu šablóny Django s názvom **include**. Tým sa vloží zo súboru kód ikony  do šablóny Django. Webový prehliadač už potom vie, ako s týmto typom obsahu zaobchádzať bez akéhokoľvek ďalšieho spracovania.

Všetky ikony Bootstrap si môžete stiahnuť [tu](https://github.com/twbs/icons/releases/download/v1.1.0/bootstrap-icons-1.1.0.zip). Súbor sa rozbalí a všetky obrazové súbory SVG sa skopírujú do nového priečinka **blog/templates/blog/icons**. Týmto spôsobom môžete získať prístup k ikone, ako je file-earmark-plus.svg alebo pencil-fill.svg ak použijeme k súboru danú cestu **blog/templates/blog/icons/file-earmark-plus.svg**

Po úprave riadku by váš HTML súbor **blog/templates/blog/base.html** mal teraz vyzerať takto:

~~~
{% load static %}
<!DOCTYPE html>
<html>
    <head>
        <title>Django Girls blog</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Lobster&subset=latin,latin-ext">
        <link rel="stylesheet" href="{% static 'css/blog.css' %}">
    </head>
    <body>
        <header class="page-header">
            <div class="container">
                <a href="{% url 'post_new' %}" class="top-menu">
                    {% include './icons/file-earmark-plus.svg' %}
                </a>
                <h1><a href="/">Django Girls Blog</a></h1>
            </div>
        </header>
        <main class="content container">
            <div class="row">
                <div class="col">
                    {% block content %}
                    {% endblock %}
                </div>
            </div>
        </main>
    </body>
</html>
~~~

Po uložení a obnovení stránky http://127.0.0.1:8000 sa nám zobrazí známa chyba **NoReverseMatch at /**.

### post_new v urls.py

Otvoríme **blog/urls.py** v editore kódu a pridáme riadok:
~~~
path('post/new/', views.post_new, name='post_new'),
~~~
aby konečný kód bude vyzerať takto:
~~~
from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
]
~~~
Po obnovení stránky keďže nemáme views **post_new** implementované, tak sa nám zobrazí **AttributeError** . Podme to hneď vyriešiť.

### post_new vo views.py

Je čas otvoriť v editore kódu súbor **blog/views.py** a pridať nasledujúce riadky k zvyšným riadkom **from ... import ...**:
~~~
from .forms import PostForm
~~~
A potom pre náš views pridať do views.py funkciu:
~~~
def post_new(request):
    form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
~~~

Na vytvorenie nového formulára **Post** musíme zavolať **PostForm()** a odovzdať ho šablóne. K tomuto views sa ešte vrátime, ale teraz si najprv vytvoríme šablónu formulára.

### post_new šablóna

V adresári **blog/templates/blog** musíme vytvoriť súbor **post_edit.html** a otvoriť ho v editore kódu. Aby formulár fungoval, potrebujeme niekoľko vecí:

* Musíme najprv formulár zobraziť. Môžeme to napríklad urobiť pomocou **{{ form.as_p }}**.
* Vyššie uvedený riadok je potrebné zabaliť do HTML prvku formulára: **<form method="POST">...</form>**.
* Potrebujeme tlačítko Save (Uložiť) na uloženie formuláru. Urobíme to pomocou HTML tlačidla : **<button type="submit">Save</button>**.
* A nakoniec, hneď za úvodnú značku **<form ...>** musíme pridať **{% csrf_token %}**. Je to veľmi dôležité, pretože to robí vaše formuláre bezpečnými! Ak na tento kód zabudnete,keď sa pokúsite uložiť formulár, Django sa bude takto sťažovať :
![](/obrazky/djangogirls26.png)

Poďme sa teda pozrieť, ako by mal vyzerať HTML kód v **post_edit.html** :

~~~
{% extends 'blog/base.html' %}

{% block content %}
    <h2>New post</h2>
    <form method="POST" class="post-form">{% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="save btn btn-secondary">Save</button>
    </form>
{% endblock %}
~~~
Ak stránku refrešneme mali by sme dostať takýto dizajn formulára :

![](/obrazky/djangogirls27.png)

Ale, to ešte nie je všetko. Keď niečo zadáte do polí **title** a **text** a pokúsite sa to uložiť, čo sa stane?

Nič! Opäť sme na tej istej stránke, náš text je preč... a nepridal sa žiadny nový príspevok. Čo sa teda pokazilo? Odpoveď znie: že nič. Z nášho pohľadu musíme len ešte niečo doplniť aby to fungovalo ako má.

### Uloženie vyplneného formulára

Znova otvoríme v editore kódu **blog/views.py** a v súčasnosti v ňom pre post_new máme iba nasledovné :
~~~
def post_new(request):
    form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
~~~

Keď odošleme formulár, vrátime sa späť do rovnakého zobrazenia, ale tentoraz máme v **request** nejaké ďalšie údaje, presnejšie v **request.POST**(pomenovanie nemá nič spoločné s blogovým príspevkom „post“, súvisí to so skutočnosťou, že „zverejňujú“ údaje). Pamätáte si, ako v HTML súbore  **<form>** mala naša definícia premennú **method="POST"**? Všetky polia z formulára sú teraz v **request.POST**. Nemali by ste premenovať **POST** na nič iné, lebo jediná platná hodnota pre **method** je **GET**. Ale tu nemáme priestor vysvetľovať, v čom spočíva rozdiel.

Takže podľa nášho zámeru musíme zvládnuť dve samostatné situácie: 
* ***po prvé***, keď prvýkrát vstúpime na stránku a chceme prázdny formulár, a 
* ***po druhé***, keď sa vrátime do zobrazenia so všetkými údajmi formulára, ktoré sme práve zadali. 

Musíme teda pridať podmienku a použijeme na to **if**.
~~~
if request.method == "POST":
    [...]
else:
    form = PostForm()
~~~

Je to čas doplniť bodky [...]. Ak **method** je POST, potom chceme zostaviť **PostForms** s údajmi z formulára. Čo urobíme nasledovne:

~~~
form = PostForm(request.POST)
~~~

Ďalšia vec je skontrolovať, či je formulár správny (t.j. či sú všetky povinné polia nastavené a neboli odoslané žiadne nesprávne hodnoty). Robíme to validačným príkazom **form.is_valid()** v súbore blog/views.py. Skontrolujeme, či je formulár platný a ak áno, môžeme ho uložiť.

~~~
if form.is_valid():
    post = form.save(commit=False)
    post.author = request.user
    post.published_date = timezone.now()
    post.save()
~~~

V zásade tu riešime dve veci: 
* chceli by sme formulár uložiť s tým že bude pridaný **author**. Keďže vo **form.save** ale nebolo na to žiadne pole a toto pole je povinné musíme najprv vyriešiť tento problém. 
* **commi=False** znamená, že model **Post** ešte nemôžeme uložť, ale najprv musíme pridať autora. 

Väčšinu budeme používať **form.save** bez **commit=False**, ale v tomto prípade ho musíme zadať. **post.save()** zachová zmeny (počká na pridanie autora) a až potom sa vytvorí nový blogový príspevok.

Nakoniec by bolo dobré, keby sme mohli okamžite prejsť na stránku **post_detail** nášho novovytvoreného blogového príspevku. No na to potrebujeme ešte jeden import:

~~~
from django.shortcuts import redirect
~~~

Pridajte ho na úplný začiatok súboru **blog/views.py**. A teraz môžeme povedať, „prejdite na stránku **post_detail** pre novovytvorený príspevok“:

~~~
return redirect('post_detail', pk=post.pk)
~~~

**post_detail** je názov zobrazenia, do ktorého chceme ísť. Pamätáte si, že toto ***zobrazenie*** vyžaduje premennú **pk**. Na jej odovzdanie do views používame **pk=post.pk**, kde **post** je novovytvorený blogový príspevok.

Celá definícia post_new vo views potom vyzerá takto :
~~~
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
~~~

Prejdite na stránku http://127.0.0.1:8000/post/new/ a uvidíme, či to bude fungovať. Pridajte **title**, **text** a uložte to. Nový blogový príspevok je pridaný a my sme presmerovaní na stránku **post_detail**.

Možno ste si všimli, že pred uložením nastavujeme dátum zverejnenia automaticky. Neskôr si vytvoríme na to tlačitko "Publikovať".

Keďže sme nedávno použili admin rozhranie Django, systém si momentálne myslí, že sme stále prihlásení. Existuje niekoľko situácií, ktoré môžu viesť k odhláseniu (zatvorenie prehliadača, reštartovanie databázy atď.). Ak pri vytváraní príspevku zistíte, že sa vám zobrazujú chyby týkajúce sa chýbajúceho prihláseného používateľa, prejdite na stránku správcu http://127.0.0.1:8000/admin a znova sa prihláste. Týmto sa problém dočasne vyrieši. 

![](/obrazky/djangogirls28.png)

### Overenie funkčnosti formulára

Teraz si ukážeme, aké skvelé sú formuláre vytvorené pomocou Djanga. Blogový príspevok musí mať polia **title** a **text**. V našom modeli **Post** sme nepovedali, že tieto polia (na rozdiel od poľa **published_date**) nie sú povinné. Takže Django na základe toho štandardne očakáva, že budú nejako nastavené do východzieho stavu. Pokúste sa teda uložiť formulár bez **title** a **text** a pozrime čo sa staneˇ.

![](/obrazky/djangogirls29.png)

> Django sa postará o overenie správnosti všetkých polí v našom formulári.

### Úprava nášho formulára

Teraz už vieme, ako pridať nový príspevok. Čo ak však chceme upraviť už existujúci príspevok ? Toto je veľmi podobné tomu, čo sme práve urobili, ale má to svoje odlišnosti. Poďme rýchlo vytvoriť dôležité veci.

Najprv si stiahneme a do adresára ikons si uložíme ikonu, ktorá predstavuje tlačidlo úprav. Stiahnite si súbor **pencil-fill.svg** a uložte ho do umiestnenia **blog/templates/blog/icons/**.

Otvorte **blog/templates/blog/post_detail.html** v editore kódu a pridajte nasledujúci kód do prvku **article**:

~~~
<aside class="actions">
    <a class="btn btn-secondary" href="{% url 'post_edit' pk=post.pk %}">
      {% include './icons/pencil-fill.svg' %}
    </a>
</aside>
~~~

takže celá šablóna post_detail.html bude vyzerať takto:

~~~
{% extends 'blog/base.html' %}

{% block content %}
    <article class="post">
        <aside class="actions">
            <a class="btn btn-secondary" href="{% url 'post_edit' pk=post.pk %}">
                {% include './icons/pencil-fill.svg' %}
            </a>
        </aside>
        {% if post.published_date %}
            <time class="date">
                Publikované: {{ post.published_date }}&nbsp&nbsp
            </time>
        {% endif %}
        <h2>{{ post.title }}</h2>
        <p>{{ post.text|linebreaksbr }}</p>
    </article>
{% endblock %}
~~~
Otvorte v editore kódu **blog/urls.py** a pridajte tento riadok:
~~~
 path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
~~~

Šablónu **blog/templates/blog/post_edit.html** použijeme znova, a posledná chýbajúca vec je ***view***. Otvorme v editore kódu **blog/views.py** a na úplný koniec súboru pridajme toto:

~~~
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
~~~

Tento odstavec vyzerá takmer rovnako ako náš pohľad **post_new**. Ale nie je to celkom tak. 
* Po prvé, z **urls** odovzdáme ďalší parameter **pk**. 
* Po druhé dostaneme model **Post**, s ktorým chceme upraviť **get_object_or_404(Post, pk=pk)** a potom, 
* keď vytvoríme formulár, odovzdáme tento príspevok pri ukladaní formulára ako **instance** …

~~~
form = PostForm(request.POST, instance=post)
~~~
…a keď sme práve otvorili formulár s týmto príspevkom na úpravu:
~~~
form = PostForm(instance=post)
~~~

Vyskúšajme, či to funguje a poďme na stránku **post_detail**. Vedľa príspevku by malo byť tlačidlo úprav s ceruzkou:

![](/obrazky/djangogirls30.png)

a keď naň klikneme, zobrazí sa nám formulár s príspevkom na našom blogu:

![](/obrazky/djangogirls31.png)

Teraz tu môžeme zmeniť názov alebo text a tieto zmeny uložiť.

Viacej informácií o formulároch Django si možno prečítať v dokumentácii: https://docs.djangoproject.com/en/3.2/topics/forms/

## Bezpečnosť našich stránok

Možnosť vytvárať nové príspevky kliknutím na odkaz je úžasná. Ale práve teraz bude môcť každý, kto navštívi vašu stránku, vytvoriť nový blogový príspevok, a to pravdepodobne nie je niečo čo by sme chceli. Preto zatiaľ kým nebudeme mať implementovanú funkciu prihlásenia registrovaného užívateľa, to urobme tak, aby sa tlačítko zobrazovalo iba vám a nikomu inému.

Otvorte v editore kódu **blog/templates/blog/base.html** a nájdite vo vnútri **header** prvok **div**, ktorý sme tam predtým vložili. Malo by to vyzerať takto:

~~~
<a href="{% url 'post_new' %}" class="top-menu">
    {% include './icons/file-earmark-plus.svg' %}
</a>
~~~

K tomuto textu pridáme ďalšiu značku **{% if %}**, vďaka ktorej sa odkaz zobrazí iba užívateľom, ktorí sú prihlásení s privilégiami správcu. Práve teraz ste to len vy. Zmeňte prvok <**a**> tak, aby vyzeral takto:

~~~
{% if user.is_authenticated %}
    <a href="{% url 'post_new' %}" class="top-menu">
        {% include './icons/file-earmark-plus.svg' %}
    </a>
{% endif %}
~~~

To **{% if %}** spôsobí, že sa odkaz odošle do prehliadača iba v prípade, že používateľ, ktorý stránku požaduje, je prihlásený. Vytváranie nových príspevkov to úplne nechráni, ale ako prvý krok ochrany je to celkom dobré. Problematike bezpečnosti sa budeme venovať v ďalších častiach.

Podobný problém sa týka aj ikony úprav, ktorú sme práve pridali na našu stránku s podrobnosťami príspevku. Tiež by sme tam potrebovali pridať rovnakú zmenu aby iní ľudia nenemohli upravovať existujúce príspevky a aby to bola iba výsada administrátora alebo vlastníka príspevku.

Otvorte preto v editore kódu **blog/templates/blog/post_detail.html** a nájdite tento riadok:

~~~
<a class="btn btn-secondary" href="{% url 'post_edit' pk=post.pk %}">
    {% include './icons/pencil-fill.svg' %}
</a>
~~~
Následne ho zmeňme na toto:

~~~
{% if user.is_authenticated %}
     <a class="btn btn-secondary" href="{% url 'post_edit' pk=post.pk %}">
        {% include './icons/pencil-fill.svg' %}
     </a>
{% endif %}
~~~

Keďže ste pravdepodobne prihlásení, ak obnovíte stránku, neuvidíte žiadnu zmenu. Preto načítajte stránku v inom prehliadači alebo v okne inkognito (nazývanom „InPrivate“ v systéme Windows Edge) a uvidíte, že odkaz sa nezobrazí a nezobrazí sa ani ikona.

# Rozšírenia funkcionality webovej aplikácie

V rámci rozšírenia funkcionality našej webovej aplikácie sa môžeme napr. zaoberať nasledovnými témami :
***Riešené***
* ***Zvýšenie konfortu práce s aplikáciou***
  * Implementácia vytvárania konceptov
  * Publikovanie konceptov príspevkov
  * Odstránenie príspevku
* ***Zvýšenie bezpečnosti aplikácie***
  * Implementácia prihlasovania užívateľov
* ***Vytvorenie diskusného fóra*** 
  * Komentovanie publikovaných príspevkov 

***Neriešené***
* ***Zavedenie registrácie užívateľov***
* ***Použitie výkonnejšej databázy***
  * Pripojenie databázy PostgreSQL***
* ***Použitie vlastnej domény***
* a pod.

>## Implementácia vytvárania konceptov

Náš blog už prešiel dlhou cestou, ale stále je čo zlepšovať. Ďalej pridáme funkcie pre vytáranie konceptov príspevkov a ich publikovanie. Pridáme aj mazanie príspevkov, ktoré už nechceme.

V súčasnosti, keď vytvárame nové príspevky pomocou nášho formulára ***Nový príspevok***, tak sa príspevok hneď uverejňuje-publikuje. Ak chcete namiesto toho uložiť príspevok ako koncept, odstráňme v **blog/views.py** v metódach **post_new** a **post_edit** tento riadok:

~~~
post.published_date = timezone.now()
~~~
Týmto spôsobom sa nové **príspevky uložia ako koncepty**, ktoré môžeme namiesto toho, aby boli okamžite zverejnené napr. neskôr ešte skontrolovať a až potom publikovať. Všetko, čo teraz k tomu potrebujeme, je spôsob, ako uviesť a zverejniť koncepty.

### Vytvorenie stránky so zoznamom nezverejnených príspevkov

V časti o súboroch dotazov sme vytvorili zobrazenie **post_list**, ktoré zobrazuje iba publikované blogové príspevky (t.j. tie, ktoré nemajú prázdne **published_date**). Niečo podobné môžeme urobiť aj pre koncepty príspevkov.

Pridajme do hlavičky súboru **blog/templates/blog/base.html** odkaz. Náš zoznam konceptov však nechceme zobrazovať každému, preto ho vložíme do kontroly pre autentifikáciu **{% if user.is_authenticated %}**. To už však máme spravené v predchádzajúcej časti, kedy sme na zobrazenie tlačítka použili ikonu Bootstrap file-earmark-plus.svg. Tu je ako ukážka použitá ikona glyphicon-edit z [Bootstrap Glipcon Components](https://www.w3schools.com/bootstrap/bootstrap_ref_comp_glyphs.asp) 

~~~
<a href="{% url 'post_draft_list' %}" class="top-menu"><span class="glyphicon glyphicon-edit"></span></a>
~~~
Ďalej medzi adresy URL v súbore **blog/urls.py** pridávame:
~~~
path('drafts/', views.post_draft_list, name='post_draft_list'),
~~~
a môžeme pre koncept vytvoriť nové zobrazenie v súbore ***blog/views.py** :

~~~
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})
~~~

Riadok **posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')** zabezpečuje, že berieme len nezverejnené príspevky (t.j. tie kde platí **published_date__isnull=True**) a zoraďujeme ich podľa dátumu vytvorenia **created_date( order_by('created_date'))**.

Poslednou častou v **postupnosti urls.py, views.py je samozrejme tempaltes**. Vytvorme súbor **blog/templates/blog/post_draft_list.html ** a pridajte do neho nasledujúce:

~~~
{% extends 'blog/base.html' %}

{% block content %}
    {% for post in posts %}
        <div class="post">
            <p class="date">created: {{ post.created_date|date:'d-m-Y' }}</p>
            <h1><a href="{% url 'post_detail' pk=post.pk %}">{{ post.title }}</a></h1>
            <p>{{ post.text|truncatechars:200 }}</p>
        </div>
    {% endfor %}
{% endblock %}
~~~

Vyzerá to veľmi podobne ako u nášho post_list.html. Teraz, keď prejdete na, http://127.0.0.1:8000/drafts/ uvidíme zoznam nezverejnených príspevkov.

***Naše prvé rozšírenie funkcionality našej webovej aplikácie blogu je hotové!***

>## Publikovanie konceptov  príspevkov

Bolo by dobré mať na stránke s podrobnosťami o blogovom príspevku tlačítko, ktoré príspevok okamžite zverejní. Otvorme súbor **blog/templates/blog/post_detail.html** a zmeňme tieto riadky:

~~~
{% if post.published_date %}
    <div class="date">
        Publikované: {{ post.published_date }}
    </div>
{% endif %}
~~~
na takéto
~~~
{% if post.published_date %}
    <div class="date">
        Publikované: {{ post.published_date }}
    </div>
{% else %}
    <a class="btn btn-secondary" href="{% url 'post_publish' pk=post.pk %}">Publikuj</a>
{% endif %}
~~~

Pridali sme sem riadok
~~~
{% else %}
~~~
To znamená že ak nie sú splné podmienky z 
~~~
{% if post.published_date %}
~~~
t.j. ak nie je zadaný dátum publikovania 
`published_date`, a potom chceme aby sa vykonal riadok
~~~
<a class="btn btn-secondary" href="{% url 'post_publish' pk=post.pk %}">Publikuj</a>
~~~

Pamätajme však že do `url` sme vložili premennú **pk**

A nastal čas aby sme v súbore **blog/urls.py** doplnili URL adresu:

~~~
path('post/<pk>/publish/', views.post_publish, name='post_publish'),
~~~
a nakoniec ako vždy pohľad musíme vytvoriť zobrazenie pre **post_publish** v súbore **blog/views.py** :

~~~
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)
~~~

Keď sme vytvorili model **Post**, napísali sme metódu **publish**. Vyzeralo to takto:
~~~
def publish(self):
    self.published_date = timezone.now()
    self.save()
~~~
a teraz to konečne môžeme použiť. Po zverejnení príspevku sme okamžite presmerovaní na stránku **post_detail**.

![](/obrazky/djangogirls32.png)

Posledným krokom bude pridanie tlačidla Odstrániť.

>## Odstránenie príspevku

Opäť otvoríme súbor **blog/templates/blog/post_detail.html** a pridáme tento riadok hneď pod riadkom s tlačidlom Edit (Upraviť) :

~~~
<a class="btn btn-secondary" href="{% url 'post_remove' pk=post.pk %}">{% include './icons/trash-fill.svg' %}</span></a>
~~~

Teraz potrebujeme adresu URL v súbore **blog/urls.py** :

~~~
path('post/<pk>/remove/', views.post_remove, name='post_remove'),
~~~
V ďalšom opäť k tomu vytvoríme zobrazenie. Otvorme preto súbor **blog/views.py** a pridajte tento kód:

~~~
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')
~~~

Jedinou funkcionalitou tejto časti je skutočne odstrániť blogový príspevok. Každý model Django môže byť odstránený pomocou **.delete()**. Prejdite na niektorú stránku s príspevkom a skúste ju odstrániť!

![](/obrazky/djangogirls33.png)

>## Implementácia prihlasovania užívateľov

Doteraz sme pri prístupe k webovej aplikácie nemuseli použiť meno a ani svoje heslo. Okrem prípadu keď sme použili administrátorské rozhranie. To ale znamená, že ktokoľvek môže pridávať alebo upravovať príspevky vo vašom blogu. Pokiaľ nechceme, aby len tak niekto písal na náš blog, tak s tým niečo musíme urobiť.

#### Autorizácia pridávania/úpravy príspevkov

Najprv zabezpečíme nasledovné veci. Naše zobrazenia **post_new**, **post_edit** a **post_draft_list** budeme chrániť tak, aby k nim mali prístup iba prihlásení používatelia. Django má na to niekoľko vhodných nástrojov, ktoré sa nazývajú **dekoratóri**. Teraz sa nebudeme zaoberať technickými detailami. O nich si môžeme niečo prečítať neskôr. Dekoratóri, ktoré budeme používať, sa dodávajú v module Django a volajú sa **post_remove post_publish django.contrib.auth.decorators login_required**

Takže upravme najprv naše **blog/views.py** a pridajme hore spolu pod zvyšok importov tieto riadky:

~~~
from django.contrib.auth.decorators import login_required
~~~

Potom pred každý zo zobrazení **post_new**, **post_edit**, **post_draft_list, post_remove a post_publish**, pridajme riadok ktorý sa nazýva dekorátor :
~~~
@login_required
~~~
a takto ich doplňme  

~~~
@login_required
def post_new(request):
    [...]
~~~
To je všetko! Teraz sa pokúsme získať prístup http://127.0.0.1:8000/post/new/ a všimnúť si rozdiel.

Ak sme dostali prázdny formulár, pravdepodobne sme stále prihlásení ako správca. Prejdite preto na http://127.0.0.1:8000/admin/logout/ odhláste sa a potom sa znovu prihláste na http://127.0.0.1:8000/post/new .

Mali by sme ale dostať jednu z našich známich chýb o ktorej už vieme ako ju odstrániť. Dekorátor, ktorý sme pridali, vás totiž presmeruje na prihlasovaciu stránku, ale keďže ešte táto stránka nie je k dispozícii, zobrazí sa chyba ktorú už poznáme že „Stránka sa nenašla (404)“.

Dosiahli sme časť nášho cieľa. Teraz už iní ľudia nemôžu vytvárať príspevky na našom blogu. Bohužiaľ pokiaľ sa neprihlásime ako admin, tak už nemôžeme vytvárať príspevky ani my. To ale v ďalšom napravíme.

### Prihlasovanie užívateľov - LogIn resp. SignIn

Teraz by sme sa mohli pokúsiť urobiť pár vecí na implementáciu užívateľov, hesiel a autentifikácie. Ale urobiť to správne nie je jednoduché. Keďže ale v Djangu pojde iba o to aby sme tieto poskytované autentifikačné nástroje iba použili.

V našom súbore **mysite/urls.py** najprv pridajme adresu URL **path('accounts/login/', views.LoginView.as_view(), name='login')** a potom hore **from django.contrib.auth import views**. Takže tento súbor by mal teraz vyzerať takto:

~~~
from django.urls import path, include
from django.contrib import admin

from django.contrib.auth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
]
~~~

Potom potrebujeme šablónu pre prihlasovaciu stránku, takže vytvorte adresár **blog/templates/registration** a súbor v jeho vnútri s názvom **login.html**:

~~~
{% extends "blog/base.html" %}

{% block content %}
    {% if form.errors %}
        <p>Vaše meno užívateľa a heslo nie je správne. Prosím skúste to znovu.</p>
    {% endif %}

    <form method="post" action="{% url 'login' %}">
    {% csrf_token %}
        <table>
        <tr>
            <td>{{ form.username.label_tag }}</td>
            <td>{{ form.username }}</td>
        </tr>
        <tr>
            <td>{{ form.password.label_tag }}</td>
            <td>{{ form.password }}</td>
        </tr>
        </table>

        <input type="submit" value="login" />
        <input type="hidden" name="next" value="{{ next }}" />
    </form>
{% endblock %}
~~~

Ako uvidíme, aj táto funkcionalita využíva našu základnú šablónu pre celkový vzhľad nášho blogu.

Je to dobré, že to funguje jednoducho a že nemusíme riešiť manipuláciu s odoslaním formulára ani heslá a ich zabezpečenie. Zostáva nám urobiť len pár vecí medzi ktorými je pridanie nastavenia v **mysite/settings.py** :

~~~
LOGIN_REDIRECT_URL = '/'
~~~
čo spôsobí že pri priamom prístupe na prihlasovaciu stránku, presmeruje úspešné prihlásenie na index najvyššej úrovne (t.j. domovskú stránku nášho blogu).

### Zlepšenie lyuotu - rozloženia prvkov

Keď už máme všetko nastavené tak, že tlačítka na pridávanie a úpravu príspevkov uvidia len oprávnení užívatelia (teda napr. my) môžeme pokračovať ďalej. Teraz sa chceme uistiť, že prihlasovacie tlačítko sa zobrazí aj všetkým ostatným užívatelom ktorí sa dostanú na počiatočnú domovskú stránku.

Pridáme prihlasovacie tlačidlo, a tým zistíme aká je situácia:
~~~
    <a href="{% url 'login' %}" class="top-menu">{% include './icons/lock-fill.svg' %}</a>
~~~

Na to potrebujeme upraviť šablóny. Tak si otvoríme **blog/templates/blog/base.html** a zmeníme časť medzy značkami <**body**> tak, aby vyzerala takto:

~~~
<body>
        <div class="container">
            {% if user.is_authenticated %}
                <a href="{% url 'post_new' %}" class="top-menu">{% include './icons/file-earmark-plus.svg' %}</a>
<!--                <a href="{% url 'post_draft_list' %}" class="top-menu">{% include './icons/pencil-fill.svg' %}</a> -->
            {% else %}
                <a> Klikom na zámok sa môžete prihlásiť --></>
                <a href="{% url 'login' %}" class="top-menu">{% include './icons/lock-fill.svg' %}</a>    
            {% endif %}
            <h1><a href="/">Django Girls Blog</a></h1>
        </div>

        <div class="content container">
            <div class="row">
                <div class="col">
                    <div class="col-md-8">
                        {% block content %}
                        {% endblock %}
                    </div>
                </div>    
            </div>
        </div>
    </body>
~~~

Šablóna týmto obsahuje podmienku **if**, ktorá kontroluje overených používateľov na to aby pre nich umožnila zobrazenie tlačítok pre pridanie a úpravy príspevkov. V opačnom prípade sa zobrazí iba tlačítko prihlásenia.

### Niečo viac o overených užívateloch

Keď už sme pri autentifikácii, pridáme do našich šablón trochu logiky. Najprv pridáme nejaké podrobnosti, ktoré sa zobrazia, keď už sme prihlásení. Upravme **blog/templates/blog/base.html** takto:

~~~
<div class="page-header">
    {% if user.is_authenticated %}
        <a href="{% url 'post_new' %}" class="top-menu"><span class="glyphicon glyphicon-plus"></span></a>
        <a href="{% url 'post_draft_list' %}" class="top-menu"><span class="glyphicon glyphicon-edit"></span></a>
        <p class="top-menu">Vítaj {{ user.username }} <small>(<a href="{% url 'logout' %}">Log out</a>)</small></p>
    {% else %}
        <a href="{% url 'login' %}" class="top-menu"><span class="glyphicon glyphicon-lock"></span></a>
    {% endif %}
    <h1><a href="/">Django Girls Blog</a></h1>
</div>
~~~

To nám pridáva privítanie užívateľa "Vítaj ***<username>*** ", ktoré nám aj napovie pod akým menom sme prihlásený a potvrdí že sme prešli overením. Tiež nám to pridáva odkaz na odhlásenie z blogu, avšak táto funkcia nám ešte nefunguje. Poďme ju teda doplniť.

Už sme zistili že Django prihlásenie zvládne a že sa na neho môžeme spoliehať. Tak uvidíme, či Django za nás zvládne aj odhlásenie. Skontrolujme stránku dokumentácie Djanga https://docs.djangoproject.com/en/2.0/topics/auth/default/ či tam nie je v súvislosti s touto problematikou nejaká aktualizácia.

V ďalšom kroku pridáme URL adresu do **mysite/urls.py**, ktorá bude smerovať na zobrazenie Django pre odhlásenie (tj **django.contrib.auth.views.logout**) a ktorá bude vyzerať takto:

~~~
from django.urls import path, include
from django.contrib import admin

from django.contrib.auth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(next_page='/'), name='logout'),
    path('', include('blog.urls')),
]
~~~

Nuž a to je zatiaľ všetko. Ak sme dodržali všetky vyššie uvedené pokyny získali sme webovú aplikáciu pri ktorej
* na prihlásenie potrebujeme užívateľské meno a heslo,
* ak chcete pridávať, upravovať, zverejňovať alebo mazať príspevky, musíte byť prihlásený
* a môžete sa aj znova odhlásiť

>## Komentovanie publikovaných príspevkov

Momentálne máme len Post model nami vytvoreného blogu. Čo tak získať spätnú väzbu od jeho čitateľov a nechať ich náš príspevok komentovať čo si o ňom myslia resp. aké majú návrhy, čo o danej veci vedia, čo by poradili, aké riešenia a zdroje by doporučili a pod.

### Vytvorenie modelu blogu s komentármi

Poďme otvoriť súbor **blog/models.py a pripojiť tento kúsok kódu na jeho koniec :

~~~
class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
~~~

Ak si potrebujeme zopakovať, čo znamenajú jednotlivé typy polí, môžeme sa vrátiť ku kapitole o modeloch. V tomto rozšírení funkcionality máme **nový typ poľa**:
~~~
models.BooleanField- ktorý vyjadruje či je pole pravda/alebo nepravda
~~~
Možnosť **related_name** v**models.ForeignKey** nám umožňuje prístup ku komentárom v rámci modelu Post.

### Vytvorenie tabuľky pre modely v databáze

Teraz je čas pridať náš model komentárov do databázy. Aby sme to urobili, musíme Djangovi povedať, že sme v našom modeli urobili zmeny. Zadajte do Git Bash-u **python manage.py makemigrations blog** . Výstup by ste mali vidieť v takejto podobe :

~~~
(myvenv) ~/djangogirls$ python manage.py makemigrations blog
Migrations for 'blog':
  0002_comment.py:
    - Create model Comment
~~~

Môžete sa presvedčiť že tento príkaz nám v adresári **blog/migrations** vytvoril ďalší migračný súbor **blog\migrations\0002_comment.py**. Teraz musíme tieto zmeny ale aplikovať na databázu použiťím príkazu **python manage.py migrate blog** . Výstup by mal vyzerať takto:

~~~
(myvenv) ~/djangogirls$ python manage.py migrate blog
    Operations to perform:
      Apply all migrations: blog
    Running migrations:
      Rendering model states... DONE
      Applying blog.0002_comment... OK
~~~

Náš model komentárov tým vznikol v databáze. Asi by bolo vhodné aby sme k nemu mali prístup na našom admin paneli.

### Zaregistrovanie modelu komentárov v paneli administrátora 

Ak chcete zaregistrovať model komentárov v paneli správcu, musíme prejísť na **blog/admin.py** a pridať tento riadok :

~~~
admin.site.register(Comment)
~~~
priamo pod týmto riadkom:
~~~
admin.site.register(Post)
~~~

Je potrebné importovať aj model komentárov v hornej časti súboru, a to takto:

~~~
from django.contrib import admin
from .models import Post, Comment

admin.site.register(Post)
admin.site.register(Comment)
~~~

Ak zadáte **python manage.py runserver** do príkazového riadka a prejdete na adresu http://127.0.0.1:8000/admin/ vo svojom prehliadači, mali by ste mať prístup k zoznamu komentárov a tiež možnosť pridávať a odstraňovať komentáre. 

### Zobrazenie našich komentárov

Prejdite do súboru **blog/templates/blog/post_detail.html** a pred značku  **{% endblock %}** na konci pridajte nasledujúce riadky :

~~~
<hr>
{% for comment in post.comments.all %}
    <div class="comment">
        <div class="date">{{ comment.created_date }}</div>
        <strong>{{ comment.author }}</strong>
        <p>{{ comment.text|linebreaks }}</p>
    </div>
{% empty %}
    <p>Zatiaľ tu nie sú žiadne komentáre :(</p>
{% endfor %}
~~~

Teraz môžeme vidieť sekciu komentárov na stránkach s podrobnosťami o príspevku. Mohlo by to však vyzerať o niečo lepšie, takže do spodnej časti súboru pridajme nejaké CSS do súboru **static/css/blog.css** :

~~~
.comment {
    margin: 20px 0px 20px 20px;
}
~~~

Návštevníkov nášho diskusného fóra môžeme tiež informovať o komentároch ktoré boli pridané na stránku zo zoznamom príspevkov. Prejdime do súboru **blog/templates/blog/post_list.html** a pridajte riadok:

~~~
<a href="{% url 'post_detail' pk=post.pk %}">Comments: {{ post.comments.count }}</a>
~~~

Potom by naša šablóna mala vyzerať takto:

~~~
{% extends 'blog/base.html' %}

{% block content %}
    {% for post in posts %}
        <div class="post">
            <div class="date">
                {{ post.published_date }}
            </div>
            <h1><a href="{% url 'post_detail' pk=post.pk %}">{{ post.title }}</a></h1>
            <p>{{ post.text|linebreaksbr }}</p>
            <a href="{% url 'post_detail' pk=post.pk %}">Komentár : {{ post.comments.count }}</a>
        </div>
    {% endfor %}
{% endblock content %}
~~~

### Nechajme čitateľov písať komentáre

Práve teraz síce vidíme komentáre na našom blogu, ale nemôžeme ich pridávať. Poďme to teda zmeniť. Prejdite na **blog/forms.py** a pridajme nasledujúce riadky na koniec súboru:

~~~
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)
~~~

Nezabudnime importovať model komentárov a zmeňme riadok:

~~~
from .models import Post
~~~
na 
~~~
from .models import Post, Comment
~~~

Teraz prejdime na **blog/templates/blog/post_detail.html** a pred riadok **{% for comment in post.comments.all %}** pridajme:
~~~
<a class="btn btn-secondary" href="{% url 'add_comment_to_post' pk=post.pk %}">Pridaj komentár</a>
~~~
Ak prejdeme na stránku s podrobnosťami o príspevku, mala by sa vám zobraziť táto chyba:

![](/obrazky/djangogirls34.png)

Vieme, ako to napraviť a prejdite na **blog/urls.py** aby sme pridali tento vzor do url **patterns** :
~~~
path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
~~~

Keď obnovíme stránku tak sa zobrazí iná chyba.

![](/obrazky/djangogirls35.png)

Ak chceme túto chybu opraviť, pridáme na koniec do **blog/views.py** toto zobrazenie :
~~~
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})
~~~

Nezabudnime však importovať na začiatok súboru **CommentForm** :

~~~
from .forms import PostForm, CommentForm
~~~

Teraz by ste mali na stránke s podrobnosťami o príspevku vidieť tlačidlo „Pridaj komentár“ (Add comment).

![](/obrazky/djangogirls37.png)

Keď však kliknete na toto tlačidlo, uvidíte:

![](/obrazky/djangogirls36.png)

Ako nám chyba hovorí, šablóna zatiaľ neexistuje. Takže vytvorte nový súbor na adrese **blog/templates/blog/add_comment_to_post.html** a pridajte do neho nasledujúci kód:

~~~
{% extends 'blog/base.html' %}

{% block content %}
    <h1>New comment</h1>
    <form method="POST" class="post-form">{% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="save btn btn-secondary">Odošli</button>
    </form>
{% endblock %}
~~~
Tak a teraz nám čitatelia našich príspevkov môžu dávať vedieť, čo si myslia o našich blogových názoroch.

### Moderovanie komentárov

Nie všetky komentáre by sa mali zobrazovať. Ako vlastník blogu pravdepodobne chceme mať možnosť schvaľovať alebo mazať komentáre. 

Ak ste tak ešte neurobili, všetky ikony Bootstrap si môžete stiahnuť [**tu**](https://github.com/twbs/icons/releases/download/v1.1.0/bootstrap-icons-1.1.0.zip). Rozbaľte súbor a odtiaľ si skopírujte požadované obrazové súbory SVG do priečinka s názvom **blog/templates/blog/icons**. Týmto spôsobom môžete získať prístup k ľubovolnej ikone ktorá sa tu nachádza. Patrí k nim aj **hand-thumbs-down.svg** ktorú si nakopírujeme do spomenutého priečinka **blog/templates/blog/icons**

Prejdime na **blog/templates/blog/post_detail.html** a zmeňte riadky:

~~~
{% for comment in post.comments.all %}
    <div class="comment">
        <div class="date">{{ comment.created_date }}</div>
        <strong>{{ comment.author }}</strong>
        <p>{{ comment.text|linebreaks }}</p>
    </div>
{% empty %}
    <p>Zatiaľ tu nie sú žiadne komentáre :</p>
{% endfor %}
~~~
na takéto :

~~~
{% for comment in post.comments.all %}
    {% if user.is_authenticated or comment.approved_comment %}
    <div class="comment">
        <div class="date">
            {{ comment.created_date }}
            {% if not comment.approved_comment %}
                <a class="btn btn-secondary" href="{% url 'comment_remove' pk=comment.pk %}">
                   {% include './icons/hand-thumbs-down.svg' %}
                </a>
                <a class="btn btn-secondary" href="{% url 'comment_approve' pk=comment.pk %}">
                   {% include './icons/hand-thumbs-up.svg' %}
                </a>
            {% endif %}
        </div>
        <strong>{{ comment.author }}</strong>
        <p>{{ comment.text|linebreaks }}</p>
    </div>
    {% endif %}
{% empty %}
    <p>Zatiaľ tu nie sú žiadne komentáre :</p>
{% endfor %}
~~~

Pri spustení aplikácie by sme mali vidieť chybu **NoReverseMatch**, pretože zatiaľ žiadna adresa URL nezodpovedá vzorom **comment_remove** a **comment_approve**.

Ak chcete chybu opraviť, pridajme do **blog/urls.py** tieto vzory adries URL :

~~~
path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
~~~

Teraz by sme mali ešte vidieť chybu **AttributeError**. Ak chceme túto chybu opraviť, musíme pridať tieto zobrazenia do **blog/views.py** :

~~~
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)
~~~

a naviac v hornrj časti súboru budeme musieť importovať do modelov modul **Comment**

~~~
from .models import Post, Comment
~~~

Ak všetko funguje, je tu ešte jedna malá úprava, ktorú môžeme urobiť. Na našej stránke so zoznamom príspevkov momentálne vidíme pod príspevkami počet **všetkých** komentárov, ktoré blogový príspevok získal. Zmeňme to tak, aby sa tam zobrazoval **iba** počet schválených komentárov, nakoľko niektoré z komentárov môžu byť tak isto nevhodné ako to bolo v prípade kontroly vlastných príspevkov.

Ak to chcete vyriešiť, prejdite na **blog/templates/blog/post_list.html** a zmeňte riadok:
~~~
<a href="{% url 'post_detail' pk=post.pk %}">Komentáre : {{ post.comments.count }}</a>
~~~
na riadok s týmto obsahom :

~~~
<a href="{% url 'post_detail' pk=post.pk %}">Komentáre : {{ post.approved_comments.count }}</a>
~~~

Nakoniec je od nás ešte očakávané aby sme do modelu Post v **blog/models.py** pridali ešte túto metódu  :

~~~
ef approved_comments(self):
    return self.comments.filter(approved_comment=True)
~~~

Tým je rozšírenie funkcionality webovej aplikácie o funkciu komentárov dokončená!