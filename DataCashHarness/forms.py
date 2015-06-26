from django.forms import ModelForm
from DataCash.models import *

class SetupForm(ModelForm):
	class Meta:
		model = Transaction
		fields = [
			'account_vTID',
			'pageset_number',
			'txn_merchant_ref', 
			'txn_amount', 
			'txn_address_1',
			'txn_address_2',
			'txn_address_3',
			'txn_postcode',
			'txn_token',
			'txn_cardholder_name',
			'txn_expiry_date',
			'txn_stored_card',
			'txn_capture_method',
			'txn_verify_3ds',
			'txn_cv2_avs',
			'txn_credit_plan'
		]

