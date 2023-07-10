from django.shortcuts import render
from .models import Kysong, Tjsong, Song,Ky_pop,Tj_pop
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.http import JsonResponse
from mylist.models import Mylist, Myfolder
import json
from django.contrib.auth.decorators import login_required   # 로그인한 사용자 정보
from django.core.exceptions import ValidationError  # 중복 데이터 에러 처리
from rest_framework.decorators import api_view, permission_classes
# Create your views here.

def song_list(request):
    if request.method == 'POST':
        songs = Tj_pop.objects.all()
    elif request.method == 'GET':
        songs = Tj_pop.objects.all()
    else:
        songs = []

    user_id = request.user
    folders = Myfolder.objects.filter(user_id=user_id)

    data = {'songs': songs, 'folders': folders}

    return render(request, 'songlist/song-list.html', data)



def ky_song_list(request):
    if request.method == 'GET':
        songs = Ky_pop.objects.all()
    elif request.method == 'POST':
        songs = Ky_pop.objects.all()
    else:
        songs = []

    user_id = request.user
    folders = Myfolder.objects.filter(user_id=user_id)

    data = {'songs':songs, 'folders': folders}

    return render(request, 'songlist/ky-song-list.html', data)



def search_view(request):
    query = request.GET.get('query')
    folders = Myfolder.objects.all()
    
    print(query)

    if query:
        words = query.split()  # 검색어를 공백으로 분리하여 단어 리스트 생성

        # 쿼리 조건 생성
        conditions = Q()
        for word in words:
            conditions |= Q(title__icontains=word)  # 대소문자 구분 없이 단어 포함 여부 검색

        results = Song.objects.filter(conditions)

    else:
        results = []
    

    data = {'results': results, 'folders':folders}
    return render(request, 'songlist/search.html', data)

@api_view(['POST'])
@login_required
def add_to_search(request):
    if request.method == 'POST':
        data = request.data
        user = request.user
        list_number = data['listNumber']
        list_name = data['listName']
        title = data['title']
        artist = data['artist']
        ky_number = data['kySongNum']
        tj_number = data['tjSongNum']

        # 중복된 데이터 확인
        duplicate_records = Mylist.objects.filter(
            list_name=list_name,
            title=title,
            artist=artist,
            ky_number_id=ky_number,
            tj_number_id=tj_number,
            list_number_id=list_number,
            user=user
        )

        if duplicate_records.exists():
            return JsonResponse({'status':'error', 'message':'이미 추가된 노래입니다.'})

        # 중복이 없을 경우 데이터베이스에 추가
        cmp = data.get('cmp', '')
        writer = data.get('writer', '')
        mylist = Mylist(
            list_name=list_name,
            user=user,
            title=title,
            artist=artist,
            cmp=cmp,
            writer=writer,
            ky_number_id=ky_number,
            tj_number_id=tj_number,
            list_number_id=list_number
        )
        mylist.save()

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message':'잘못된 요청입니다.'})


@api_view(['POST'])
@login_required
def add_to_tjlist(request):
    if request.method == 'POST':
        data = request.data
        list_number = data['listNumber']
        list_name = data['listName']
        user = request.user
        tj_song_num = data['song_num_id']

        print(data)

        print(tj_song_num)
        song_data = Song.objects.get(tj_song_num=tj_song_num)
        print(song_data)

        # 중복된 데이터 확인
        duplicate_records = Mylist.objects.filter(
            list_name=list_name,
            title=song_data.title,
            artist=song_data.artist,
            tj_number_id=tj_song_num,
            list_number_id=list_number,
            user=user
        )

        if duplicate_records.exists():
            return JsonResponse({'status':'error', 'message':'이미 추가된 노래입니다.'})

        mylist = Mylist(
            list_name = list_name,
            user = user,
            title = song_data.title,
            artist = song_data.artist,
            cmp = song_data.cmp,
            writer = song_data.writer,
            ky_number_id = song_data.ky_song_num_id,
            tj_number_id = song_data.tj_song_num_id,
            list_number_id = list_number
        )
        mylist.save()

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 500, 'message':'잘못된 요청입니다.'})
        

@api_view(['POST'])
@login_required
def add_to_kylist(request):
    if request.method == 'POST':
        data = request.data
        list_number = data['listNumber']
        list_name = data['listName']
        user = request.user
        ky_song_num = data['song_num_id']

        print(data)

        print(ky_song_num)
        song_data = Song.objects.get(ky_song_num=ky_song_num)
        print(song_data)

        # 중복된 데이터 확인
        duplicate_records = Mylist.objects.filter(
            list_name=list_name,
            title=song_data.title,
            artist=song_data.artist,
            ky_number_id=ky_song_num,
            list_number_id=list_number,
            user=user
        )

        if duplicate_records.exists():
            return JsonResponse({'status':'error', 'message':'이미 추가된 노래입니다.'})

        mylist = Mylist(
            list_name = list_name,
            user = user,
            title = song_data.title,
            artist = song_data.artist,
            cmp = song_data.cmp,
            writer = song_data.writer,
            ky_number_id = song_data.ky_song_num_id,
            tj_number_id = song_data.tj_song_num_id,
            list_number_id = list_number
        )
        mylist.save()

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message':'잘못된 요청입니다.'})

    

