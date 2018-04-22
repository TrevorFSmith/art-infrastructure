from __future__ import unicode_literals
from datetime import timedelta

from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User


class Artist(models.Model):

    name = models.TextField(blank=False, null=False)
    email = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True, max_length=2048)
    notes = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


class ArtistGroupManager(models.Manager):

    def search(self, search_string):
        terms = normalize_search_string(search_string)
        if len(terms) == 0: return None;
        name_query = ArtistGroup.objects.filter(name__icontains=terms[0])
        for term in terms[1:]:
            name_query = name_query & ArtistGroup.objects.filter(name__icontains=term)
        search_query = name_query
        return search_query.order_by('name')


class ArtistGroup(models.Model):

    """A group of artists who collectively create installations, perhaps also with individual artists."""
    name = models.TextField(blank=False, null=False)
    artists = models.ManyToManyField(Artist)
    url = models.URLField(blank=True, null=True, max_length=2048)
    created = models.DateTimeField(auto_now_add=True)

    objects = ArtistGroupManager()

    class Meta:
        ordering = ['name']

    @models.permalink
    def get_absolute_url(self):
        return ('artwork:artist_group_detail', (), { 'id':self.id })

    def __unicode__(self):
        return self.name


class Photo(models.Model):

    """An image with some metadata to be associated with multiple types of models."""
    image = models.ImageField(upload_to='photo', blank=False)
    title = models.TextField(null=True, blank=True)
    caption = models.TextField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def display_name(self):
        if self.title: return self.title
        return os.path.basename(self.image.name)

    @models.permalink
    def get_absolute_url(self):
        return ('artwork:photo_detail', (), { 'id':self.id })

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return str(self.image)


class EquipmentType(models.Model):

    """A sort of equipment, for example: 'Xenon Fantastico Projector'"""
    name = models.TextField(null=False, blank=False)
    provider = models.TextField(null=True, blank=True)
    url = models.URLField(blank=True, null=True, max_length=1024)
    notes = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    @models.permalink
    def get_absolute_url(self):
        return ('artwork:equipment_type_detail', (), { 'id':self.id })

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Equipment(models.Model):

    """A piece of equipment like a projector or a ladder."""
    name = models.TextField(null=False, blank=False)
    equipment_type = models.ForeignKey(EquipmentType, blank=False, null=False)
    photos = models.ManyToManyField(Photo, blank=True)
    notes = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    @models.permalink
    def get_absolute_url(self):
        return ('artwork:equipment_detail', (), { 'id':self.id })

    class Meta:
        verbose_name_plural = 'equipment'
        ordering = ['name']

    def __unicode__(self):
        return "%s: %s" % (self.equipment_type.name, self.name)


class Document(models.Model):

    """A document associated with an Installation."""
    title = models.TextField(null=True, blank=True)
    doc = models.FileField(upload_to='document', blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """When saving the content, use the title if one isn't provided"""
        if self.title == None or len(self.title) == 0: self.title = str(self.doc)
        if self.title.rfind('/') != -1: self.title = self.title[self.title.rfind('/') + 1:]
        super(Document, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return self.doc.url

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return str(self.doc)


class InstallationSite(models.Model):

    """A location in which art is installed."""
    name = models.TextField(null=False, blank=False)
    location = models.TextField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    photos = models.ManyToManyField(Photo, blank=True)
    equipment = models.ManyToManyField(Equipment, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    @models.permalink
    def get_absolute_url(self):
        return ('art_cloud.front.views.installation_site_detail', (), { 'id':self.id })

    class Meta:
        verbose_name =  'location'
        verbose_name_plural = 'locations'
        ordering = ['name']

    def __unicode__(self):
        return self.name


class InstallationManager(models.Manager):

    def all_open(self):
        return self.filter(closed=None) | self.filter(closed__gt=timezone.now())

    def search(self, search_string):
        terms = normalize_search_string(search_string)
        if len(terms) == 0: return None;
        name_query = Installation.objects.filter(name__icontains=terms[0])
        for term in terms[1:]:
            name_query = name_query & Installation.objects.filter(name__icontains=term)
        search_query = name_query
        return search_query.order_by('name')


class Installation(models.Model):

    """A piece of art"""
    name = models.TextField(null=False, blank=False)
    groups = models.ManyToManyField(ArtistGroup, blank=True)
    artists = models.ManyToManyField(Artist, blank=True)
    user = models.ManyToManyField(User, blank=True)
    site = models.ForeignKey(InstallationSite, null=True, blank=True)
    opened = models.DateTimeField(null=True, blank=True)
    closed = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    photos = models.ManyToManyField(Photo, blank=True)
    documents = models.ManyToManyField(Document, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = InstallationManager()

    def collaborators(self):
        q = User.objects.filter(installation=self) | User.objects.filter(artistgroup__installation=self)
        return q.distinct().order_by('username')

    def is_opened(self):
        if self.is_closed(): return False
        if self.opened == None: return False
        return self.opened < timezone.now()
    is_opened.boolean = True

    def is_closed(self):
        if self.closed == None: return False
        return self.closed < timezone.now()
    is_closed.boolean = True

    @models.permalink
    def get_absolute_url(self):
        return ('artwork:installation_detail', (), { 'id':self.id })

    class Meta:
        verbose_name =  'artwork'
        verbose_name_plural = 'works of art'
        ordering = ['name']

    def __unicode__(self):
        return self.name
