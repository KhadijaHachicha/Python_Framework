from django.contrib import admin
from .models  import Enterprise,Utilisatuer
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id','username','email','is_active','is_superuser','role')
    list_editable = ('username','is_active',)
    search_fields = ('user_id','username','email')
    list_filter = ('is_active','role')
    list_per_page = 1
admin.site.register(Utilisatuer,UserAdmin) 
admin.site.register(Enterprise) 