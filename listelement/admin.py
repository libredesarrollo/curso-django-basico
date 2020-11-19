from django.contrib import admin

from .models import Element, Category, Type, ElementImages
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field


#django export import

class ElementResource(resources.ModelResource):

    #id = Field(attribute="id", column_name="#ID")

    class Meta:
        model = Element
        #exclude = ('title')
        fields = ('id','title','url_clean','category','type')
        #export_order = ('url_clean','id','title')

    #def dehydrate_id(self, e):
    #    return '# %s' % (e.id)

class ElementImagesInline(admin.StackedInline):
    exclude = ('base_cover_name','base_cover_ext')
    model = ElementImages
    extra = 3

class ElementAdmin(ImportExportModelAdmin):
    resource_class=ElementResource
    list_display = ('id','title')
    inlines = [ElementImagesInline]
    

# Register your models here.

class TypeAdmin(admin.ModelAdmin):
    list_display = ('id','title')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','title')

#class ElementAdmin(admin.ModelAdmin):
#    list_display = ('id','title')



admin.site.register(Type, TypeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Element, ElementAdmin)
