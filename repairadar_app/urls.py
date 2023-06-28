from django.urls import path
from . import views
from .views import resolution_chart, RepairListView, RepairDetailView, RepairCreateView, RepairUpdateView, RepairDeleteView, FeedbackCreateView, FeedbackListView, UserRepairListView, RepairUpdateView, RepairDeleteView, OrderRepairsByUrgencyView

urlpatterns = [
    path('', RepairListView.as_view(), name='repairadar-home'),
    path('repair/<int:pk>/', RepairDetailView.as_view(), name='repair-detail'),
    path('repair/create/', RepairCreateView.as_view(), name='repair-create'),
    path('repair/<int:pk>/update/', RepairUpdateView.as_view(), name='repair-update'),
    path('repair/<int:pk>/delete/', RepairDeleteView.as_view(), name='repair-delete'),
    path('user/<str:username>', UserRepairListView.as_view(), name="user-repairs"),
    path('feedback/', FeedbackListView.as_view(), name='repair-feedback'),
    path('feedback/create', FeedbackCreateView.as_view(), name='feedback-create'),
    path('orderbyurgency/', OrderRepairsByUrgencyView.as_view(), name='order-by-urgency'),
    path('resolution_chart/', resolution_chart, name='resolution-chart')
]