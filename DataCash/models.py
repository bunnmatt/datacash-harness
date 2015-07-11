from django.db import models

class Environment(models.Model):
	environment_name = models.CharField(max_length=50)
	environment_endpoint = models.CharField(max_length=250)

	def __str__(self):
		return self.environment_name

class Account(models.Model):
	environment_name = models.ForeignKey('Environment')
	account_vTID = models.CharField(max_length=8, primary_key=True)
	account_name = models.CharField(max_length=25)
	account_password = models.CharField(max_length=100)

	def __str__(self):
		return self.account_vTID
	
class Pageset(models.Model):
	account_vTID = models.ForeignKey('Account')
	pageset_name = models.CharField(max_length=100)
	pageset_number = models.IntegerField(primary_key=True)

	def __str__(self):
		return str(self.pageset_number)

class Transaction(models.Model):
	pageset_number = models.ForeignKey('Pageset')
	account_vTID = models.ForeignKey('Account')

	txn_merchant_ref = models.CharField(max_length=32, unique=True)
	txn_datacash_ref = models.CharField(max_length=16)
	txn_amount = models.DecimalField(max_digits=8, decimal_places=2)
	txn_address_1 = models.CharField(max_length=250)
	txn_address_2 = models.CharField(max_length=250)
	txn_address_3 = models.CharField(max_length=250)
	txn_postcode = models.CharField(max_length=10)
	txn_token = models.CharField(max_length=19, null=True, blank=True)
	txn_cardholder_name = models.CharField(max_length=100, null=True, blank=True)
	txn_expiry_date = models.CharField(max_length=5, null=True, blank=True)
	txn_threeds_user_agent = models.CharField(max_length=250, null=True, blank=True)
	txn_threeds_date_time = models.CharField(max_length=50, null=True, blank=True)
	txn_threeds_pares = models.TextField(null=True, blank=True)
	txn_credit_plan = models.CharField(max_length=25, null=True, blank=True)
	txn_auth_code = models.CharField(max_length=10, null=True, blank=True)

	stored_card_choices = (
		(True, 'Yes'),
		(False, 'No'),
	)

	txn_stored_card = models.BooleanField(choices=stored_card_choices, default=False)

	capture_method_choices = (
		('cnp', 'Cardholder Not Present'),
		('ecomm', 'eCommerce'),
	)
	txn_capture_method = models.CharField(max_length=5, choices=capture_method_choices, default='ecomm')

	verify_3ds_choices = (
		('yes', 'Yes'),
		('no', 'No'),
		('noblock', 'Do not include 3DS block'),
	)
	txn_verify_3ds = models.CharField(max_length=7, choices=verify_3ds_choices, default='yes')

	cv2_avs_choices = (
		(0, 'Accept All [0]'),
		(1, 'AVS must match [1]'),
		(2, 'CV2 must match [2]'),
		(3, 'All must match [3]'),
		(5, 'AVS match/all not checked [5]'),
		(6, 'CV2 match/all not checked [6]'),
		(7, 'All match/all not checked [7])'),
	)
	txn_cv2_avs = models.IntegerField(choices=cv2_avs_choices, default='0')

	def __str__(self):
		return self.txn_merchant_ref





