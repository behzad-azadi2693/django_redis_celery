# redis in django

***
### this contains repository
```
system secore
system view
basket order 
caching system
```
***

***
### cache in django
```
memcache and pylibmemcache:
key value store
default size 1MB store
shared by several client
in memory store
fast and easy
more popularity


locmemcache:
local memory cache global
you want to cache separate use LOCATIN(spinning multiple processes)
use python dictionary
useful for development and testing for  your code is caching correctly


dummy:
usefull for development and testing
checking check is a key valid
don't for caching production


file-base cache:
use compressed file in location directory
is this fast and slow?? depend on what you're caching


database cache:
save in table named in LOCATION
this is awesome and best but if your DB is fast
can be easily shared across processes and servers 

manage.py createcachetable



program code:
from django.core.cache import cache
cache.set()
cache.get()
(cache <time> <name>)(vies.index)

{%load cache%}
{% cahe <time> <name> %}{%endcache%}


from django.views.decorators.cache import cache_page
@cache_page(<time>)



notes:
cache in FBVs better of CBVs
cahe design for FBV but for CBV we designing
```
***
