from django.db import models


class MenuModel(models.Model):
    title = models.CharField(max_length=255, unique=True,
                             verbose_name='Название меню')
    slug = models.SlugField(max_length=255, unique=True,
                            verbose_name='URL')

    def __str__(self) -> str:
        return self.title


class MenuItem(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название подменю')
    slug = models.SlugField(max_length=255, verbose_name='URL')
    menu = models.ForeignKey(
        MenuModel, related_name='menuitems', on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
