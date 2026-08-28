from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class Image(models.Model):
    title_photo = models.CharField(max_length=250, null=True, blank=True, verbose_name='عنوان عکس')
    image = models.ImageField(upload_to='')

    def __str__(self):
        return f'{self.title_photo}'

    class Meta:
        verbose_name = 'بارگذاری عکس'
        verbose_name_plural = 'بارگذاری عکس ها'


class VehicleTitle(models.Model):
    title = models.CharField(max_length=200, verbose_name='دسته بندی خودرو')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'دسته بندی خودرو'
        verbose_name_plural = 'دسته بندی خودروها'


# ===== مدل برای مشخصات پویا =====
class VehicleSpecification(models.Model):
    """
    مدل مشخصات پویا - ادمین می‌تواند هر تعداد مشخصه به هر خودرو اضافه کند
    """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     limit_choices_to={
                                         'model__in': ['firefightingvehicle', 'municipalityvehicle',
                                                       'ambulancevehicle', 'pump']
                                     })
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    key = models.CharField(max_length=200, verbose_name='عنوان مشخصه')
    value = models.TextField(verbose_name='مقدار مشخصه')
    order = models.PositiveIntegerField(default=0, verbose_name='ترتیب نمایش')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        verbose_name = 'مشخصه فنی'
        verbose_name_plural = 'مشخصات فنی'
        ordering = ['order']
        unique_together = ['content_type', 'object_id', 'key']

    def __str__(self):
        return f"{self.key}: {self.value[:50]}"


# ===== مدل پایه =====
class BaseVehicle(models.Model):
    """مدل پایه برای تمام خودروها"""
    img = models.ManyToManyField(Image, blank=True, verbose_name='عکس')
    title = models.ForeignKey(VehicleTitle, on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name='دسته بندی خودروها')
    image_title = models.ImageField(upload_to='', null=True, blank=True, verbose_name='عکس اصلی')
    chassis = models.CharField(max_length=100, verbose_name='شاسی')
    chassis_english = models.CharField(max_length=150, verbose_name='شاسی به انگلیسی', null=True, blank=True)

    # ===== فیلد توضیحات تکمیلی (ثابت) =====
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='توضیحات تکمیلی',
        help_text='توضیحات بیشتر درباره خودرو (متن دلخواه)'
    )

    slug = models.SlugField(max_length=400, unique=True, default='', null=False, db_index=True,
                            verbose_name='عنوان در url')

    # ارتباط با مشخصات پویا
    specs = GenericRelation(VehicleSpecification, related_query_name='vehicle')

    class Meta:
        abstract = True

    def get_specs_dict(self):
        """برگرداندن مشخصات به صورت دیکشنری برای استفاده در قالب"""
        return {spec.key: spec.value for spec in self.specs.all()}

    def get_active_specs(self):
        """برگرداندن مشخصات فعال به صورت لیست"""
        return self.specs.filter(is_active=True)


# ===== خودرو آتش نشانی =====
class FireFightingVehicle(BaseVehicle):

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.chassis_english or self.chassis)
        super().save()

    def __str__(self):
        return f'{self.chassis}'

    class Meta:
        verbose_name = 'خودرو آتش نشانی'
        verbose_name_plural = 'خودرو های آتش نشانی'

    def get_absolute_url(self):
        return reverse('single', args={self.slug})


# ===== خودرو خدمات شهری =====
class MunicipalityVehicle(BaseVehicle):

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.chassis_english or self.chassis)
        super().save()

    def __str__(self):
        return f'{self.chassis}'

    class Meta:
        verbose_name = 'خودرو خدمات شهری'
        verbose_name_plural = 'خودرو های خدمات شهری'

    def get_absolute_url(self):
        return reverse('municipality_single', args={self.slug})


# ===== خودرو آمبولانس =====
class AmbulanceVehicle(BaseVehicle):

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.chassis_english or self.chassis)
        super().save()

    def __str__(self):
        return f'{self.chassis}'

    class Meta:
        verbose_name = 'خودرو آمبولانس'
        verbose_name_plural = 'خودروهای آمبولانس'

    def get_absolute_url(self):
        return reverse('ambulance_single', args={self.slug})


# ===== پمپ =====
class Pump(BaseVehicle):
    pump_model = models.CharField(max_length=100, verbose_name='مدل پمپ')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.pump_model)
        super().save()

    def __str__(self):
        return f'{self.pump_model}'

    class Meta:
        verbose_name = 'پمپ آتش نشانی'
        verbose_name_plural = 'پمپ های آتش نشانی'

    def get_absolute_url(self):
        return reverse('pump_single', args={self.slug})


class ContactUs(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام ')
    email = models.EmailField(max_length=200, verbose_name='ایمیل')
    title = models.CharField(max_length=300, verbose_name='عنوان')
    message = models.TextField(verbose_name='متن')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'تماس با ما'
        verbose_name_plural = 'تماس های با ما'