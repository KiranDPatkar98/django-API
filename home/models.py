from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# This class is defined as an abstract Django model, denoted by abstract = True in its Meta class.
# Abstract models aren't created in the database but serve as a base for other models to inherit from.


class BaseModel(models.Model):
    uid = models.URLField(primary_key=True, editable=False)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = str(uuid4())
        super().save(*args, **kwargs)


class Todo(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    todo_title = models.CharField(max_length=100)
    todo_description = models.TextField()
    is_done = models.BooleanField(default=False)


class TimingTodo(BaseModel):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)
    timing = models.DateField()
