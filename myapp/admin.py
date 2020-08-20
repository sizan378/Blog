from django.contrib import admin
from .models import Author,Category,Article,Comment


class authorAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    search_fields = ['__str__','details']
    class Meta:
        Model=Author


admin.site.register(Author,authorAdmin)


class categoryAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    search_fields = ['__str__']
    class Meta:
        Model=Category


admin.site.register(Category,categoryAdmin)


class articleAdmin(admin.ModelAdmin):
    list_display = ['__str__','posted_on']
    search_fields = ['__str__']
    list_per_page = 10
    list_filter = ['posted_on','category']

    class Meta:
        Model=Article


admin.site.register(Article,articleAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    search_fields = ['__str__']
    list_per_page = 10


    class Meta:
        Model=Comment


admin.site.register(Comment,CommentAdmin)
