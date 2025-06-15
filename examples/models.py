from django.db import models


def default_pros_cons():
    return {"+": [], "-": []}


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    attributes = models.JSONField(default=dict)  # Pour le JSON simple clé/valeur

    def __str__(self):
        return self.name


class Review(models.Model):
    products = models.ManyToManyField(  # Changé de ForeignKey à ManyToManyField
        Product,
        related_name="reviews",  # Nom du champ changé en 'products' pour plus de clarté
    )
    pros_cons = models.JSONField(
        default=default_pros_cons
    )  # Pour le JSON avec listes +/-

    def __str__(self):
        product_names = ", ".join([p.name for p in self.products.all()])
        return f"Review for {product_names if product_names else 'N/A'}"
