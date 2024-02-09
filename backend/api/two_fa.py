import json
import base64
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django_otp.plugins.otp_totp.models import TOTPDevice
from .models import User
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import pyotp
from rest_framework_simplejwt.tokens import RefreshToken
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib.auth import logout, authenticate, login
from dataclasses import dataclass

@dataclass
class registerPostParameters():
	token : str
	username: str

@permission_classes([IsAuthenticated])
def enable2fa(request):
	try:
		user = request.user
		print(user)
		print("c mon user dans le back:", user.username)
		# Check if the user already has a TOTP device enabled
		if not TOTPDevice.objects.filter(user=user, confirmed=True).exists():
			totp_device = TOTPDevice.objects.create(user=user)
			totp_device.save()
			# Get the TOTPDevice instance associated with the user
			otpauth_url = totp_device.config_url
			user.qrcode = otpauth_url
			print(user.qrcode)
			user.status_2fa = True
			user.save()
			return JsonResponse({'success': True, 'qrcode': user.qrcode}, status=200)
		else:
			return JsonResponse({'success': False, 'error': 'TOTP device already enabled'}, status=400)
	except Exception as e:
		return JsonResponse({'success': False, 'error': str(e)}, status=500)

@permission_classes([IsAuthenticated])
def disable2fa(request):
	user = request.user
	try:
		totp_device = TOTPDevice.objects.get(user=user, confirmed=True)
		totp_device.delete()
		user.status_2fa = False
		user.save()
		return JsonResponse({'success': True, 'message': '2FA disabled successfully'}, status=200)
	except TOTPDevice.DoesNotExist:
		return JsonResponse({'success': False, 'error': 'TOTP device not found'}, status=404)
	except Exception as e:
		return JsonResponse({'success': False, 'error': str(e)}, status=500)

@permission_classes([IsAuthenticated])
def get_2fa_status(request):
	try:
		user = request.user
		print("2FA :", user.status_2fa)
		if (user.status_2fa == True):

			return JsonResponse({
				'two_factor_enabled': True,
				'qrcode': user.qrcode
				}, status=200)
		else:
			return JsonResponse({'two_factor_enabled': False}, status=270)
	except Exception as e:
		return JsonResponse({'error': str(e)}, status=500)

@permission_classes([IsAuthenticated])
def check_totp(request):
	try:
		data = registerPostParameters(**json.loads(request.body))
	except Exception  as e:
		return HttpResponse(status=400, reason="Bad request: " + str(e))
	if not User.objects.filter(username=data.username).exists:
		return HttpResponseNotFound(status=404)
	user = User.objects.get(username=data.username)
	token = data.token
	print(token)
	print(user)
	if verify_totp(user, token):
		# TOTP is valid, proceed with login
		login(request, user)
		# Generate JWT token, access, and refresh
		refresh = RefreshToken.for_user(user)
		jwt_token = str(refresh.access_token)
		refresh_token = str(refresh)
		# Set JWT token in a cookie
		response = JsonResponse({
			'status': 'success',
			'message': 'Login successful',
			'token': jwt_token,
			'refresh_token': refresh_token
		})
		response.set_cookie('refresh_token',refresh_token)
		response.set_cookie('jwt_token', jwt_token)
		return response
	else:
		# TOTP is invalid, show an error message
		return JsonResponse({'status': 'error', 'message': 'Invalid TOTP token'}, status=401)


def verify_totp(user, token):
	try:
		totp_device = TOTPDevice.objects.get(user=user, confirmed=True)
	except TOTPDevice.DoesNotExist:
		print("TOTP device not found for user")
		return False

	if token is None:
		print("Token not provided")
		return False

	print("Token:", token)
	
	secret_key = totp_device.key
	base16_secret_key = secret_key
	secret_bytes = bytes.fromhex(base16_secret_key)
	base32_secret_key = base64.b32encode(secret_bytes).decode()
	
	print("Secret Key (base32):", base32_secret_key)

	totp = pyotp.TOTP(base32_secret_key)

	if (totp.verify(token)):
		return True
	else:
		return False