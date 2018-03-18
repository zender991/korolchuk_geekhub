from django.db import models

class Bookmark(models.Model):
    product_id = models.IntegerField()
    user_id = models.IntegerField()

    # def __str__(self):
    #     return self.id




