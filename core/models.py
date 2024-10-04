from django.db import models
from django.utils import timezone
from user.models import Profile
from datetime import timedelta


class Task(models.Model):
    STATUS_CHOICES = [
        (1, 'Активные'),
        (2, 'Срочные'),
        (3, 'Просроченые'),
        (4, 'Выполненые')
    ]

    status = models.PositiveSmallIntegerField("Статус",
                                              choices=STATUS_CHOICES)
    task = models.TextField(max_length=1024,
                            verbose_name='Задача')
    deadline = models.DateTimeField(default=timezone.now() + timedelta(weeks=1),
                                    verbose_name='Дедлайн')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Дата последнего изменения')
    profile_from = models.ForeignKey(Profile,
                                     related_name='tasks_from',
                                     on_delete=models.CASCADE
                                     )

    def __str__(self):
        return self.task

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class TaskExecutor(models.Model):
    task = models.ForeignKey(Task,
                             related_name='task_executor',
                             on_delete=models.CASCADE,
                             verbose_name='Задача')
    profile = models.ForeignKey(Profile,
                                related_name='executor_profile',
                                on_delete=models.CASCADE,
                                verbose_name='Профиль')

    def __str__(self):
        return f'{self.task.task[0:25]}... => {self.profile}'

    class Meta:
        verbose_name = 'Назначение'
        verbose_name_plural = 'Назначения'


class TaskNote(models.Model):
    note = models.TextField(max_length=1024, verbose_name='Заметка')
    task = models.ForeignKey(Task,
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE,
                             related_name='task_note',
                             verbose_name='Задача')
    created_at = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile,
                                related_name='profile_notes',
                                on_delete=models.CASCADE,
                                verbose_name='Профиль')

    def __str__(self):
        return f'{self.note[:15]}...'

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'


class Feedback(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Имя и фамилия')
    text = models.TextField(max_length=1000,
                            verbose_name='Текст отзыва')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class TaskNoteLike(models.Model):
    note = models.ForeignKey(TaskNote,
                             on_delete=models.CASCADE,
                             related_name='note_likes',
                             )
    profile = models.ForeignKey(Profile,
                                on_delete=models.CASCADE,
                                related_name='profile_likes')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile.user.username} лайкнул заметку "{self.note.note[:20]}..."'

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'

