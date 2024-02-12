from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseNotFound
from .utils import decode_Payload
from api.models import User, AvatarUploadForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import User
import base64, os
from django.conf import settings
from dataclasses import dataclass
import json
import re

@dataclass
class registerPostParameters():
	pseudo: str


def avatar(request):
	if request.method != 'GET':
		return JsonResponse({'error': 'Invalid request method'}, status=405)
	payload = decode_Payload(request)
	if not payload:
		return JsonResponse({'error': 'User ID not provided'}, status=400)
	user_id = payload.get('user_id')
	if not user_id:
		return JsonResponse({'error': 'User ID not provided'}, status=400)
	user = get_object_or_404(User, id=user_id)
	avatar_data = None
	if user.avatar and os.path.exists(user.avatar.path):
		with open(user.avatar.path, 'rb') as avatar_file:
			avatar_data = base64.b64encode(avatar_file.read()).decode('utf-8')
	else:
		# set the default avatar
		default_avatar_path = os.path.join(settings.MEDIA_ROOT, 'avatars', 'default_avatar.png')
		with open(default_avatar_path, 'rb') as f:
			avatar_data = base64.b64encode(f.read()).decode('utf-8')
	return JsonResponse({'avatar': avatar_data})

		
@login_required	
def upload_avatar(request):
	if request.method == 'POST':
		payload = decode_Payload(request)
		if not payload:
			return JsonResponse({'error': 'User ID not provided'}, status=400)
		user_id = payload.get('user_id')
		if not user_id:
			return JsonResponse({'error': 'User ID not provided'}, status=400)
		user = get_object_or_404(User, id=user_id)
		form = AvatarUploadForm(request.POST, request.FILES, instance=request.user)
		if form.is_valid() and request.user == form.instance:
			if user.avatar and os.path.exists(user.avatar.path) and user.avatar.path != '/app/backend/media/avatars/default_avatar.png':
				os.remove(user.avatar.path) 
			form.save()
			return HttpResponse(status=200)
	return JsonResponse({'error': 'Invalid form submission'}, status=400)


@login_required	
@permission_classes([IsAuthenticated])
def get_history(request, user_profil):
	if request.method != 'GET':
		return HttpResponseNotFound(status=404)
	payload = decode_Payload(request)
	user_id = payload.get('user_id')
	if (not user_id):
		return HttpResponseNotFound(status=404)
	if (User.objects.filter(username=user_profil).exists()):
		user = User.objects.get(username=user_profil)
		all_games = user.get_all_games()
		return JsonResponse({'all_games': all_games}, safe=False)
	elif (User.objects.filter(pseudo=user_profil).exists()) :
		user = User.objects.get(pseudo=user_profil)
		all_games = user.get_all_games()
		return JsonResponse({'all_games': all_games}, safe=False)
	return HttpResponseNotFound(status=404)
	
@login_required	
@permission_classes([IsAuthenticated])
def get_user(request, user_profil):
	if request.method != 'GET':
		return HttpResponseNotFound(status=404)
	payload = decode_Payload(request)
	user_id = payload.get('user_id')
	if not user_id:
		return HttpResponseNotFound(status=404)
	if (User.objects.filter(username=user_profil).exists()):
		if (User.objects.get(username=user_profil).id == user_id):
			user = User.objects.get(username=user_profil)
			user_win = user.get_total_wins()
			user_loss = user.get_total_losses()
			data = {
				'User_ID': user_id,
				'username': user.username,
				'pseudo': user.pseudo,
				'email': user.email,
				'win': user_win,
				'lose': user_loss,
			}
			return JsonResponse(data, safe=False)
	if (User.objects.filter(pseudo=user_profil).exists()):
		user = User.objects.get(pseudo=user_profil)
		user_win = user.get_total_wins()
		user_loss = user.get_total_losses()
		data = {
			'pseudo': user.pseudo,
			'win': user_win,
			'lose': user_loss,
		}
		return JsonResponse(data, safe=False)
	return HttpResponseNotFound(status=404)


  
@login_required
def add_friend_request(request, userToAddName):
	# Get the two user
	currentUser = request.user
	print(currentUser)
	userToAdd = get_object_or_404(User, pseudo=userToAddName)
	print(userToAdd)
	# Add the userToAdd to the friendlist if is not already in
	if userToAdd not in  currentUser.friendlist.all():
		currentUser.friendlist.add(userToAdd)
		currentUser.save()
		return HttpResponse("Friend added to the friendlist", status=200)
	else:
		return HttpResponse("Friend is already in the friendlist", status=400)

@login_required
def my_friends(request):
	user = request.user
	friend_list = list(user.friendlist.values('pseudo', 'user_is_connected', 'user_is_in_game', 'user_is_looking_game', 'user_is_looking_tournament').order_by('-user_is_connected', "pseudo"))
	return JsonResponse({'friend_list': friend_list})

def isFriend(request, userToAddName):
	if not request.method == 'GET':
		return HttpResponseNotFound(status=404)
	payload = decode_Payload(request)
	user_id = payload.get('user_id')
	if (not user_id):
		return HttpResponseNotFound(status=404)    
	currentUser = request.user
	if (User.objects.filter(pseudo=userToAddName).exists):
		print("exist")
	userToAdd = User.objects.get(pseudo=userToAddName)
	print(userToAdd)
	# userToAdd = get_object_or_404(User, username=userToAddName)
	print(currentUser.friendlist.all())
	is_friend = userToAdd in currentUser.friendlist.all()
	print(is_friend)
	if (is_friend):
		return HttpResponseNotFound(status=200)
	return HttpResponseNotFound(status=400)

@login_required
@permission_classes([IsAuthenticated])
def username(request):
	if not request.method == 'GET':
		return HttpResponseNotFound(status=404)
	payload = decode_Payload(request)
	user_id = payload.get('user_id')
	if (not user_id):
		return HttpResponseNotFound(status=404)
	if (not User.objects.filter(id=user_id)):
		return HttpResponseNotFound(status=404)
	user = User.objects.get(id=user_id)
	data = {
		'username': user.username,
	}
	return JsonResponse(data, safe=False)

@login_required
@permission_classes([IsAuthenticated])
def pseudo(request):
	if not request.method == 'GET':
		return HttpResponseNotFound(status=404)
	payload = decode_Payload(request)
	user_id = payload.get('user_id')
	if (not user_id):
		return HttpResponseNotFound(status=404)
	if (not User.objects.filter(id=user_id)):
		return HttpResponseNotFound(status=404)
	user = User.objects.get(id=user_id)
	data = {
		'pseudo': user.pseudo,
	}
	return JsonResponse(data, safe=False)

@login_required
@permission_classes([IsAuthenticated])
def registerpseudo(request):
	if not request.method == 'POST':
		return HttpResponseNotFound(status=404)
	payload = decode_Payload(request)
	user_id = payload.get('user_id')
	if (not user_id):
		return HttpResponseNotFound(status=404)
	if (not User.objects.filter(id=user_id)):
		return HttpResponseNotFound(status=404)
	user = User.objects.get(id=user_id)
	try:
		data = registerPostParameters(**json.loads(request.body))
	except Exception  as e:
		return HttpResponse(status=400, reason="Bad request: " + str(e))
	if User.objects.filter(pseudo=data.pseudo).exists():
			return HttpResponse(reason="Conflict: Pseudo already exists.", status=409)
	regexPseudo = r'^[a-zA-Z0-9_-]+$'
	if not re.match(regexPseudo, data.pseudo):
			return JsonResponse({'error': 'Username not valid'})
	user.pseudo = data.pseudo
	user.save()
	return HttpResponse(status=200)

@permission_classes([IsAuthenticated])
def isUserLoggedIn(request):
	if request.method != 'GET':
		return HttpResponseNotFound(status=404)
	payload = decode_Payload(request)
	if (not payload):
		return HttpResponseNotFound(status=404)
	user_id = payload.get('user_id')
	if (not user_id):
		return HttpResponseNotFound(status=404)
	else:
		print("yeah")
		return HttpResponseNotFound(status=200)
	
def change_user_status(request, status):
	if request.method != 'PATCH':
		return HttpResponseNotFound(status=404)
	payload = decode_Payload(request)
	if (not payload):
		return HttpResponseNotFound(status=404)
	user_id = payload.get('user_id')
	if (not user_id):
		return HttpResponseNotFound(status=404)
	if (not User.objects.filter(id=user_id)):
		return HttpResponseNotFound(status=404)
	user = User.objects.get(id=user_id)
	if (status == 'leaving'):
		user.user_is_connected = False
	else :
		user.user_is_connected = True
	user.save()
	return HttpResponseNotFound(status=200)
	
	