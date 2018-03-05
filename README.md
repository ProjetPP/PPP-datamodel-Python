# PPP DataModel

[![Build Status](https://scrutinizer-ci.com/g/ProjetPP/PPP-datamodel-Python/badges/build.png?b=master)](https://scrutinizer-ci.com/g/ProjetPP/PPP-datamodel-Python/build-status/master)
[![Code Coverage](https://scrutinizer-ci.com/g/ProjetPP/PPP-datamodel-Python/badges/coverage.png?b=master)](https://scrutinizer-ci.com/g/ProjetPP/PPP-datamodel-Python/?branch=master)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/ProjetPP/PPP-datamodel-Python/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/ProjetPP/PPP-datamodel-Python/?branch=master)
[![PyPi version](https://img.shields.io/pypi/v/ppp_datamodel.svg)](https://pypi.python.org/pypi/ppp_datamodel)


# How to install

With a recent version of pip:

```
pip3 install git+https://github.com/ProjetPP/PPP-datamodel-Python.git
```

With an older one:

```
git clone https://github.com/ProjetPP/PPP-datamodel-Python.git
cd PPP-datamodel-Python
python3 setup.py install
```

Use the `--user` option if you want to install it only for the current user.


# How to use

You can use any of the classes in the `ppp_datamodel` package: `Triple`,
`Resource`, and `Missing`. They all have a nice constructor, getters for
their attributes, and serialization methods, etc.

An example:

```
>>> import ppp_datamodel
>>> my_triple = ppp_datamodel.Triple(subject=ppp_datamodel.Resource(value='George Washington'), predicate=ppp_datamodel.Resource(value='birth date'), object=ppp_datamodel.Missing())
>>> print(my_triple.as_json())
{"type": "triple", "predicate": {"type": "resource", "value": "birth date"}, "subject": {"type": "resource", "value": "George Washington"}, "object": {"type": "missing"}}
>>> my_triple.predicate
<PPP node "resource" {'value': 'birth date'}>
```

You can also deserialize them:

```
>>> ppp_datamodel.AbstractNode.from_json('{"type": "resource", "value": "George Washington"}')
<PPP node "resource" {'value': 'George Washington'}>
>>> ppp_datamodel.AbstractNode.from_json('{"type": "resource", "value": "George Washington"}') == ppp_datamodel.Resource(value='George Washington')
True
```


For a list of their accepted attributes, see the
[PPP data model specification](https://github.com/ProjetPP/Documentation/blob/master/data-model.md)
