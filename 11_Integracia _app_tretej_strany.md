>## Integrácia aplikácie tretej strany

Keď už sme napísali naše vlastné doplnky do aplikácie django CMS, môžeme náš CMS rozšíriť o aplikáciu tretej strany, napr. [Djangocms-Blog](https://github.com/nephila/djangocms-blog).

### Základná inštalácia 

Najprv musíme nainštalovať aplikáciu do nášho virtuálneho prostredia napr. z [PyPI](https://pypi.python.org/):
~~~
$ pip install djangocms-blog
~~~
a nasledovať budú nastavenia Django.

### Nastavenia Django

>#### v INSTALLED_APPS

Pridajte aplikáciu a všetky jej požiadavky, ktoré tam ešte nie sú,  INSTALLED_APPS súboru settings.py. Pritom sa alemusíme vyhnúť duplicite:
~~~
'filer',                    # uz mame
'easy_thumbnails',          # uz mame
'aldryn_apphooks_config',
'parler',
'taggit',
'taggit_autosuggest',
'meta',
'sortedm2m',
'djangocms_blog',
~~~

>#### v THUMBNAIL_PROCESSORS
Jednou zo závislých funckcií je Django Filer. Poskytuje špeciálnu funkciu, ktorá umožňuje sofistikovanejšie orezávanie obrázkov.
~~~
THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',        # uz mame
    'easy_thumbnails.processors.autocrop',          # uz mame
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',             # uz mame
    'easy_thumbnails.processors.filters',           # uz mame
)

META_SITE_PROTOCOL = 'https'  # set 'http' for non ssl enabled websites
META_USE_SITES = True
~~~

>#### v URL Patterns

Pridajte nasledujúci vzor adresy URL do súboru hlavnej adresy urls.py:
~~~
urlpatterns += [
    url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
]
~~~

### Migrácia databázy

Pridali sme novú aplikáciu, takže musíme aktualizovať aj našu databázu:
~~~
python manage.py migrate
~~~
Znova spustíme server:
~~~
$ python manage.py runserver
~~~

### Vytvorte novú pripojenú stránku

Aplikácia News & Blog sa dodáva s apphookom django CMS, takže pridajte novú stránku django CMS (ktorú nazveme **Blog** ) a pridajte k nej aplikáciu Blog [rovnako ako v prípade prieskumov](https://docs.django-cms.org/en/latest/introduction/05-apphooks.html#apply-apphook).

Pre túto aplikáciu musíme tiež vytvoriť a vybrať konfiguráciu aplikácie (Application configuration).

 Tejto konfigurácii aplikácie dáme nejaké nastavenia:
* **Instance namespace**: článok (používa sa na revezné (návratové) URL adresy )
* **Application title**: Blog (názov, ktorý bude reprezentovať konfiguráciu aplikácie v správcovi)
* **Permalink type**: vyberte formát, ktorý uprednostňujete pre URL adresy vytváraných článkov

Uložte túto konfiguráciu aplikácie a uistite sa, že je vybratá v **Application configurations**. Publikujte (zverejnite) novú stránku a mali by ste tam nájsť aplikáciu Blog. (Kým skutočne nevytvoríte žiadne články, bude vás informovať, že nie sú dostupné žiadne položky .)

### Pridať nové články zo správ a blogu

Nové články môžete pridávať pomocou správcu alebo pomocou novej ponuky **Blog**, ktorá sa teraz zobrazuje na paneli s nástrojmi, keď sa nachádzate na stránke patriacej blogu.
