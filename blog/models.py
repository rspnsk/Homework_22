from django.db import models
from django.utils import timezone

class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    content = models.TextField(verbose_name='Содержимое')
    preview = models.ImageField('Превью', upload_to='blog/previews/', blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', default=timezone.now)
    is_published = models.BooleanField('Опубликовано', default=False)
    views_count = models.PositiveIntegerField('Просмотры', default=0)

    class Meta:
        verbose_name = 'Запись блога'
        verbose_name_plural = 'Записи блога'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
