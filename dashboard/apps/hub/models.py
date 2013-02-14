from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import PhoneNumberField
from django.contrib.localflavor.us.us_states import US_STATES
from django.db import models
from django.template.defaultfilters import slugify

class Office(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(primary_key=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return '%s' % self.slug

    def __repr__(self):
        return '<%s - %s>' % (self.__class__.__name__, self.slug)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(slugify)
        return super(Office, self).save(*args, **kwargs)

class Organization(models.Model):
    """Government or non-government source of live and certified election results"""
    GOV_LEVELS = (
        ('county', 'County'),
        ('state','State'),
        ('federal','Federal'),
        ('local', 'Local')
    )
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField()
    gov_agency = models.BooleanField(default=False)
    gov_level = models.CharField(max_length=20, blank=True, choices=GOV_LEVELS)
    url = models.URLField(blank=True)
    # Address bits
    street = models.CharField(max_length=75, blank=True)
    city = models.CharField(max_length=75, blank=True)
    state = models.CharField(max_length=2, db_index=True, choices=US_STATES)

    fec_page = models.URLField(blank=True, help_text='Link to <a href="http://www.fec.gov/pubrec/cfsdd/cfsdd.shtml">FEC clearinghouse</a> page, if available.')
    description = models.TextField(blank=True, help_text="Notes on data sources, key contacts, records requests, etc.")

    def __unicode__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Organization, self).save(*args, **kwargs)


class DataFormat(models.Model):
    name = models.CharField(max_length=10)
    slug = models.SlugField(primary_key=True)

    def __unicode__(self):
        return '%s' % self.name

class State(models.Model):
    """Top-level window into state data

    Intended as a resource to track general state information and
    as a skeleton for admin inlines such as election data and FOIA logs

    """
    postal = models.CharField(max_length=2, choices=US_STATES, primary_key=True)
    name = models.CharField(max_length=25, help_text="Full state name")
    note = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return '%s' % self.name

    def __repr__(self):
        return '<%s - %s>' % (self.__class__.__name__, self.postal)

class ElecData(models.Model):
    """Metadata about source of election results from a single state.

    This model is highly denormalized to simplify data entry in admin.
    Allows entering multiple "election/race" combos for a single election date,
    so that we can track both general elections (which assume core data of
    Prez/Senate/House/Gov) and edge case races such as runoffs, recalls, unexpired
    terms, etc. The edge cases should only be entered for core races (P/S/H/G).

    Business rules:
        * On all entries, indicate:
            * if it's certified or live results
            * levels of aggregation for results (precinct, county, state)
            * available data formats
        * General elections are common case, and assumes Prez/Sen/House/Gov
            * Indicate which (if any) non-core races are available (state officers, legislative, local)
            * Do NOT fill in Office if it's a general race
        * Special/runoff/recall elections for federal or gov seats are edge case that should be itemized
            * Requires Office foreign key

    """
    RACE_CHOICES = (
        ('primary', 'Primary'),
        ('general', 'General'),
        ('runoff', 'Runoff'),
        ('recall', 'Recall'),
    )
    RESULT_CHOICES = (
        ('live', 'Live'),
        ('certified', 'Certified'),
        ('unofficial', 'Unofficial'),
    )

    # User meta
    user = models.ForeignKey(User)

    # Election meta
    race_type = models.CharField(max_length=10, choices=RACE_CHOICES, db_index=True)
    start_date = models.DateField(db_index=True, help_text="Some races such as NH and WY pririmaries span multiple days. Most elections, however, are single-day elections where start and end date should match.")
    end_date = models.DateField(db_index=True)
    runoff_for = models.DateField(blank=True, null=True, help_text="If runoff, date this election is a run-off for.")
    special = models.BooleanField(blank=True, default=False, db_index=True, help_text="Is this a special election (i.e. to fill a vacancy for an unexpired term)?")
    #TODO: open_primary = models.BooleanField(blank=True, default=False, help_text="Are partisan candidates on a single ballot?")
    state = models.ForeignKey(State)
    office = models.ForeignKey(Office, blank=True, null=True, help_text="Only fill out if this is a special election for a particular office")
    district = models.IntegerField(blank=True, null=True, db_index=True, help_text="Only fill out for special Congressional Races")

    # Data Source Meta
    organization = models.ForeignKey(Organization, null=True, help_text="Agency or Org that is source of the data")
    portal_link = models.URLField(blank=True, help_text="Link to portal, page or form where data can be found, if available")
    direct_link = models.URLField(blank=True, help_text="Direct link to data, if available")
    result_type = models.CharField(max_length=10, choices=RESULT_CHOICES)
    formats = models.ManyToManyField(DataFormat, help_text="Formats that data is available in")
    absentee_and_provisional = models.BooleanField(default=False, db_index=True, help_text="True if absentee and provisional data available")

    # Reporting levels (aggregation levels(s) at which data is available)
    state_level = models.BooleanField("Racewide", default=False, db_index=True)
    county_level = models.BooleanField("County", default=False, db_index=True)
    precinct_level = models.BooleanField("Precinct", default=False, db_index=True)
    # Congress and state leg are only used when statewide offices are broken down by those units
    cong_dist_level = models.BooleanField("Congressional Distritct", default=False, db_index=True)
    state_leg_level = models.BooleanField("State legislative", default=False, db_index=True)
    level_note = models.TextField(blank=True)

    # Offices covered (results include data for these offices)
    prez = models.BooleanField("President", default=False, db_index=True)
    senate = models.BooleanField("U.S. Senate", default=False, db_index=True)
    house = models.BooleanField("U.S. House", default=False, db_index=True)
    gov = models.BooleanField(default=False, db_index=True)
    state_officers = models.BooleanField("State Officers", default=False, db_index=True, help_text="True if there were races for state-level, executive-branch offices besides Governor, such as Attorney General.")
    state_leg = models.BooleanField("State Legislators", default=False, db_index=True, help_text="True if there were races for state legislators. Do NOT check this for state executive officer races.")

    # General note about data
    note = models.TextField(blank=True, help_text="Data quirks such as details about live results or reason for special election")

    class Meta:
        ordering = ['state', '-end_date']
        verbose_name_plural = 'Election Data Sources'
        unique_together = (
            'race_type',
            'end_date',
            'special',
            'office',
            'state',
            'district',
        )

    def __unicode__(self):
        return self.elec_key(as_string=True)

    def __repr__(self):
        return '<%s - %s>' % (self.__class__.__name__, self.elec_key(as_string=True))

    @property
    def offices(self):
        office_fields = (
            'prez',
            'senate',
            'house',
            'gov',
            'state_officers',
            'state_leg',
        )
        return tuple(attr for attr in office_fields if getattr(self, attr))

    def special_key(self, as_string=False):
        if self.special:
            bits = filter(lambda bit: bit not in ('None', None), ('special', self.office_id, str(self.district)))
        else:
            bits = ()
        if as_string:
            return ', '.join(bits)
        return bits

    def elec_key(self, as_string=False):
        meta = (
            self.start_date.strftime('%Y-%m-%d'),
            self.state_id,
            self.race_type,
        )
        # Race meta: Itemized special election or list of offices
        race_info = self.special_key() or self.offices

        if as_string:
            key = " - ".join(meta) + ' (%s)' %  ', '.join(race_info)
        else:
            key = meta + race_info
        return key

class BaseContact(models.Model):
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=70)
    title = models.CharField(max_length=70, blank=True)
    phone =  PhoneNumberField(blank=True)
    mobile = PhoneNumberField(blank=True)
    email = models.EmailField(max_length=254, blank=True)
    note = models.TextField(blank=True)

    class Meta:
        abstract = True

class Contact(BaseContact):
    org = models.ForeignKey("Organization")

    def __unicode__(self):
        return '%s (%s)' % (self.last_name, self.org)

class Volunteer(BaseContact):
    user = models.OneToOneField(User, blank=True, null=True, help_text="Link volunteer to User with data admin privileges, if he or she has them")
    affil = models.CharField("Affiliation", max_length=254, blank=True)
    twitter = models.CharField(max_length=254, blank=True)
    skype = models.CharField(max_length=254, blank=True)
    states = models.ManyToManyField('State', blank=True)

    def __unicode__(self):
        return '%s (%s)' % (self.last_name, self.org)

class BaseLog(models.Model):
    user = models.ForeignKey(User, help_text="User who entered data for the log")
    date = models.DateField()
    subject = models.CharField(max_length=100)
    gdoc_link = models.URLField(blank=True, help_text="Link to GDoc for extended notes on conversation")
    follow_up = models.DateField(blank=True, null=True, help_text="Date for follow up conversation (e.g. FOIA deadline)")
    notes = models.TextField(blank=True)

    class Meta:
        abstract = True

class Log(BaseLog):
    """Notes, docs and other bits from conversations with election contacts"""
    state = models.ForeignKey(State)
    org = models.ForeignKey(Organization, blank=True, null=True, help_text="If conversation took place with more than one person at an org")
    contact = models.ForeignKey(Contact, blank=True, null=True)
    formal_request = models.BooleanField(default=False, help_text="True if this represents a formal FOIA request")

    class Meta:
        verbose_name_plural = 'FOIA Logs'

    def __unicode__(self):
        return self.log_key(as_string=True)

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.log_key(as_string=True))

    def log_key(self, as_string=False):
        key = (self.state_id, self.date.strftime('%Y-%m-%d'),)
        if self.contact:
            key += (self.contact,)
        key += (self.subject,)
        if as_string:
            key = ' - '.join(key)
        return key

class VolunteerLog(BaseLog):
    """Track correspondence with Volunteers"""
    volunteer = models.ForeignKey(Volunteer)

    def __unicode__(self):
        return self.log_key(as_string=True)

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.log_key(as_string=True))

    def log_key(self, as_string=False):
        key = (self.user, self.date.strftime('%Y-%m-%d'),)
        key += (self.subject,)
        if as_string:
            key = ' - '.join(key)
        return key
