from django.db import models
import random
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.db.models.signals import pre_save
from ecommerce.utils import unique_slug_generator, get_filename

def upload_image_path(instance,filename):
    new_filename = random.randint(1,10000)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
    return "products/{new_filename}/{final_filename}".format(new_filename=new_filename,final_filename=final_filename)

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name,ext = os.path.splitext(base_name)
    return name,ext

class ProductManager(models.Manager):

    def featured(self):
        return self.get_queryset().filter(featured=True)

    def get_by_id(self,id):
        qs = self.get_queryset().filter(id=id)  #Product.objects === self.get_queryset
        if qs.count()== 1:
            return qs.first()
        return None

class Product(models.Model):
    title           = models.CharField(max_length=120)
    slug            = models.SlugField(blank=True,unique=True)
    description     = models.TextField()
    price           = models.DecimalField(default=0.00,max_digits=100, decimal_places=2)
    image           = models.ImageField(upload_to=upload_image_path,null=True,blank=True)
    featured        = models.BooleanField(default=False)
    timestamp       = models.DateTimeField(auto_now_add=True)
    is_digital      = models.BooleanField(default=False)

    objects = ProductManager()

    def get_absolute_url(self):
        # return "/products/{slug}".format(slug=self.slug)
        return reverse("products:detail",kwargs={"slug":self.slug})

    def __str__(self):
        return self.title
    
    @property
    def name(self):
        return self.name

    def get_downloads(self):
        qs = self.productfile_set.all()
        return qs 



# this code is for generating unique slug 
def product_pre_save_receiver(sender,instance,*args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver,sender=Product)

def upload_product_file_loc(instance, filename):
    slug = instance.product.slug
    if not slug:
        slug = unique_slug_generator(instance.product)
    location = "product/{}".format(slug)
    return location + filename 


class ProductFile(models.Model):
    product         = models.ForeignKey(Product, on_delete=models.CASCADE)
    file            = models.FileField(upload_to=upload_product_file_loc, storage=FileSystemStorage(location=settings.PROTECTED_ROOT))
    free            = models.BooleanField(default=False)
    user_required   = models.BooleanField(default=False)


    def __str__(self):
        return str(self.file.name)

    def get_download_url(self):
        return reverse("products:download",kwargs={"slug":self.product.slug, "pk":self.pk})

    def get_default_url(self):
        return self.product.get_absolute_url()

    @property
    def name(self):
        return get_filename(self.file.name)
