# datacash-harness
Django-based test harness for the DataCash Payment Gateway.

This is a simple Django based tool for testing connectivity and messaging to the [DataCash Payment Gateway](http://www.mastercard.com/gateway/payment-processing/online-credit-card-and-debit-card-payment-processing.html).

## Django Apps

There are two Django apps included in the repository:

### DataCash

Contains the functionality necessary to send and receive payment XML messages to the payment gateway.

### DataCashHarness

Provides a set of simple web pages to set up payment sessions, and inspect the request and response messages in your web browser.

## Getting Started

### Using Vagrant

There is a `Vagrantfile` to get you up and running with a [Vagrant](http://vagrantup.com) development environment.  
Once you've installed Vagrant so the following:

1. Run `vagrant up` to boot up your virtual machine.  This will install all the necessary Python modules and run `manage.py` to start the test server.  The test server is accessible on port 8080 of your host machine.
2. SSH into your Vagrant machine and run: `python manage.py migrate` to create the database tables.
3. Run `python manage.py createsuperuser` to create an admin superuser
4. If you go to `http://localhost:8080/` you should see the DataCash Harness homepage
5. Log into Django admin at `http://localhost:8080/admin` and create the necessary entries in the Environments, Accounts and Pagesets tables.
6. Go to `http://localhost:8080/` and you should be good to place some test payments.
