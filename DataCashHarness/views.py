from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

from DataCash.models import *
from DataCash import PaymentGateway

from .forms import SetupForm


def index(request):

	environments = Environment.objects
	form = SetupForm();
	return render(request, 'index.html', {'form' : form, 'environments' : environments})

def setup(request):

	form = SetupForm(request.POST)
	if form.is_valid():
		# Create a transaction object
		transaction = form.save()

		# Obtain the server name to include in the "Return URL" field
		transaction.host_name = request.META["HTTP_HOST"]

		account = get_object_or_404(Account, account_vTID=transaction.account_vTID)
		environment = get_object_or_404(Environment, environment_name=account.environment_name)

		# Create a PaymentGateway object
		paymentGateway = PaymentGateway.DataCashPaymentGateway(environment, account)
		
		DataCashRequest = paymentGateway.createPayment(transaction)
		DataCashResponse = paymentGateway.submitRequest(DataCashRequest.getMessageAsXML())


		return render(request, 'setup.html', {
			'XmlRequest' : DataCashRequest.getMessageAsXML(), 
			'ResponseData' : DataCashResponse.getMessageAsDict(), 
			'XmlResponse' : DataCashResponse.getMessageAsXML()
			})
	else:
		environments = Environment.objects
		return render(request, 'index.html', {'form' : form, 'environments' : environments})
	
def interstitial(request, MerchantReference):
	merchant_ref = MerchantReference
	datacash_ref = request.GET['dts_reference']

	return render(request, 'interstitial.html', {'datacash_ref' : datacash_ref, 'merchant_ref' : merchant_ref})	

def pre(request, MerchantReference):

	transaction = get_object_or_404(Transaction, txn_merchant_ref=MerchantReference)

	# Get the DataCash reference from the data posted back from DataCash
	datacash_ref = request.POST['txn_datacash_ref']

	# Update the transaction object
	transaction.txn_datacash_ref = datacash_ref
	transaction.txn_threeds_date_time = datetime.today().strftime("%Y%m%d %H:%M:%S")
	transaction.txn_threeds_user_agent = request.META["HTTP_USER_AGENT"]
	transaction.save()

	account = get_object_or_404(Account, account_vTID=transaction.account_vTID)
	environment = get_object_or_404(Environment, environment_name=account.environment_name)

	# Create a PaymentGateway object
	paymentGateway = PaymentGateway.DataCashPaymentGateway(environment, account)

	
	DataCashRequest = paymentGateway.authenticatePayment(transaction)
	DataCashResponse = paymentGateway.submitRequest(DataCashRequest.getMessageAsXML())
	PaReq = DataCashResponse.getElementValue('pareq_message')

	return render(request, 'pre.html', {
		'XmlRequest' : DataCashRequest.getMessageAsXML(), 
		'ResponseData' : DataCashResponse.getMessageAsDict(), 
		'XmlResponse' : DataCashResponse.getMessageAsXML(),
		'pareq_message' : PaReq
		})

# This view receives POST data from the ACS redirect
# following 3D Secure authentication, and therefore
# CSRF needs to be disabled to prevent a 403 error
@csrf_exempt
def auth(request):

	transaction = get_object_or_404(Transaction, txn_datacash_ref=request.POST['MD'])
	transaction.txn_threeds_pares = request.POST['PaRes']
	account = get_object_or_404(Account, account_vTID=transaction.account_vTID)
	environment = get_object_or_404(Environment, environment_name=account.environment_name)

	# Create a PaymentGateway object
	paymentGateway = PaymentGateway.DataCashPaymentGateway(environment, account)
		
	DataCashRequest = paymentGateway.authorisePayment(transaction)
	DataCashResponse = paymentGateway.submitRequest(DataCashRequest.getMessageAsXML())

	return render(request, 'auth.html', {
			'transaction' : transaction,
			'XmlRequest' : DataCashRequest.getMessageAsXML(), 
			'ResponseData' : DataCashResponse.getMessageAsDict(), 
			'XmlResponse' : DataCashResponse.getMessageAsXML() 
			})

def fulfil(request):

	transaction = get_object_or_404(Transaction, txn_merchant_ref=request.POST['txn_merchant_ref'])
	transaction.txn_auth_code = request.POST['txn_auth_code']
	transaction.save()

	account = get_object_or_404(Account, account_vTID=transaction.account_vTID)
	environment = get_object_or_404(Environment, environment_name=account.environment_name)

	# Create a PaymentGateway object
	paymentGateway = PaymentGateway.DataCashPaymentGateway(environment, account)
		
	DataCashRequest = paymentGateway.completePayment(transaction)
	DataCashResponse = paymentGateway.submitRequest(DataCashRequest.getMessageAsXML())

	return render(request, 'fulfil.html', {
		'transaction' : transaction,
		'ResponseData' : DataCashResponse.getMessageAsDict(), 
		'XmlRequest' : DataCashRequest.getMessageAsXML(),
		'XmlResponse' : DataCashResponse.getMessageAsXML() 
	})