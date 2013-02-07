from django.test import TestCase

from ..models import ElecData

class ElecDataTest(TestCase):

    fixtures = ['test_elecdata_model']


    def test_offices(self):
        "ElecData.offices should return tuple of offices up for election"
        # Florida 2012 races
        general = ElecData.objects.get(pk=4)
        primary = ElecData.objects.get(pk=30)
        prez_primary = ElecData.objects.get(pk=31)

        self.assertEqual(general.offices, ('prez', 'senate', 'house', 'state_officers', 'state_leg'))
        self.assertEqual(primary.offices, ('senate', 'house', 'state_leg'))
        self.assertEqual(prez_primary.offices, ('prez',))

    def test_elec_key(self):
        "ElecData.elec_key can return tuple or string election key"
        # Florida 2012 races
        general = ElecData.objects.get(pk=4)
        primary = ElecData.objects.get(pk=30)
        prez_primary = ElecData.objects.get(pk=31)

        self.assertEqual(general.elec_key(), ('2012-11-06', u'FL', u'general', 'prez', 'senate', 'house', 'state_officers', 'state_leg'))
        self.assertEqual(general.elec_key(as_string=True), '2012-11-06 - FL - general (prez, senate, house, state_officers, state_leg)')

        self.assertEqual(primary.elec_key(), ('2012-08-14', u'FL', u'primary', 'senate', 'house', 'state_leg'))
        self.assertEqual(primary.elec_key(as_string=True), u'2012-08-14 - FL - primary (senate, house, state_leg)')

        self.assertEqual(prez_primary.elec_key(), ('2012-01-31', u'FL', u'primary', 'prez'))
        self.assertEqual(prez_primary.elec_key(as_string=True), u'2012-01-31 - FL - primary (prez)')

    def test_special_status(self):
        "ElecData.special key should return tuple of meta"
        # Florida 2011 special
        special = ElecData.objects.get(pk=35)
        self.assertEqual(special.special_key(), ('special', u'state-senate', '1'))

        # Florida 2012 general
        general = ElecData.objects.get(pk=4)
        self.assertEqual(general.special_key(),())
