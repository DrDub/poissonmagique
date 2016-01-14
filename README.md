Poisson Magique is a Play-by-Post RPG email gateway and Web interface for Role Playing Games.

It is a mail server + web interface to help with the GM tasks of modifying and forwarding emails in a PbP campaign.

WIP, see http://poissonmagique.net for details.


Deployment
----------

To setup the local settings you will need:

* A working SMTP server that will relay messages for this server.
* To create a folder for the the mail queues, for example $HOME/run.

Create config/localsettings.py and webapp/localsettings.py (see the
sample_localsettings.py in each folder).

The default listening port for the SMTP server is 1220 as specified in
config/settings.py. This is the port you will need to configure in
hubbed_hosts for exim4 (see below).


$ PYTHONPATH=$PWD python webapp/manage.py syncdb
$ salmon start
$ salmon start --boot config.uploader --pid run/uploader.pid 
$ PYTHONPATH=$PWD python webapp/manage.py runserver

(you'll need to log into the django admin and change the Site from the default example.com)


Exim4 Config
------------

These instructions are to set-up Poisson Magique on a Debian box
(tested on Jessie) with direct internet connection and a fixed IP.

Let's call the machine HOSTNAME with an IP, HOSTIP. These instructions
will enable you to run PossionMagique as an unprivileged user in the
machine, without disruption local emails. For that, you will need a
separate DNS name for PossionMagique, which we will call PM_NAME.

First, you need to set the PM_NAME DNS records so its MX records in
point to HOSTIP.

You will need to configure the host with an internal bridge interface
to avoid Exim to reject PM_NAME emails as pointing to localhost. To do
that install the bridge-utils package and set a local IP in
/etc/interfaces:

  apt-get install bridge-utils

Add to /etc/rc.local

  brctl addbr brPM
  ifup brPM

Add to /etc/networking/interfaces

  auto brPM
  iface brPM inet static
    address 10.10.0.50
    netmask 255.255.255.240

(Then issue the two rc.local commands.)

In poissonmagique/config/localsettings.py you will be setting

server_name_config = 'your PM_DNS'
relay_name_config = 'localhost'

but your PM_DNS has to resolve locally to the bridge interface
(10.10.0.50). So add that line to /etc/hosts:

10.10.0.50 your-PM_DNS

Finally, configure exim4 to be a relay for this SMTP, issue as
root (or using sudo):

dpkg-reconfigure exim4-config

leave 'internet site; mail is sent and received directly using SMTP',
set your email name (different from the name being used for
PoissonMagique, usually HOSTNAME), listen on HOSTIP; 127.0.0.1, do
*not* set PM_DNS as local domain, set it as a domain to relay emails
for. Set 10.10.0.50 as an IP to relay emails.

Finally, add to /etc/exim4/hubbed_hosts (you might need to create that
file):

PM_DNS: 10.10.0.50::1220

(you might need to add also mx.PM_DNS if use an mx.PM_DNS name alias
in your MX records.)

Please note the double double colon, it is the required syntax for
Exim.