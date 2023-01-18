from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UrlSerializer
from .models import Url
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
import json

import requests
from bs4 import BeautifulSoup

class UrlView(viewsets.ModelViewSet):
    serializer_class = UrlSerializer
    queryset = Url.objects.all()

    def list(self, request, *args, **kwargs):
        """
        Returns a list of all URLs
        """
        urls = self.queryset
        serializer = UrlSerializer(urls, many=True)
        return Response(serializer.data)

    # def get(self, request, *args, **kwargs):
    #     url = self.get_object()
    #     page = requests.get(url)
    #     soup = BeautifulSoup(page.content, 'html.parser')
    #     text = soup.get_text()
    #     worList = text.split()
    #     wordCount = len(wordList)
    #     return JsonResponse({'word_count': wordCount})

    def post(self, request, *args, **kwargs):
        """
        Returns the word count of a specific URL
        """
        url = json.loads(request.body)['url']
        tags = json.loads(request.body)['selectedTags']
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            text = ""
            # Filtering the soup using the selectedTags
            if len(tags) == 0:
                text = soup.get_text()
            else:
                for tag in tags:
                    text += " ".join([i.text for i in soup.find_all(tag)])
            wordList = text.split()
            wordCount = len(wordList)
            # Counting the occurrences of each word creating a wordOccurences array
            wordOccurences = {}
            for word in wordList:
                if word in wordOccurences:
                    wordOccurences[word] += 1
                else:
                    wordOccurences[word] = 1
            topResults = dict(sorted(wordOccurences.items(), key=lambda x: x[1], reverse=True)[:50])
            # Creating or updating data in Urls
            tagsString = ','.join(tags)
            url = url + '?tag=' + tagsString
            urlObj, created = Url.objects.update_or_create(
                url=url,
                defaults={'result': wordCount}
            )
            return JsonResponse({'result': wordCount, 'top50Results': topResults, 'completed': 'success'})
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e), 'completed': 'fail'})

