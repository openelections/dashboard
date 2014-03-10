from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import Contact, Election, Log, State, Volunteer

class ElectionTest(TestCase):

    fixtures = [
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
        special = Election.objects.get(pk=35)

        self.assertEqual(general.elec_key(), ('2012-11-06', u'FL', u'general', 'prez', 'senate', 'house', 'state_officers', 'state_leg'))
        self.assertEqual(general.elec_key(as_string=True), u'2012-11-06 - FL - general (prez, senate, house, state_officers, state_leg)')

        self.assertEqual(gop_primary.elec_key(), ('2012-08-14', u'FL', u'primary', 'senate', 'house', 'state_leg'))
        self.assertEqual(gop_primary.elec_key(as_string=True), u'2012-08-14 - FL - primary (senate, house, state_leg)')

        self.assertEqual(gop_prez_primary.elec_key(), ('2012-01-31', u'FL', u'primary', 'prez'))
        self.assertEqual(gop_prez_primary.elec_key(as_string=True), u'2012-01-31 - FL - primary (prez)')

        self.assertEqual(special.elec_key(), ('2011-09-20', u'FL', 'special', u'primary', 'state_leg'))
        self.assertEqual(special.elec_key(as_string=True), '2011-09-20 - FL - special - primary (state_leg)')

    def test_general_elec_validation_rules(self):
        """General elections must have validation rules"""
        general = Election.objects.get(pk=4)
        # Generals must have at least one office type selected
        offices = [
            'prez',
            'senate',
            'house',
            'gov',
            'state_officers',
            'state_leg',
        ]
        for office in offices:
            setattr(general, office, False)
        self.assertRaises(ValidationError, general.clean)
        # Restore one office
        general.prez = True

        # Primary elec fields should not be selected
        # Test primary_type
        general.primary_type = 'closed'
        self.assertRaises(ValidationError, general.clean)
        general.primary_type = ''

    def test_primary_elec_validation_rules(self):
        """Primary elections must have validation rules"""
        gop_prez_primary = Election.objects.get(pk=31)

        # Primary race_type must have a primary_type (e.g. closed, open, blanket)
        gop_prez_primary.primary_type = ""
        self.assertRaises(ValidationError, gop_prez_primary.clean)

        # Primary race_type of other represents an edge case that requires explanation
        gop_prez_primary.primary_type = "other"
        self.assertRaises(ValidationError, gop_prez_primary.clean)


class LogTest(TestCase):

        fixtures = [
            'test_log_model',
        ]

        def test_log_key(self):
            """Log key returns info on state, date and subject of conversation"""
            kwargs = {
                "follow_up": None,
                "notes": "This is a test.",
                "gdoc_link": "",
                "state_id": "KS",
                "contact": None,
                "user_id": 9,
                "formal_request": False,
                "date": "2013-03-28",
                "org_id": 15,
                "subject": "Test subject line"
            }
            log = Log(**kwargs)
            log.save()
            self.assertEqual(log.log_key(),  ('KS', '2013-03-28', 'Test subject line'))
            self.assertEqual(log.log_key(as_string=True),  'KS - 2013-03-28 - Test subject line')

            # Test with contact
            contact = Contact.objects.all()[0]
            log.contact = contact
            log.save()
            expected = (
                'KS',
                '2013-03-28',
                u'Williams (Kansas Secretary of State elections division)',
                'Test subject line',
            )
            self.assertEqual(expected, log.log_key())


class VolunteerTest(TestCase):
    fixtures = [
        'test_state_status',
    ]

    def test_status_entry(self):
        v = Volunteer.objects.get(user__username="testuser")
        status = v.status_entry()
        self.assertEqual(len(status), 2)
        self.assertEqual(status['full_name'], "John Smith")
        self.assertEqual(status['website'], "http://example.com/~testuser/")


class StateTest(TestCase):
    fixtures = [
        'test_state_status',
    ]

    def test_status_entry(self):
        s = State.objects.get(pk="KS")
        status = s.status_entry()
        self.assertEqual(status['postal'], "KS")
        self.assertEqual(status['name'], "Kansas")
        self.assertEqual(status['metadata_status'], "partial")
        self.assertEqual(len(status['volunteers']), 1)
        self.assertEqual(status['volunteers'][0]['full_name'], "John Smith")
