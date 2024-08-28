from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q, Value
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
from movies.models import FilmWork, PersonFilmWork
import uuid


class MoviesApiMixin:
    def __init__(self):
        self.model = FilmWork
        self.http_method_names = ['get']

    def get_queryset(self):
        queryset = self.model.objects.prefetch_related('persons', 'genres') \
            .values(
            'id',
            'title',
            'description',
            'creation_date',
            'rating',
            'type',
        ).annotate(
            genres=ArrayAgg('genres__name', distinct=True),
            actors=Coalesce(ArrayAgg('persons__full_name',
                                     filter=Q(persons__personfilmwork__role=PersonFilmWork.Roles.ACTOR), distinct=True),
                            Value([])),
            directors=Coalesce(ArrayAgg('persons__full_name',
                                        filter=Q(persons__personfilmwork__role=PersonFilmWork.Roles.DIRECTOR),
                                        distinct=True), Value([])),
            writers=Coalesce(ArrayAgg('persons__full_name',
                                      filter=Q(persons__personfilmwork__role=PersonFilmWork.Roles.WRITER),
                                      distinct=True), Value([])),
        )
        return queryset

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )
        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset),
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        queryset = self.get_queryset().get(pk=uuid.UUID(str(self.kwargs['pk'])))
        return queryset
