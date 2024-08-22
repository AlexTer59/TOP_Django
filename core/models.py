from django.db import models


class TaskStatus(models.Model):
    status = models.CharField(max_length=100, verbose_name='Статус задачи')

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = 'Статус задачи'
        verbose_name_plural = 'Статусы задач'


class Task(models.Model):
    status = models.ForeignKey(TaskStatus,
                               blank=True,
                               null=True,
                               on_delete=models.SET_NULL,
                               related_name='tasks_status',
                               verbose_name='Статус задачи')
    task = models.CharField(max_length=256, verbose_name='Задача')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


