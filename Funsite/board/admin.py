from django.contrib import admin

from Funsite.board.models import Post, Category, Reply

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Reply)
