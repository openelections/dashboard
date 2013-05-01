from django.core.exceptions import ValidationError
from django.test import TestCase


from ..models import Election

class ElectionTest(TestCase):

    fixtures = [
        'parties_initial',
        'test_elecdata_model'
    ]


    def test_offices(self):
        "Election.offices should return tuple of offices up for election"
        # Florida 2012 races
        general = Election.objects.get(pk=4)
        gop_primary = Election.objects.get(pk=30)
        gop_prez_primary = Election.objects.get(pk=31)

        self.assertEqual(general.offices, ('prez', 'senate', 'house', 'state_officers', 'state_leg'))
        self.assertEqual(gop_primary.offices, ('senate', 'house', 'state_leg'))
        self.assertEqual(gop_prez_primary.offices, ('prez',))

    def test_elec_key(self):
        "Election.elec_key can return tuple or string election key"
        # Florida 2012 races
        general = Election.objects.get(pk=4)
        gop_primary = Election.objects.get(pk=30)
        gop_prez_primary = Election.objects.get(pk=31)

        self.assertEqual(general.elec_key(), ('2012-11-06', u'FL', u'general', 'prez', 'senate', 'house', 'state_officers', 'state_leg'))
        self.assertEqual(general.elec_key(as_string=True), u'2012-11-06 - FL - general (prez, senate, house, state_officers, state_leg)')

        self.assertEqual(gop_primary.elec_key(), ('2012-08-14', u'FL', u'primary', u'REP', 'senate', 'house', 'state_leg'))
        self.assertEqual(gop_primary.elec_key(as_string=True), u'2012-08-14 - FL - primary/REP (senate, house, state_leg)')

        self.assertEqual(gop_prez_primary.elec_key(), ('2012-01-31', u'FL', u'primary', u'REP', 'prez'))
        self.assertEqual(gop_prez_primary.elec_key(as_string=True), u'2012-01-31 - FL - primary/REP (prez)')

    def test_special_status(self):
        "Election.special key should return tuple of meta"
        # Florida 2011 special
        special = Election.objects.get(pk=35)
        self.assertEqual(special.special_key(), ('special', u'state-senate', '1'))

        # Florida 2012 general
        general = Election.objects.get(pk=4)
        self.assertEqual(general.special_key(),())

    def test_special_no_district(self):
        """Special without a district should return a two-tuple without a district num, and elec_key should not have num"""
        # Florida 2011 special
        special = Election.objects.get(pk=35)
        special.district = ""
        special.save()
        self.assertEqual(special.special_key(), ('special', u'state-senate'))
        self.assertEqual(special.elec_key(), ('2011-09-20', u'FL', u'primary', 'DEM', 'special', 'state-senate'))
