from django.forms import ModelForm
from .models import MyappPost


class MyappPostForm(ModelForm):
    class Meta:
        # モデルのクラス
        model = MyappPost
        fields = ['category', 'title', 'comment', 'image1', 'image2']
