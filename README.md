# im_qsb
This package provides methods for safely describing App Engine Search API Query as a json structure (a QSpec).

You can construct a QSpec manually or by using the qsb_X methods

You can render any QSpec to a Search API Query String using render_query_string()

The github repo is [here](https://github.com/emlynoregan/im_qsb).

[![Build Status](https://travis-ci.org/emlynoregan/im_qsb.svg?branch=master)](https://travis-ci.org/emlynoregan/im_qsb)

## Install 

Use the python package for this library. You can find the package online [here](https://pypi.org/project/im-qsb/).

Change to your Python App Engine project's root folder and do the following:

> pip install im_qsb --target lib

Or add it to your requirements.txt. You'll also need to set up vendoring, see [app engine vendoring instructions here](https://cloud.google.com/appengine/docs/python/tools/using-libraries-python-27).

# QSpec

A QSpec is a json structure for describing a Search Engine API query, which is converted to a querystring using the following rules:

## string QSpec:
	qspec format: <string or unicode>
	renders to: quote delimited and escaped unicode string value 
	example: 'Fred "Freddy" Frog' => u'"Fred \"Freddy\" Frog"'
	construct method: qsb_string(<string or unicode>)

## number QSpec:
	qspec format: <number>
	renders to: a numeric value
	example: 47 => u'47'
	construct method: qsb_number(<number>)

## boolean QSpec:
	qspec format: <boolean>
	renders to: '1' or '0'
	example: True => '1'
	construct method: qsb_boolean(<boolean>)

## unquoted QSpec:
	qspec format: { "unquoted": <string or unicode> }
	renders to: an escaped but not quote delimited unicode string value
	example: { "unquoted": 'Fred "Freddy" Frog' } => u'Fred \"Freddy\" Frog'
	construct method: qsb_unquoted(<string or unicode>)

## field QSpec:
	qspec format: { "fieldname": <string or unicode> }
	renders to: a valid fieldname, with invalid characters replaced with "_"
	example: 'first*name' => u'firse_name'
	construct method: qsb_field(<string or unicode>)

## equality QSpec
	qspec format: { "op": "=", "field": <field QSpec>, "value": <QSpec> }
	renders to: an equality comparison
	example: {"op":"=", "field": {"fieldname":"name"}, "value": "Frodo"} => u'name:"Frodo"'
	construct method: qsb_eq(<field QSpec>, <QSpec>)

## inequality QSpec
	qspec format: qspec format: { "op": "!=", "field": <field QSpec>, "value": <QSpec> }
	renders to: an inequality comparison
	example: {"op":"!=", "field": {"fieldname":"name"}, "value": "Frodo"} => u'NOT (name:"Frodo")'
	construct method: qsb_neq(<field QSpec>, <QSpec>)

## paren QSpec
	qspec format: { "op": "paren", "arg": <QSpec> }
	renders to: wraps parens around a QSpec
	example: {"op": "paren", "arg": 47} => u'(47)'
	construct method: qsb_paren(<QSpec>)

## stem QSpec
	qspec format: { "op": "stem", "arg": <QSpec> }
	renders to: adds a stem to a QSpec
	example: {"op": "stem", "arg": "Harry"} => u'~"Harry"'
	construct method: qsb_stem(<QSpec>)

## less-than QSpec
	qspec format: { "op": "<", "field": <field QSpec>, "value": <QSpec> }
	renders to: a less-than comparison
	example: {"op":"<", "field": {"fieldname":"amount"}, "value": 43} => u'amount<43'
	construct method: qsb_lt(<field QSpec>, <QSpec>)

## less-than-or-equal-to QSpec
	qspec format: { "op": "<=", "field": <field QSpec>, "value": <QSpec> }
	renders to: a less-than-or-equal-to comparison
	example: {"op":"<=", "field": {"fieldname":"amount"}, "value": 47.2} => u'amount<=47.2'
	construct method: qsb_le(<field QSpec>, <QSpec>)

## greater-than QSpec
	qspec format: { "op": ">", "field": <field QSpec>, "value": <QSpec> }
	renders to: a greater-than comparison
	example: {"op":">", "field": {"fieldname":"amount"}, "value": -1} => u'amount>-1'
	construct method: qsb_gt(<field QSpec>, <QSpec>)

## greater-than-or-equal-to QSpec
	qspec format: { "op": ">=", "field": <field QSpec>, "value": <QSpec> }
	renders to: a greater-than-or-equal-to comparison
	example: {"op":">=", "field": {"fieldname":"amount"}, "value": 0} => u'amount>=0'
	construct method: qsb_ge(<field QSpec>, <QSpec>)

## and QSpec
	qspec format: { "op": "AND", args: [<list of QSpec>] }
	renders to: a space separated list of QSpecs, which is a valid way to express AND relationships.
	example: {"op":"AND", "args": ["X", "Y", "Z"] => u'"X" "Y" "Z"'
	construct method: qsb_and(<QSpec>, ...)

## or QSpec
	qspec format: { "op": "OR", args: [<list of QSpec>] }
	renders to: an OR separated list of QSpecs.
	example: {"op":"OR", "args": ["noodle", {"quoted": "poodle"}]} => u'"noodle" OR poodle'
	construct method: qsb_or(<QSpec>, ...)

## not QSpec
	qspec format: { "op": "NOT", arg: <QSpec> }
	renders to: a negation of a QSpecs.
	example: {"op":"NOT", "args":"noodle"} => u'NOT "noodle"'
	construct method: qsb_not(<QSpec>)

## geopoint QSpec
	qspec format: { "op": "geopoint", left: <number QSpec>, right: <number QSpec> }
	renders to: a geopoint specification
	example: {"op":"geopoint", "left": 12, "right": 42.7} => u'geopoint(12,42.7)'
	construct method: qsb_geopoint(<number QSpec>, <number QSpec>)

## distance QSpec
	qspec format: { "op": "distance", left: <QSpec>, right: <QSpec> }
	renders to: a distance specification
	example: {"op": "distance", "left": {"op":"geopoint", "left": 12, "right": 42.7}, "right": {"fieldname": "home"}} 
		=> u'distance(geopoint(12,42.7),home)'
	construct method: qsb_distance(<QSpec>, <QSpec>)
