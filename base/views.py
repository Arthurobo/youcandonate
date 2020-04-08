from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse

import stripe
stripe.api_key = "sk_test_B4phUrXHGQg9ktEpClL5IfZ3008ZHZZ9dL"
#stripe.api_key = "pk_test_LKJNb7CPxnqOwy5dQNbW4en1"


def index(request):
	return render(request, 'base/index.html')


def charge(request):

	if request.method == 'POST':
		print('Data:', request.POST)

		amount = int(request.POST['amount'])

		customer= stripe.Customer.create(
			email=request.POST['email'],
			name=request.POST['nickname'],
			source=request.POST['stripeToken']
		)
		charge = stripe.Charge.create(
			customer=customer,
			amount = amount*100,
			currency='usd',
			description='Donation'
		)
	return redirect(reverse('success', args=[amount]))


def successMsg(request, args):
	amount = args
	return render(request, 'base/success.html', {'amount':amount})