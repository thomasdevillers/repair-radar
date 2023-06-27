from django.urls import path
from . import views
from .views import RepairListView, RepairDetailView, RepairCreateView, RepairUpdateView, FeedbackCreateView, FeedbackListView

urlpatterns = [
    path('', RepairListView.as_view(), name='repairadar-home'),
    path('repair/<int:pk>/', RepairDetailView.as_view(), name='repair-detail'),
    path('repair/create/', RepairCreateView.as_view(), name='repair-create'),
    path('repair/<int:pk>/update/', RepairUpdateView.as_view(), name='repair-update'),

    path('feedback/', FeedbackListView.as_view(), name='repair-feedback'),
    path('feedback/create', FeedbackCreateView.as_view(), name='feedback-create'),
]