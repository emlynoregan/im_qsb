import unittest
from im_qsb import render_query_string, qsb_string, is_string_QSpec,\
    qsb_unquoted, is_unquoted_QSpec, qsb_number, is_number_QSpec, qsb_bool,\
    is_bool_QSpec, qsb_eq, qsb_field, is_eq_QSpec, is_field_QSpec, qsb_neq,\
    is_neq_QSpec, qsb_paren, is_paren_QSpec, qsb_stem, is_stem_QSpec,\
    is_lt_QSpec, qsb_lt, qsb_le, is_le_QSpec, qsb_ge, is_ge_QSpec, is_gt_QSpec,\
    qsb_gt, qsb_geopoint, is_geopoint_QSpec, qsb_distance, is_distance_QSpec,\
    qsb_and, is_and_QSpec, qsb_or, is_or_QSpec, qsb_not, is_not_QSpec
class Tests(unittest.TestCase):
    def testRenderString(self):
        qspec = qsb_string("Thingo")

        is_string_QSpec(qspec, True)        
        
        result = render_query_string(qspec)
        
        self.assertEqual(result, u'"Thingo"')

    def testRenderString2(self):
        qspec = qsb_string(u'O"Regan')

        is_string_QSpec(qspec, True)        
        
        result = render_query_string(qspec)
        
        self.assertEqual(result, u'"O\\"Regan"')

    def testRenderUnquotedString(self):
        qspec = qsb_unquoted(u'O"Regan')

        is_unquoted_QSpec(qspec, True)        
        
        result = render_query_string(qspec)
        
        self.assertEqual(result, u'O\\"Regan')

    def testRenderNumber(self):
        qspec = qsb_number(47.3)

        is_number_QSpec(qspec, True)        
        
        result = render_query_string(qspec)
        
        self.assertEqual(result, u'47.3')

    def testRenderBoolean(self):
        qspec = qsb_bool(True)

        is_bool_QSpec(qspec, True)        
        
        result = render_query_string(qspec)
        
        self.assertEqual(result, u'1')

    def testField(self):
        qspec = qsb_field("DOC_NAME")

        is_field_QSpec(qspec, True)        
        
        result = render_query_string(qspec)
        
        self.assertEqual(result, u'DOC_NAME')

    def testAnd(self):
        qspec = qsb_and(
            "Poodle",
            qsb_unquoted("Noodle")
        )

        is_and_QSpec(qspec, True)
        
        result = render_query_string(qspec)
        
        self.assertEqual(result, u'"Poodle" Noodle')

    def testOr(self):
        qspec = qsb_or(
            qsb_eq(
                qsb_field("dog"),
                "Poodle"
            ),
            qsb_unquoted("Noodle"),
            "Squirtle"
        )

        is_or_QSpec(qspec, True)
        
        result = render_query_string(qspec)
        
        self.assertEqual(result, u'dog:"Poodle" OR Noodle OR "Squirtle"')

    def testNot(self):
        qspec = qsb_not(
            qsb_eq(
                qsb_field("dog"),
                "Poodle"
            )
        )

        is_not_QSpec(qspec, True)
        
        result = render_query_string(qspec)
        
        self.assertEqual(result, u'NOT dog:"Poodle"')

    def testEq(self):
        qspec = qsb_eq(
            qsb_field("DOC_NAME"),
            "Noodle"
        )

        is_eq_QSpec(qspec, True)
        
        result = render_query_string(qspec)
        
        self.assertEqual(result, u'DOC_NAME:"Noodle"')

    def testNeq(self):
        qspec = qsb_neq(
            qsb_field("DOC_NAME"),
            "Noodle"
        )

        is_neq_QSpec(qspec, True)    
        
        result = render_query_string(qspec)
        
        self.assertEqual(result, u'NOT (DOC_NAME:"Noodle")')


    def testParen(self):
        qspec = qsb_paren(
            u"Noodle doodle",
        )

        is_paren_QSpec(qspec, True)     
        
        result = render_query_string(qspec)
        
        self.assertEqual(result, u'("Noodle doodle")')

    def testStem(self):
        qspec = qsb_stem(
            u"Noodle doodle",
        )

        is_stem_QSpec(qspec, True)
        
        result = render_query_string(qspec)
        
        self.assertEqual(result, u'~"Noodle doodle"')

    def testLt(self):
        qspec = qsb_lt(
            qsb_field("ZZZ"),
            qsb_number(4300)
        )

        is_lt_QSpec(qspec, True) 
        
        result = render_query_string(qspec)
        
        self.assertEqual(result, u'ZZZ<4300')

    def testLe(self):
        qspec = qsb_le(
            qsb_field("A*B"),
            qsb_number(45.9)
        )

        is_le_QSpec(qspec, True)   
        
        result = render_query_string(qspec)
        
        self.assertEqual(result, u'A_B<=45.9')

    def testGe(self):
        qspec = qsb_ge(
            qsb_field("ABC"),
            qsb_number(0)
        )

        is_ge_QSpec(qspec, True)   
        
        result = render_query_string(qspec)
        
        self.assertEqual(result, u'ABC>=0')

    def testGt(self):
        qspec = qsb_gt(
            qsb_field("abcd"),
            qsb_number(-1)
        )

        is_gt_QSpec(qspec, True)   
        
        result = render_query_string(qspec)
        
        self.assertEqual(result, u'abcd>-1')

    def testGeopoint(self):
        qspec = qsb_geopoint(
            45.6,
            29.2
        )

        is_geopoint_QSpec(qspec, True)        
        
        result = render_query_string(qspec)
        
        self.assertEqual(result, u'geopoint(45.6,29.2)')

    def testDistance(self):
        distqspec = qsb_distance(
            qsb_field("home_base"),
            qsb_geopoint(34.5, 22)
        )

        is_distance_QSpec(distqspec, True)
        
        qspec = qsb_gt(
            distqspec,
            47
        )

        is_gt_QSpec(qspec, True)
        
        result = render_query_string(qspec)
        
        self.assertEqual(result, u'distance(home_base,geopoint(34.5,22))>47')
