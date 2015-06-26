# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "notch-interactive/trusty64-python"
  
  config.vm.provision "shell", inline: <<-SHELL
      sudo ln -sf /usr/bin/python3 /usr/local/bin/python

      sudo aptitude install -y python3-setuptools
      sudo easy_install3 pip

      sudo pip3 install django
      sudo pip3 install xmltodict
      sudo pip3 install django-widget-tweaks
      sudo pip3 install requests

      sudo python /vagrant/manage.py runserver 0.0.0.0:8000
  SHELL

  config.vm.network :forwarded_port, host: 8080, guest: 8000

end
