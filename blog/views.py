from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Blog
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list_exe.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        """Метод, выводящий в список статей только те, которые имеют положительный признак публикации."""
        return Blog.objects.filter(is_published=True)

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        """Метод, увеличивающий счетчик просмотров статьи при посещении ее страницы"""
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save(update_fields=['views_count'])
        return obj

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'content', 'preview', 'is_published']
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blog:blog_list')

class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ['title', 'content', 'preview', 'is_published']
    template_name = 'blog/blog_form.html'

    def get_success_url(self):
        """Метод, который после успешного редактирования записи перенаправляет пользователя на просмотр этой статьи."""
        # self.object — это сохранённый экземпляр Blog
        return reverse('blog:blog_detail', args=[self.object.pk])

class BlogDeleteView(DeleteView):
    model = Blog
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:blog_list')
