from rest_framework.views import APIView
from rest_framework.decorators import api_view

from rest_framework.response import Response
from rest_framework import status

from .models import User, Friendship, FriendshipRequest
from .serializers import UserSerializer, FriendshipSerializer, FriendshipRequestSerializer

from django.db.models import Q


@api_view(['GET', 'POST'])
def list_all_users(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(
            {
                "message": "User created",
                "code": status.HTTP_201_CREATED,
                "data": serializer.data
            })


@api_view(['GET'])
def user_detail(request, pk):
    user = User.objects.filter(id=pk)

    if not user.exists():
        return Response({
            'code': status.HTTP_404_NOT_FOUND,
            'message': 'User not found',
            'data': None
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user[0], many=False)

    return Response({
        'code': status.HTTP_200_OK,
        'message': None,
        'data': serializer.data
    })


@api_view(['GET'])
def list_users_friends(request, pk):
    friends = Friendship.objects.filter(
        user_1__pk=pk) | Friendship.objects.filter(user_2__pk=pk)
    serializer = FriendshipSerializer(friends, many=True)

    return Response(serializer.data)


@api_view(['POST'])
def add_friend(request, pk, friend_pk):
    user1 = User.objects.get(id=pk)
    user2 = User.objects.get(id=friend_pk)
    friendship_request = FriendshipRequest.objects.filter(
        addressee__pk=pk, destination__pk=friend_pk)
    if friendship_request.exists():
        serializer = FriendshipRequestSerializer(friendship_request[0])
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Friend request is already created',
            'data': serializer.data
        })
    friendship_request = FriendshipRequest.objects.filter(
        addressee__pk=friend_pk, destination__pk=pk)  # Then we must accept this request
    if friendship_request.exists():
        friendship = Friendship(user1=user1, user2=user2)
        friendship.save()
        friendship_request.delete()

        serializer = FriendshipSerializer(friendship)
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Existing friend request was accepted',
            'data': serializer.data
        })

    friendship_request = FriendshipRequest(addressee=user1, destination=user2)
    friendship_request.save()

    serializer = FriendshipRequestSerializer(friendship_request)

    return Response({
        'code': status.HTTP_200_OK,
        'message': 'Friend request created',
        'data': serializer.data
    })


@api_view(['GET'])
def incoming_requests(request, pk):
    user = User.objects.get(id=pk)

    friendship_requests = FriendshipRequest.objects.filter(destination__pk=pk)
    serializer = FriendshipRequestSerializer(friendship_requests, many=True)

    return Response({
        'code': status.HTTP_200_OK,
        'message': None,
        'data': serializer.data
    })


@api_view(['GET'])
def outgoing_requests(request, pk):
    user = User.objects.get(id=pk)
    friendship_requests = FriendshipRequest.objects.filter(addressee__pk=pk)
    serializer = FriendshipRequestSerializer(friendship_requests, many=True)
    return Response({
        'code': status.HTTP_200_OK,
        'message': None,
        'data': serializer.data
    })


@api_view(['POST'])
def accept_request(request, pk, fr_pk):
    user = User.objects.get(id=pk)
    friendship_request = FriendshipRequest.objects.get(id=fr_pk)
    if friendship_request and friendship_request.destination == user:
        friendship = Friendship(
            user_1=user, user_2=friendship_request.addressee)
        friendship.save()
        friendship_request.delete()
        serializer = FriendshipSerializer(friendship)

        return Response({
            'code': status.HTTP_201_CREATED,
            'message': None,
            'data': serializer.data
        })
    return Response({
        'code': status.HTTP_400_BAD_REQUEST,
        'message': 'Friendship request not found',
        'data': None
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def retrieve_status_of_friend(request, pk, fr_pk):
    user = User.objects.get(id=pk)
    friendship = Friendship.objects.filter(
        user_1=user, user_2__pk=fr_pk) | Friendship.objects.filter(user_1__pk=fr_pk, user_2=pk)
    if friendship.exists():
        return Response({
            'code': status.HTTP_200_OK,
            'message': None,
            'status': 'friend'
        })
    friendship_request = FriendshipRequest.objects.filter(
        addressee__pk=pk, destination__pk=fr_pk)
    if friendship_request.exists():
        return Response({
            'code': status.HTTP_200_OK,
            'message': None,
            'status': 'outgoing'
        })
    friendship_request = FriendshipRequest.objects.filter(
        addressee__pk=fr_pk, destination__pk=pk)
    if friendship_request.exists():
        return Response({
            'code': status.HTTP_200_OK,
            'message': None,
            'status': 'incoming'
        })
    return Response({
        'code': status.HTTP_200_OK,
        'message': None,
        'status': 'unknown'
    })
