from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import (
    Image, VehicleTitle, FireFightingVehicle,
    MunicipalityVehicle, AmbulanceVehicle, Pump,
    ContactUs, VehicleSpecification
)


# ===== Inline برای مشخصات پویا =====
class VehicleSpecificationInline(GenericTabularInline):
    model = VehicleSpecification
    extra = 3
    fields = ['key', 'value', 'order', 'is_active']
    ordering = ['order']
    classes = ['collapse']


# ===== ادمین خودرو آتش نشانی =====
@admin.register(FireFightingVehicle)
class FireFightingVehicleAdmin(admin.ModelAdmin):
    list_display = ['chassis', 'title', 'get_specs_count']
    list_filter = ['title']
    search_fields = ['chassis', 'chassis_english']
    inlines = [VehicleSpecificationInline]

    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'chassis', 'chassis_english', 'image_title', 'img')
        }),
        ('توضیحات تکمیلی', {
            'fields': ('description',),
            'description': 'توضیحات بیشتر درباره خودرو (متن دلخواه)'
        }),
    )

    def get_specs_count(self, obj):
        return obj.specs.count()

    get_specs_count.short_description = 'تعداد مشخصات'


# ===== ادمین خودرو خدمات شهری =====
@admin.register(MunicipalityVehicle)
class MunicipalityVehicleAdmin(admin.ModelAdmin):
    list_display = ['chassis', 'title', 'get_specs_count']
    list_filter = ['title']
    search_fields = ['chassis', 'chassis_english']
    inlines = [VehicleSpecificationInline]

    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'chassis', 'chassis_english', 'image_title', 'img')
        }),
        ('توضیحات تکمیلی', {
            'fields': ('description',),
            'description': 'توضیحات بیشتر درباره خودرو (متن دلخواه)'
        }),
    )

    def get_specs_count(self, obj):
        return obj.specs.count()

    get_specs_count.short_description = 'تعداد مشخصات'


# ===== ادمین خودرو آمبولانس =====
@admin.register(AmbulanceVehicle)
class AmbulanceVehicleAdmin(admin.ModelAdmin):
    list_display = ['chassis', 'title', 'get_specs_count']
    list_filter = ['title']
    search_fields = ['chassis', 'chassis_english']
    inlines = [VehicleSpecificationInline]

    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'chassis', 'chassis_english', 'image_title', 'img')
        }),
        ('توضیحات تکمیلی', {
            'fields': ('description',),
            'description': 'توضیحات بیشتر درباره خودرو (متن دلخواه)'
        }),
    )

    def get_specs_count(self, obj):
        return obj.specs.count()

    get_specs_count.short_description = 'تعداد مشخصات'


# ===== ادمین پمپ =====
@admin.register(Pump)
class PumpAdmin(admin.ModelAdmin):
    list_display = ['pump_model', 'title', 'get_specs_count']
    list_filter = ['title']
    search_fields = ['pump_model']
    inlines = [VehicleSpecificationInline]

    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'pump_model', 'image_title', 'img')
        }),
        ('توضیحات تکمیلی', {
            'fields': ('description',),
            'description': 'توضیحات بیشتر درباره پمپ (متن دلخواه)'
        }),
    )

    def get_specs_count(self, obj):
        return obj.specs.count()

    get_specs_count.short_description = 'تعداد مشخصات'


# ===== ادمین مشخصات فنی =====
@admin.register(VehicleSpecification)
class VehicleSpecificationAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', 'content_type', 'object_id', 'order', 'is_active']
    list_filter = ['content_type', 'is_active']
    search_fields = ['key', 'value']
    ordering = ['content_type', 'order']


# ===== ادمین تصاویر =====
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title_photo', 'image']
    search_fields = ['title_photo']


# ===== ادمین دسته بندی خودروها =====
@admin.register(VehicleTitle)
class VehicleTitleAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']


# ===== ادمین تماس با ما =====
@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'title', 'message']
    search_fields = ['name', 'email', 'title']