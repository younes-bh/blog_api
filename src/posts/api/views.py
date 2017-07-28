from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (
        ListAPIView,
        RetrieveAPIView,
        UpdateAPIView,
        DestroyAPIView,
        CreateAPIView,
        RetrieveUpdateAPIView
        )
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
    )
from posts.models import Post
from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
    PostCreateUpdateSerializer
    )
from .permissions import IsOwnerOrReadOnly
from .paginations import PostLimitOffsetPagination, PostPageNumberPagination

class PostListAPIView(ListAPIView):
    #queryset = Post.objects.all()
    serializer_class = PostListSerializer
    # This is for searching and oredering with built in rest_framework filters
    # For example http://127.0.0.1:6001/api/posts/?search=switch&ordering=-publish
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content', 'user__first_name', 'user__last_name']
    pagination_class = PostPageNumberPagination

    # This is for using Q search for examplle :http://127.0.0.1:6001/api/posts/?q=real
    def get_queryset(self, *args, **kwargs):
        #queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)
        queryset_list = Post.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains = query)|
                Q(content__icontains = query)|
                Q(user__first_name__icontains = query)|
                Q(user__last_name__icontains = query)
            ).distinct()
        return queryset_list

class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = "slug"
    #lookup_url_kwarg = "slug"

class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    lookup_field = "slug"
    #lookup_url_kwarg = "slug"

    def perform_update(self, serializer):
        serializer.save(user = self.request.user)

class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    lookup_field = "slug"
    #lookup_url_kwarg = "slug"

class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
