from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Favorite
from .forms import SearchForm, ProductForm 
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
import random


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})

@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('product')
    favorite_products = Favorite.objects.filter(user=request.user).values_list("product_id", flat=True)
    return render(request, 'favorite_list.html', {'favorites': favorites, 'favorite_products': favorite_products})

def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    # おすすめ商品を取得（メイン商品を除外し、最大3つ）
    all_other_products = list(Product.objects.exclude(id=pk))
    recommended_products = random.sample(all_other_products, min(3, len(all_other_products)))
    products = Product.objects.all()
    favorite_products = Favorite.objects.filter(user=request.user).values_list("product_id", flat=True)
    
    context = {
        'product': product,  # メインの商品
        'recommended_products': recommended_products,  # おすすめ商品
        "products": products, 
        "favorite_products": favorite_products,
    }
    
    return render(request, 'product_detail.html', context)


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('search_app:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_form.html', {'form': form, 'product':product})


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'product_confirm_delete.html', {'product': product})


@login_required
def product_list(request):
    products = Product.objects.all()
    favorite_products = Favorite.objects.filter(user=request.user).values_list("product_id", flat=True)
    context = {"products": products, "favorite_products": favorite_products,}

    return render(request, "search.html", context)


@login_required
def search_view(request):
    form = SearchForm(request.GET or None)
    results = Product.objects.all()
    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            results = results.filter(name__icontains=query) 
            
    category_name = request.GET.get('category')
    if category_name:
        try:
            category = Category.objects.get(name=category_name)
            results = results.filter(category_id=category.id)
        except Category.DoesNotExist:
            results = results.none()
            category = None
            
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        results = results.filter(price__gte=min_price)
    if max_price:
        results = results.filter(price__lte=max_price)
        
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_asc':
        results = results.order_by('price')
    elif sort_by == 'price_desc':
        results = results.order_by('-price')
        
    if request.GET.get('favorite_only') == 'true':
        favorite_products = Favorite.objects.filter(user=request.user).values_list("product_id", flat=True)
        results = results.filter(id__in=favorite_products)
        
    paginator = Paginator(results, 12)# 1 ページに表示する件数を指定
    page_number = request.GET.get('page')# 現在のページ番号を GET リクエストから取得
    page_obj = paginator.get_page(page_number)# 指定されたページの結果を取得
    
    # ここ重要
    # 現在のユーザーのお気に入り商品IDリストを取得
    favorite_products = Favorite.objects.filter(user=request.user).values_list("product_id", flat=True)
    """
    Favorite.objects.filter(user=request.user):
    Favoriteモデルのデータベースを操作するために、Favorite.objectsを使い⇨
    
    ⇨filter(user=request.user)は、userフィールドが現在のリクエストユーザー（request.user）と一致するレコードのみを取得させる。
    なので「現在のユーザーが登録したお気に入り」だけを絞り込んで取得していル状態
    
    .values_list("product_id", flat=True):
    .values_list("product_id")は、取得したお気に入りのレコードから、product_idフィールドの値だけを取り出していて⇨
    ⇨flat=Trueオプションを使うと、product_idフィールドの値をリスト形式で返す（例えば、[1, 2, 3]のような単純なリスト）。
    ⇨なので結果として、現在のユーザーが「お気に入り」に登録した商品IDのリストだけが返しているということ。
    """
    return render(request, 'search.html', {'form': form, 'page_obj': page_obj, 'results': results, "favorite_products": favorite_products,},)
    
@login_required
def product_list(request):
    products = Product.objects.all()        
    favorite_products = Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)
    context = {
        'products': products,
        'favorite_products': favorite_products,  
    }
    
    return render(request, 'search.html', context)

@require_POST
def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        favorite.delete()  # 既にお気に入りなら削除
        is_favorited = False
    else:
        is_favorited = True
        
    return JsonResponse({"is_favorited": is_favorited})# お気に入り状態を返す