from django.shortcuts import render
from django.http import JsonResponse, Http404
from kafka import KafkaConsumer, KafkaProducer
from rest_framework.response import Response
from rest_framework import status
from django.core import serializers
from rest_framework.views import APIView
import json
import datetime
from .serializers import EventSerializer,CountSerializer
from .models import Event
from django.db.models import Count
from rest_framework.pagination import LimitOffsetPagination 
from rest_framework.generics import ListAPIView
from django.core.paginator import Paginator, InvalidPage,EmptyPage, PageNotAnInteger

# Create your views here.

class EventAPIView(APIView):
    def get(self, request, *args, **kwargs):
        e = Event.objects.all()
        serializers = EventSerializer(e, many = True)
        return Response(serializers.data, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        #print(request.data)
        data = json.dumps(request.data)
        #print(data, type(data))
        x = json.loads(data)
        #print(x,type(x))
        #x = json.loads(request.body.decode("utf-8"))
        if not x.get('event_type'):
            return Response("Empty event type", status = status.HTTP_400_BAD_REQUEST)
        event_type = x['event_type']
        choice = {"BUTTON_CLICKED", "LINK_CLICKED", "WINDOW_CLOSED"}
        if not event_type in choice:
            return Response("Invalid event type", status = status.HTTP_400_BAD_REQUEST)

        if not x.get('timestamp'):
            return Response("Empty timestamp", status = status.HTTP_400_BAD_REQUEST)
        try: 
            #print(x['timestamp'], type(x['timestamp']))
            dt = datetime.datetime.strptime(x['timestamp'], "%d/%m/%Y %H:%M:%S")
        except ValueError:
            return Response("Invalid timestamp", status = status.HTTP_400_BAD_REQUEST)

        if not x.get('message'):
            return Response("Empty message", status = status.HTTP_400_BAD_REQUEST)
        #timestamp = data['timestamp']
        #message = data['message']
        #event = {1:event_type, 2:timestamp, 3:message}
        #print('hi')
        producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda x: json.dumps(x).encode('utf-8'), api_version=(0,10,1))
        #producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=EventSerializer, api_version=(0,10,1))
        producer.send('event-analytics', data)
        producer.close()

        """ consumer = KafkaConsumer(bootstrap_servers='localhost:9092',auto_offset_reset='latest', value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        consumer.subscribe(['event-analytics'])

        #print('consumer')
        #print(type(consumer))
        #print(consumer.value)
        for m in consumer:
            #print(m)
            #print(m.value, type(m.value))
            data1 = json.loads(m.value)
            #print(data1, type(data1))
            timestamp = data1['timestamp']
            #print(timestamp, type(timestamp))
            message = data1['message']
            #print(message, type(message))
            event_type = data1['event_type']
            #print(event_type, type(event_type))
            e = Event(event_type = event_type, timestamp = timestamp, message = message)
            e.save()
            #print('f') """
        #print(type(data))
        #data1 = json.loads(data)
        d = Event.objects.all().last()
        data1 = d.__dict__
        #data1 = serializers.serialize("json", d)
        #print(type(data1))
        serializers = CountSerializer(data = data1)
        #print(serializers.is_valid())
        if serializers.is_valid():
            #s1 = Event.objects.all()
            #e = 
            s1 = EventSerializer(data1)
            return Response(s1.data, status = status.HTTP_200_OK)
        return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)

class APIOne(APIView):
    def get(self, request, *args, **kwargs):
        #e = Event.objects.annotate(num_events=Count('event_type'))
        e = Event.objects.values('event_type').annotate(num_events=Count('event_type'))
        #print(e)
        #serializers = EventSerializer(e, many = True)
        return Response(e, status=status.HTTP_201_CREATED)

        #for i in e:
         #   print(e[i], e[i].num_events)

class ViewPaginatorMixin(object):
    min_limit = 1
    max_limit = 10

    def paginate(self, object_list, page=1, limit=10, **kwargs):
        try:
            page = int(page)
            if page < 1:
                page = 1
        except (TypeError, ValueError):
            page = 1

        try:
            limit = int(limit)
            if limit < self.min_limit:
                limit = self.min_limit
            if limit > self.max_limit:
                limit = self.max_limit
        except (ValueError, TypeError):
            limit = self.max_limit

        paginator = Paginator(object_list, limit)
        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)
        data = {
            'previous_page': objects.has_previous() and objects.previous_page_number() or None,
            'next_page': objects.has_next() and objects.next_page_number() or None,
            'data': list(objects)
        }
        return data

class APITwo(ListAPIView):
    serializer_class = EventSerializer
    search_fields = ['timestamp', 'event_type', 'message']

    pagination_class = LimitOffsetPagination
    def get_queryset(self, *args, **kwargs):
        eventtype = self.request.query_params.get('event_type', '')
        """ try:
            if eventtype == 'BUTTON_CLICKED':
                eventtype = 'BUTTON_CLICKED'
            elif eventtype == 'LINK_CLICKED':
                eventtype = 'LINK_CLICKED'
            elif eventtype == 'WINDOW_CLOSED':
                eventtype = 'WINDOW_CLOSED'
            event = Event.objects.filter(event_type = eventtype).order_by('id')
            return event
        except TypeError:
            return Response("Invalid event type", status = status.HTTP_400_BAD_REQUEST) """
        
        print(eventtype,type(eventtype))
        choice = {"BUTTON_CLICKED", "LINK_CLICKED", "WINDOW_CLOSED"}
        if not eventtype in choice:
            print(eventtype)
            context = {"response":"Invalid event type"}
            return context
            #return Response(context, status=status.HTTP_400_BAD_REQUEST)

        if eventtype == 'BUTTON_CLICKED':
            eventtype = 'BUTTON_CLICKED'
        elif eventtype == 'LINK_CLICKED':
            eventtype = 'LINK_CLICKED'
        elif eventtype == 'WINDOW_CLOSED':
            eventtype = 'WINDOW_CLOSED'
        #else:
         #   return Response("Invalid event type", status = status.HTTP_400_BAD_REQUEST)
        event = Event.objects.filter(event_type = eventtype).order_by('id')
        return event
        #data = json.loads(first)
        #serializers = EventSerializer(first, many = True)
        #return Response(serializers.data, status=status.HTTP_201_CREATED)

class APITwoLinkClicked(ListAPIView):
    serializer_class = EventSerializer
    search_fields = ['timestamp', 'event_type', 'message']

    pagination_class = LimitOffsetPagination
    def get_queryset(self, *args, **kwargs):
        first = Event.objects.filter(event_type = 'LINK_CLICKED').order_by('id')
        return first

class APITwoWindowClosed(ListAPIView):
    serializer_class = EventSerializer
    search_fields = ['timestamp', 'event_type', 'message']

    pagination_class = LimitOffsetPagination
    def get_queryset(self, *args, **kwargs):
        first = Event.objects.filter(event_type = 'WINDOW_CLOSED').order_by('id')
        return first



#class APITwo(ViewPaginatorMixin, APIView):
 #   def get(self, request, *args, **kwargs):
  #      e = Event.objects.all()
   #     print(e)
    #    first = Event.objects.filter(event_type = 'BUTTON_CLICKED').order_by('id')
     #   second = Event.objects.filter(event_type = 'LINK_CLICKED')
      #  third = Event.objects.filter(event_type = 'WINDOW_CLOSED')

       # print(first)

        #serialized = EventSerializer(first, many=True)
        #return JsonResponse({"events": self.paginate(serialized.data)})
        
        """ f = Paginator(first, 10)
        #s = Paginator(second, 5)
        #t = Paginator(third, 5)

        page = request.GET.get('page') or 1
        try:
            current_page = f.page(page)
        except InvalidPage as e:
            page = int(page) if page.isdigit() else page
            context = {
                'page_number': page,
                'message': str(e)
            }
            return JsonResponse(context, status=404)
        context = {
            'events': list(current_page)
        }
        return JsonResponse(context) """
    
        #data = json.loads(f)

        #return Response(data, status=status.HTTP_201_CREATED)