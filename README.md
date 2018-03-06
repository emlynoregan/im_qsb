# im_qsb
This package provides methods for safely describing App Engine Search API Query as a json structure (a QSpec).

You can construct a QSpec manually or by using the qsb_X methods

You can render any QSpec to a Search API Query String using render_query_string()

[![Build Status](https://travis-ci.org/emlynoregan/im_qsb.svg?branch=master)](https://travis-ci.org/emlynoregan/im_qsb)

## Install 

Use the python package for this library. You can find the package online [here](https://pypi.org/project/im-qsb/).

Change to your Python App Engine project's root folder and do the following:

> pip install im_qsb --target lib

Or add it to your requirements.txt. You'll also need to set up vendoring, see [app engine vendoring instructions here](https://cloud.google.com/appengine/docs/python/tools/using-libraries-python-27).

# QSpec

A QSpec is a json structure for describing a Search Engine API query, which is converted to a querystring using the following rules:

## string QSpec:
<string or unicode> => a quote delimited and escaped unicode string value, eg: 'Fred "Freddy" Frog' => u'"Fred \"Freddy\" Frog"'

Construct:
	qsb_string(<string or unicode>)

## number QSpec:
<number>: a numeric value, eg: 47 => u'47'

Construct:
	qsb_number(<number>)

## boolean QSpec:
<boolean>: '1' or '0', eg: True => '1', 

Construct:
	qsb_boolean(<boolean>)

## unquoted QSpec:
{ "unquoted": <string or unicode> }: an escaped but not quote delimited unicode string value, eg: { "unquoted": 'Fred "Freddy" Frog' } => u'Fred \"Freddy\" Frog'

Construct:
	qsb_unquoted(<string or unicode>)

## field QSpec:
{ "fieldname": <string or unicode> }: a valid fieldname, with invalid characters replaced with "_", eg: 'first*name' => u'firse_name'

Construct:
	qsb_field(<string or unicode>)

## equality QSpec
{ "op": "=", "field": <field QSpec>, "value": <QSpec> }: an equality comparison, eg: {"op":"=", "field": {"fieldname":"name"}, "value": "Frodo"} => u'name:"Frodo"'

Construct:
	qsb_eq(<field QSpec>, <QSpec>)

## inequality QSpec
{ "op": "!=", "field": <field QSpec>, "value": <QSpec> }: an inequality comparison, eg: {"op":"!=", "field": {"fieldname":"name"}, "value": "Frodo"} => u'NOT (name:"Frodo")'

Construct:
	qsb_neq(<field QSpec>, <QSpec>)

## paren QSpec
{ "op": "paren", "arg": <QSpec> }: wraps parens around a QSpec, eg: {"op": "paren", "arg": 47} => u'(47)'

Construct:
	qsb_paren(<QSpec>)

## stem QSpec
{ "op": "stem", "arg": <QSpec> }: adds a stem to a QSpec, eg: {"op": "stem", "arg": "Harry"} => u'~"Harry"'

Construct:
	qsb_stem(<QSpec>)

## less-than QSpec
{ "op": "<", "field": <field QSpec>, "value": <QSpec> }: a less-than comparison, eg: {"op":"<", "field": {"fieldname":"amount"}, "value": 43} => u'amount<43'

Construct:
	qsb_lt(<field QSpec>, <QSpec>)

## less-than-or-equal-to QSpec
{ "op": "<=", "field": <field QSpec>, "value": <QSpec> }: a less-than-or-equal-to comparison, eg: {"op":"<=", "field": {"fieldname":"amount"}, "value": 47.2} => u'amount<=47.2'

Construct:
	qsb_le(<field QSpec>, <QSpec>)

## greater-than QSpec
{ "op": ">", "field": <field QSpec>, "value": <QSpec> }: a greater-than comparison, eg: {"op":">", "field": {"fieldname":"amount"}, "value": -1} => u'amount>-1'

Construct:
	qsb_gt(<field QSpec>, <QSpec>)

## greater-than-or-equal-to QSpec
{ "op": ">=", "field": <field QSpec>, "value": <QSpec> }: a greater-than-or-equal-to comparison, eg: {"op":">=", "field": {"fieldname":"amount"}, "value": 0} => u'amount>=0'

Construct:
	qsb_ge(<field QSpec>, <QSpec>)

## and QSpec
{ "op": "AND", args: [<list of QSpec>] }: a space separated list of QSpecs, which is a valid way to express AND relationships. eg: {"op":"AND", "args": ["X", "Y", "Z"] => u'"X" "Y" "Z"'

Construct:
	qsb_and(<QSpec>, ...)

## or QSpec
{ "op": "OR", args: [<list of QSpec>] }: an OR separated list of QSpecs. eg: {"op":"OR", "args": ["noodle", {"quoted": "poodle"}]} => u'"noodle" OR poodle'

Construct:
	qsb_or(<QSpec>, ...)

## not QSpec
{ "op": "NOT", arg: <QSpec> }: a negation of a QSpecs. eg: {"op":"NOT", "args":"noodle"} => u'NOT "noodle"'

Construct:
	qsb_not(<QSpec>)

## geopoint QSpec
{ "op": "geopoint", left: <number QSpec>, right: <number QSpec> }: a geopoint specification, eg: {"op":"geopoint", "left": 12, "right": 42.7} => u'geopoint(12,42.7)'

Construct:
	qsb_geopoint(<number QSpec>, <number QSpec>)

## distance QSpec
{ "op": "distance", left: <QSpec>, right: <QSpec> }: a distance specification, eg: {"op": "distance", "left": {"op":"geopoint", "left": 12, "right": 42.7}, "right": {"fieldname": "home"}} => u'distance(geopoint(12,42.7),home)'

Construct:
	qsb_distance(<QSpec>, <QSpec>)
