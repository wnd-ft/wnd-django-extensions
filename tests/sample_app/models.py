from django.db import models

from wnd_django_extensions import WndModelMixin


class AnSns(models.Model, WndModelMixin):
    sns_id = models.CharField(max_length=50)

    class Meta:
        app_label = 'sample_app'


class User(models.Model, WndModelMixin):
    name = models.CharField(max_length=50)
    an_sns = models.OneToOneField(
        AnSns,
        on_delete=models.CASCADE,
    )

    class Meta:
        app_label = 'sample_app'


class VendorInformation(models.Model, WndModelMixin):
    description = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'sample_app'


class Vendor(models.Model, WndModelMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    corporate_number = models.PositiveIntegerField()
    information = models.OneToOneField(
        VendorInformation,
        on_delete=models.CASCADE,
    )

    class Meta:
        app_label = 'sample_app'


class VendorStaff(models.Model, WndModelMixin):
    email = models.EmailField(max_length=50)
    vendor = models.ForeignKey(Vendor, related_name='staffs', on_delete=models.CASCADE)

    class Meta:
        app_label = 'sample_app'
