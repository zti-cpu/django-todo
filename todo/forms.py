from django.forms import ModelForm
from .models import Todo


# создание модели для пользователей
class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'memo', 'important']
