from django.contrib import admin
from django import forms

from .models import Article, Tag, Scope


class ScopeInlineFormset(forms.BaseInlineFormSet):
    def clean(self) -> None:
        has_main_scope = False
        for form in self.forms:
            if has_main_scope and form.cleaned_data.get("is_main", False):
                raise forms.ValidationError(
                    "Статья может иметь только один основной раздел"
                )

            has_main_scope = has_main_scope or form.cleaned_data.get("is_main", False)
        if not has_main_scope:
            raise forms.ValidationError("Не указан основной раздел")
        return super().clean()  # вызываем базовый код переопределяемого метода


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = (ScopeInline,)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
