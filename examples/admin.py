from django.contrib import admin
from django import forms
from .models import Product, Review

try:
    from django_jsonform.widgets import (
        JSONFormWidget,
    )  # Essayer d'importer depuis .widgets
except ImportError:
    try:
        from django_jsonform.forms import (
            JSONFormWidget,
        )  # Essayer d'importer depuis .forms
    except ImportError:
        # Si les deux échouent, cela pourrait indiquer un problème plus profond
        # ou une structure d'importation différente pour la version installée.
        # Pour l'instant, on lève une exception plus claire si aucun ne fonctionne.
        raise ImportError(
            "Impossible d'importer JSONFormWidget depuis django_jsonform.widgets ou django_jsonform.forms. Vérifiez votre installation et la documentation de django-jsonform."
        )


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            "attributes": JSONFormWidget(
                schema={
                    "type": "object",
                    "title": "Attributes",
                    "properties": {
                        "Test": {"type": "string"},
                        "Total": {"type": "string"},
                    },
                }
            )
        }


class ReviewAdminForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = "__all__"
        widgets = {
            "pros_cons": JSONFormWidget(
                schema={
                    "type": "object",
                    "title": "Points Positifs et Négatifs",
                    "properties": {
                        "+": {
                            "type": "array",
                            "title": "Points Positifs (+)",
                            "items": {
                                "type": "string",
                            },
                            "format": "textarea",  # Chaque élément de la liste sera une ligne dans le textarea
                        },
                        "-": {
                            "type": "array",
                            "title": "Points Négatifs (-)",
                            "items": {
                                "type": "string",
                            },
                            "format": "textarea",  # Chaque élément de la liste sera une ligne dans le textarea
                        },
                    },
                }
            )
        }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ("name",)
    search_fields = ("name",)  # Important pour l'autocomplete dans ReviewAdmin


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    form = ReviewAdminForm
    list_display = (
        "get_product_names",
    )  # Changer pour la nouvelle méthode d'affichage
    autocomplete_fields = ["products"]  # Active l'autocomplétion pour le champ products

    def get_product_names(self, obj):
        return ", ".join([p.name for p in obj.products.all()])

    get_product_names.short_description = "Products"
