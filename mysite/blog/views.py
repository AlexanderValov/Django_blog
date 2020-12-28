from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import MultipleObjectsReturned
from django.utils import timezone
from django.db.models.functions import Now
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.auth.decorators import login_required
from pytils.translit import slugify
from django.http import HttpResponse, Http404

from .models import Post, Comment
from .forms import PostForm, SearchForm, FliterForm, CommentForm
from .decorators import group_required


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        search_vector = SearchVector('title', 'body')
        search_query = SearchQuery(query)
        results = Post.objects.annotate(search=search_vector, rank=SearchRank(
            search_vector, search_query)).filter(search=search_query).order_by('-rank')

    context = {
        'form': form,
        'query': query,
        'results': results
    }

    return render(request, 'blog/post/search.html', context)


def post_list(request):
    # sort
    order_by = request.GET.get('order_by')
    if order_by == None:
        order_by = 'publish'
    direction = request.GET.get('direction')
    ordering = order_by
    if direction == 'desc':
        ordering = '-{}'.format(ordering)
    post = Post.objects.all().order_by(ordering)
    paginator = Paginator(post, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # filter by year
    check = ''  # чтобы год не повторялся
    years = ''
    for i in Post.objects.all():
        if str(i.publish.year) not in check:
            years += (
                f'<input type="submit" name="year" value="{i.publish.year}"><br>')
            check += str(i.publish.year)
    # filter by author
    check_author = ''
    authors = ''
    for i in Post.objects.all():
        if str(i.author) not in check_author:
            authors += (
                f'<input type="submit" name="author" value="{i.author}"><br>')
            check_author += str(i.author)

    form = FliterForm(request.GET)
    if form.is_valid():
        if form.cleaned_data['year']:
            posts = post.filter(publish__year=form.cleaned_data['year'])
        elif form.cleaned_data['author']:
            posts = post.filter(author__username=form.cleaned_data['author'])

    context = {
        'posts': posts,
        'order_by': order_by,
        'direction': direction,
        'page': page,
        'form': form,
        'years': years,
        'authors': authors
    }
    return render(request, 'blog/post/list.html', context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # add comments
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.name = request.user
            new_comment.save()
            return redirect(post)
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
    }

    return render(request, 'blog/post/detail.html', context)


@group_required('moderators', 'admins')
def add_post(request):
    new_post = None
    if request.method == 'POST':
        post_form = PostForm(data=request.POST)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.created = timezone.now()
            new_post.author = request.user
            new_post.slug = slugify(post_form.cleaned_data.get("title"))
            new_post.save()
            return redirect(new_post)
    else:
        post_form = PostForm()
    context = {
        'post_form': post_form,
        'new_post': new_post
    }

    return render(request, 'blog/post/new_post.html', context)


@group_required('moderators', 'admins')
def update_post(request, year, month, day, post):
    instance = get_object_or_404(Post, slug=post,
                                 publish__year=year,
                                 publish__month=month,
                                 publish__day=day)
    form = PostForm(request.POST or None,
                    request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.slug = slugify(form.cleaned_data.get("title"))
        instance.save()
        return redirect(instance)
    context = {
        "form": form,
        "instance": instance,
    }
    return render(request, "blog/post/update_post.html", context)


@group_required('admins')
def delete_post(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    post.delete()
    return redirect('blog:post_list')
