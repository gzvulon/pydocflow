# Motivation
Dictmodel tries to simplfy data modeling 
using native `python typing` system,
while keeping inner representation in `python struct`. 

`python struct` is similar to json hierarchial structure with combinations of `dict`, `list` as nodes  and primitive types as leafs, root is `dict`.

DictModel instances can be passed to different systems that accept json/dict input
without unnecessary representation transform.


Existing libraries like 
[jsonmodels](http://) are missing ability to express typed mapping like `Dict[str, int]` or even `dict`. 

Others are bounded to data source provider:
- MongoEngine (mongodb)
- Google Datastore
- DjangoModels

In python 3.7 we have native pure data types,
but we have a convertation from dict to inner python objects which in most cases in not requred, and cannot be passed.

# Installation 
```
git clone me
```

# Object Instantiation Approaaches

## Change Representation Approach
Treat dicts like well known statically type models
while python 3.7 introduced Data Types,
this approach to data modeling in python still similar to
those proposed by:
- Google: datastore ORM
- Google: protobuf Messages
- Django: sqldb ORM
- jsonmodels: python objects serializable to jsons and structs( ditcs)

> Cons:
- All of them are transform original dict-struct
- and create something that not always easy serializable
- lack dict functionality like `update`
- recently transformed to struct (dict)
- tied to specific solution (json, db, message)

## Change Class Approach
*Dictmodel* are keep type of original dict-struc
which is `dict`.
In fact `DictModel` class is subtype of dict.
Just with methods class and instance.

Pros:
- support dict as field type
- not mandatory by design
- one contracts /cfg definition for all ( db, yml, msg )




