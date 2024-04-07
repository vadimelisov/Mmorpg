from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from board.filters import PostFilter
from board.forms import PostForm, ReplyForm, SendForm
from board.models import Post, Reply
from sitecore import settings


class PostsList(ListView):
    model = Post
    template_name = 'posts_template.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_logged'] = self.request.user.is_authenticated
        context['current_user'] = self.request.user
        context['user_is_staff'] = self.request.user.is_staff
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail_template.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        replies_by_post_id = Reply.objects.filter(post=self.kwargs['pk']).order_by('-date_posted')
        context['is_logged'] = self.request.user.is_authenticated
        context['replys'] = replies_by_post_id
        return context


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create_template.html'
    context_object_name = 'post_create'
    success_url = '/posts/'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_author = self.request.user
        post.save()
        return super().form_valid(form)


class PostEdit(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    context_object_name = 'post_edit'
    success_url = '/posts/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class ReplyAdd(CreateView):
    form_class = ReplyForm
    model = Reply

    template_name = 'reply_add.html'
    context_object_name = 'reply_create'

    success_url = '/posts/'

    def form_valid(self, form):
        reply = form.save(commit=False)
        reply.author = self.request.user
        reply.post = get_object_or_404(Post, id=self.kwargs['pk'])
        form.save()
        return redirect('post', reply.post.pk)


class Replies(ListView):
    model = Reply
    template_name = 'replies.html'
    context_object_name = 'replies'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Reply.objects.filter(post__post_author_id=self.request.user.pk).order_by('-date_posted')
        context['filter'] = PostFilter(self.request.GET, queryset, request=self.request.user.pk)
        return context


def news_send(request):
    if request.method == 'GET':
        form = SendForm()
        return render(request, 'send_mails.html', {'form': form})
    else:
        form = SendForm(request.POST)
        if form.is_valid():
            content_mail = form.cleaned_data.get('content')
            recievers = []
            for user in User.objects.all():
                if user.email != ' ' or user.email != '':
                    recievers.append(user.email)

            html_mail = render_to_string(
                'send_mails_mail.html',
                {
                    'text': content_mail,
                }
            )

            message = EmailMultiAlternatives(
                subject=f'Новость!',
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=recievers
            )

            message.attach_alternative(html_mail, 'text/html')
            message.send()

            return redirect('/posts/')


def delete_reply(self, pk):
    reply = Reply.objects.get(id=pk)
    reply.delete()
    return redirect('/posts/')


def allow_reply(request, pk):
    reply = Reply.objects.get(id=pk)
    reply.is_allowed = True
    html_mail = render_to_string(
        'reply_sendmail_accepted.html',
        {
            'text': reply.content,
            'post_title': reply.post.title,
            'post_link': f'http://127.0.0.1:8000/posts/{reply.post.pk}',
        }
    )

    message = EmailMultiAlternatives(
        subject=f'Ваш отклик был принят',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[reply.author.email]
    )

    message.attach_alternative(html_mail, 'text/html')
    message.send()
    reply.save()
    return redirect('/posts/')


def delete_post(self, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return redirect('/posts/')
