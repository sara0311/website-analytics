from django.urls import path, include
from .views import EventAPIView, APIOne, APITwo, APITwoLinkClicked, APITwoWindowClosed

urlpatterns = [
    path('api/event', EventAPIView.as_view()),
    path('api/event_count', APIOne.as_view()),
    path('api/event/pagination', APITwo.as_view()),
    path('event/apitwo/lc/', APITwoLinkClicked.as_view()),
    path('event/apitwo/wc/', APITwoWindowClosed.as_view()),
    #path('api/play', PlayAPIView.as_view()),
]
