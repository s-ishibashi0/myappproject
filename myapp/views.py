from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, DetailView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import MyappPostForm
from .models import MyappPost, Category
import requests


class WeatherService:
    def __init__(self, city, api_key):
        self.city = city
        self.api_key = api_key
        self.url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ja'

    def get_weather(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # HTTPエラーを発生させる
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}  # エラーメッセージを返す


class IndexView(ListView):
    template_name = 'index.html'
    paginate_by = 12

    def get_queryset(self):
        return MyappPost.objects.order_by('-posted_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 天気情報を取得する処理
        city = 'Tokyo'  # 任意の都市
        api_key = 'd1b593d4c085da080729d45cf6151bd4'  # OpenWeatherMapのAPIキーを設定
        weather_service = WeatherService(city, api_key)
        weather_data = weather_service.get_weather()

        # コンテキストに天気情報を追加
        context['weather'] = weather_data
        context['categories'] = Category.objects.all()
        return context


class CategoryView(ListView):
    template_name = 'index.html'
    paginate_by = 9

    def get_queryset(self):
        category_id = self.kwargs['category']
        return MyappPost.objects.filter(category_id=category_id).order_by('-posted_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class CategoryListView(TemplateView):
    template_name = 'category_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class DetailView(DetailView):
    template_name = 'datail.html'
    model = MyappPost


@method_decorator(login_required, name='dispatch')
class CreateMyappView(CreateView):
    form_class = MyappPostForm
    template_name = "post_myapp.html"
    success_url = reverse_lazy('myapp:post_done')

    def form_valid(self, form):
        postdata = form.save(commit=False)
        postdata.user = self.request.user
        postdata.save()
        return super().form_valid(form)


class PostSuccessView(TemplateView):
    template_name = 'post_success.html'


class SearchView(ListView):
    model = MyappPost
    template_name = 'search_results.html'
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get('q')  # GETリクエストから検索キーワードを取得
        if query:
            # titleフィールドに部分一致するレコードを検索
            return MyappPost.objects.filter(title__icontains=query)
        return MyappPost.objects.none()  # クエリがない場合は空の結果を返す

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')  # 検索キーワードもテンプレートに渡す
        return context
