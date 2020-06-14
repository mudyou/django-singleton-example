from django.core.cache import cache
from django.db import models
from django.db.models.manager import Manager


class SingletonModel(models.Model):

    class Meta:
        abstract = True

    # override defualt manager and user privet manager
    objects = None
    __objects = Manager()

    def __str__(self):
        return 'Singleton Object'

    def set_cache(self):
        cache.set(self.__class__.__name__, self)

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)
        self.set_cache()

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls, **kwargs):
        if cache.get(cls.__name__) is None:
            obj, created = cls.__objects.get_or_create(pk=1, defaults=kwargs)
            if not created:
                obj.set_cache()
        return cache.get(cls.__name__)


class ContactUs(SingletonModel):
    support = models.EmailField()
    sales = models.EmailField()
    phone_number = models.CharField(max_length=15)
    landline = models.CharField(max_length=15)
    facebook_link = models.CharField(max_length=250)
    linkedin_link = models.CharField(max_length=250)
    adderess = models.TextField()

    class Meta:
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'
