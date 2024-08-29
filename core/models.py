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


class TaskNote(models.Model):
    note = models.TextField(max_length=1000, verbose_name='Заметка')
    task = models.ForeignKey(Task,
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE,
                             related_name='task_note',
                             verbose_name='Задача')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.note[:15]}...'

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'

