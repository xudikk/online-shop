from django.db import models
from django.db.models import TextChoices, IntegerChoices
from django.utils.text import slugify

from core.models import User


class Category(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    deleted = models.BooleanField(default=False)

    # soft delete
    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()

        self.ctg_products.all().delete()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class CustomManager(models.Manager):
        def all(self):
            return self.model.objects.filter(deleted=False)

        def get(self, *args, **kwargs):
            return self.model.objects.filter(deleted=False, *args, **kwargs).first()

    objects = CustomManager()


class Brand(models.Model):
    name = models.CharField(max_length=128)
    icon = models.ImageField(upload_to="brand/")
    deleted = models.BooleanField(default=False)

    # soft delete
    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()
        # unga tegishli bo'lgan productlarni ham o'chiramiz!
        self.brand_products.all().delete()

    def __str__(self):
        return self.name

    class CustomManager(models.Manager):
        def all(self):
            return self.model.objects.filter(deleted=False)

        def get(self, *args, **kwargs):
            return self.model.objects.filter(deleted=False, *args, **kwargs).first()

    objects = CustomManager()


# class RateChoice(IntegerChoices):
#


class Product(models.Model):
    name = models.CharField(max_length=128)
    img = models.ImageField(upload_to="products/", max_length=512)
    info = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    stock = models.PositiveIntegerField(default=0)
    deleted = models.BooleanField(default=False)

    # price
    price = models.PositiveIntegerField(default=0)
    price_type = models.CharField(max_length=3, choices=[
        ("UZS", "O'zbek so'mi"),
        ("USD", "Aqsh Dollori"),
        ("RUB", "Rossiya Rubli"),
    ], default="UZS")
    discount = models.IntegerField(default=20)

    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, related_name="brand_products")
    ctg = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="ctg_products")

    def get_price(self):
        return int(self.price * (1-self.discount/100))

    def get_price_with_icon(self):
        price = {
            "USD": f"${self.get_price()}",
            "RUB": f"₽{self.get_price()}",
            "UZS": f"{self.get_price()} So'm",
        }

        return price[self.price_type]

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()

    def save(self, *args, **kwargs):
        # sql yozamiz keyingi darslarda
        result = super(Product, self).save(*args, **kwargs)
        print(getattr(self, "cart_pro"), "\n\n")
        if getattr(self, "cart_pro"):
            for i in self.cart_pro.all():
                i.save()

        return result





class Rate(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    rate = models.SmallIntegerField(default=5, choices=[
        (1, "*"),
        (2, "**"),
        (3, "***"),
        (4, "****"),
        (5, "*****"),
    ])
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_rate")


# saved -> liked
class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_pro")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_cart')
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.PositiveIntegerField(default=0, editable=False)
    status = models.BooleanField(default=True)  # True -> active, False -> zakaz bo'p bo'lgan activmas

    def save(self, *args, **kwargs):
        self.total_price = self.product.get_price() * self.quantity
        return super(Cart, self).save(*args, **kwargs)

    # def get_total_price(self):












