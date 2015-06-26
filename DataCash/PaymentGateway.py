# This class handles connectivity to the DataCash payment gateway
# XML messages can be sent to the DPG to process and query transactions


import urllib.parse
import urllib.request
import xml.sax.saxutils as su
import xml.etree.ElementTree as ET
import time
import xmltodict
import os


# Import Django templating to construct XML messages
from django.template import Context, Template, loader
from django.shortcuts import render

class DataCashPaymentGateway:

	def __init__(self, environment, account):
		self.url = environment.environment_endpoint
		self.client = account.account_vTID
		self.password = account.account_password
		self.environment = environment
		self.account = account
		self.logDirectory = os.path.dirname(os.path.abspath(__file__)) + '/logs/'

		
	def submitRequest(self, request):
		# Log the request message
		logFileName = self.logDirectory + 'logfile.txt'
		logFile = open(logFileName, 'a')
		logFile.write('Time: ' + str(time.ctime(int(time.time()))) + '\n')
		logFile.write(request + '\n \n')
		logFile.close()
		
		# Send the request message to the DataCash endpoint
		gatewayRequest = urllib.request.Request(self.url, request.encode('utf-8'))
		gatewayResponse = urllib.request.urlopen(gatewayRequest)
		responseMessage = DataCashResponse(gatewayResponse)
		
		# Log the response message
		logFile = open(logFileName, 'a')
		logFile.write('Time: ' + str(time.ctime(int(time.time())))  + '\n')
		logFile.write('HTTP Status: ' + str(responseMessage.status) + '\n')
		logFile.write(responseMessage.content + '\n \n')
		logFile.close()

		return responseMessage
		
	def createPayment(self, transaction):
		template_name = 'setup.xml'
		return DataCashRequestMessage(transaction, self.environment, self.account, template_name)

	def authenticatePayment(self, transaction):
		template_name = 'pre.xml'
		return DataCashRequestMessage(transaction, self.environment, self.account, template_name)

	def authorisePayment(self, transaction):
		template_name = 'auth.xml'
		return DataCashRequestMessage(transaction, self.environment, self.account, template_name)

	def completePayment(self, transaction):
		template_name = 'fulfil.xml'
		return DataCashRequestMessage(transaction, self.environment, self.account, template_name)



class DataCashMessage:
	def getMessageAsDict(self):
		return xmltodict.parse(self.content)

	def getMessageAsHTML(self):
		return su.escape(self.content)

	def getMessageAsXML(self):
		return self.content



class DataCashRequestMessage(DataCashMessage):
	def __init__(self, transaction, environment, account, template_name):
		self.template = loader.get_template(template_name)
		self.context = Context({'transaction' : transaction, 'environment' : environment, 'account' : account})
		self.content = self.template.render(self.context)


		
class DataCashResponse(DataCashMessage):

	def __init__(self, httpResponse):
		self.status = httpResponse.status
		self.reason = httpResponse.reason
		self.content = httpResponse.read().decode(encoding='UTF-8')	
		self.xmlObject = ET.fromstring(self.content)
		
	def getElementValue(self, elementName):
		# Simple function to return the value of a given XML element in the response
		# We are only concerned with finding the first occurrence of a named element
		# anywhere in the XML response
		xPath = './/'+elementName
		element = self.xmlObject.find(xPath)
		if element is None:
			return element
		else:
			value = element.text
			return value		