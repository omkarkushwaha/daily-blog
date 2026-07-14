from django.contrib import admin
from .models import Post, Category, Tag, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ("id", "name")

    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    list_display = ("id", "name")

    search_fields = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "author",
        "category",
        "created_at",
    )

    list_filter = (
        "category",
        "created_at",
        "author",
    )

    search_fields = (
        "title",
        "content",
    )

    ordering = (
        "-created_at",
    )

    date_hierarchy = "created_at"

    filter_horizontal = (
        "tags",
    )

    list_per_page = 10


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "post",
        "created_at",
    )

    search_fields = (
        "user__username",
        "text",
    )

    list_filter = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 20