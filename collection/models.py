from django.db import models
from django.utils import timezone

USERTYPE_VALUES = [("subscriber","subscriber"),
                   ("service seeker","service seeker"),
]

NOTIFYMODE_VALUES = [("email","email"),
                     ("sms","sms"),
]

TIER_VALUES = [("standard","standard"),
                ("gold","gold"),
                ("platinum","platinum"),
]

class Users(models.Model):
    user_id = models.CharField(max_length=50, primary_key=True)
    type_of_user = models.CharField(max_length=15, choices=USERTYPE_VALUES)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=80)
    phone = models.CharField(max_length=20, null=True)
    notify_mode = models.CharField(max_length=6, choices=NOTIFYMODE_VALUES, null=True)
    password = models.CharField(max_length=20)
    credits = models.IntegerField(null=True)
    is_active = models.BooleanField(default=False)

class Guests(models.Model):
    guest_email = models.EmailField(max_length=80)
    guest_password = models.CharField(max_length=20)

class Categories(models.Model):
    cat_id = models.CharField(max_length=50, primary_key=True)
    cat_name = models.CharField(max_length=50)
    cat_desc = models.TextField()

class Areas(models.Model):
    area_id = models.CharField(max_length=50, primary_key=True)
    location = models.CharField(max_length=200)
    zip_codes = models.TextField()

class ServiceLists(models.Model):
    list_id = models.CharField(max_length=50, primary_key=True)
    area = models.ForeignKey(Areas, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    base_price = models.IntegerField()

class Subscriptions(models.Model):
    sub_id = models.CharField(max_length=50, primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    service_list = models.ForeignKey(ServiceLists, on_delete=models.CASCADE)
    tier = models.CharField(max_length=9, choices=TIER_VALUES)

class QRD(models.Model):
    qrd_id = models.CharField(max_length=50, primary_key=True)
    user = models.CharField(max_length=50)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    area = models.ForeignKey(Areas, on_delete=models.CASCADE)
    budget = models.IntegerField()
    timeline = models.IntegerField()
    description = models.TextField()
    short_title = models.CharField(max_length=70,null=True)
    qrd_date = models.DateField(default=timezone.now)
