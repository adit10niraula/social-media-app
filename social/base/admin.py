from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Twitter

# Register your models here.
admin.site.unregister(Group)

#mix profile info into user info
class ProfileInline(admin.StackedInline):
    model = Profile



#exptends user model

class UserAdmin(admin.ModelAdmin):
    model = User
    #just display usename field on admin page
    fields = ['username']
    inlines = [ProfileInline]


#unregister initial 
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Twitter)



