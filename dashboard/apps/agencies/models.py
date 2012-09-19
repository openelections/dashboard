from django.db import models
from django.contrib.localflavor.us.models import USStateField
from django.template.defaultfilters import slugify


class Agency(models.Model):
    """Government sources of live and certified election results"""
    name = models.CharField(max_length=75, unique=True)
    slug = models.SlugField(blank=True)
    gov_level = models.CharField(max_length=20, choices=(('county', 'County'), ('state','State'), ('federal','Federal')))
    url = models.URLField(blank=True)

    # Address bits
    street = models.CharField(max_length=75, blank=True)
    city = models.CharField(max_length=75, blank=True)
    state = USStateField()

    fec_page = models.URLField(blank=True, help_text='Link to <a href="http://www.fec.gov/pubrec/cfsdd/cfsdd.shtml">FEC clearinghouse</a> page, if available.')
    description = models.TextField(blank=True, help_text="Notes on data sources, key contacts, records requests, etc.")

    class Meta:
        verbose_name_plural = 'Agencies'

    def __unicode__(self):
        return '%s' % self.name 

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Agency, self).save(*args, **kwargs)

class Link(models.Model):
    agency = models.ForeignKey(Agency)
    url = models.URLField()
    live_or_cert = models.CharField(max_length=4, choices=(('live', 'Live'), ('cert', 'Certified'), ('both', 'Both')))
    descrip = models.CharField(max_length=250, blank=True, help_text="Short description of the data source")

    class Meta:
            abstract = True

    def __unicode__(self):
        return '%s - %s' % (self.agency, self.url)

    def __repr__(self):
        return '<%s - %s>' % (self.agency, self.url)

class DataFormat(models.Model):
    name = models.CharField(max_length=10)
    slug = models.SlugField(primary_key=True)

    def __unicode__(self):
        return '%s' % self.name 
    
class PortalLink(Link):
    """A top-level entry point into an agency's eleciton data.
    
    Agencies often have separate portal sites for live and historical results.
    """

    def __unicode__(self):
        return '%s - %s' % (self.agency, self.url)
    
class ResultLink(Link):
    """Direct link to election results.

    Generally, a results link should  point to a data set for a single election, 
    or a category of similarly structured data sets for a given state.
    """
    formats = models.ManyToManyField(DataFormat, related_name='resultformats')
    #TODO: Add M2M years field to allow granular tracking of data formats over time?
