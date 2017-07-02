Poisson Magique is a Play-by-Post (PbP) RPG email gateway and Web interface
for Role Playing Games.

It is a mail server to help with the GM tasks of modifying and
forwarding emails in a PbP campaign, as the GM itself or as the
different player (character or non-character).

Register an adventure by emailing:

pm-new-campaign@pm

Subject: Campaign Name

At this stage, the campaign has already started.

To add new player character, the GM sends an email to

pm-register-pc@pm

Subject: PC name (e.g., Alice Cooper)

the system replies with the email address for enrolment:

pm-enroll-72jase@pm  (for Alice)
etc.

Then other players email an empty email to the enrolment address and
are signed up.


The GM sends emails to Alice@pm etc or special accounts:

pm-roll-dice@pm for dice rolls
pm-register-npc@pm for NPCs

To send emails as other characters, the GM sends email to as-Alice or
other characters (only once).

The game continues until the GM sends an email to pm-end. If a player
sends an email to pm-end their email address is purged from the
game.

See http://wiki.duboue.net/index.php/Poisson_Magique/Example for a
full example.


For Spanish campaigns, the email goes to

pm-new-campaign-es@pm

and the system is set to Spanish from there on.




WIP, see http://poissonmagique.net for details.


Deployment
----------

To setup the local settings you will need:

* A working SMTP server that will relay messages for this server.
* A redis installation to be used by the systems
* To create a folder for the the mail queues, for example $HOME/run.

Create config/localsettings.py (see sample_localsettings.py).

The default listening port for the SMTP server is 1220 as specified in
config/settings.py. This is the port you will need to configure in
hubbed_hosts for exim4 (see below).

```bash
$ salmon start
$ salmon start --boot config.sender --pid run/sender.pid 
```

To render the end of game reports you will need the following packages
installed:

* pandoc
* texlive
* texlive-latex-extra


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

```bash
  brctl addbr brPM
  ifup brPM
```

Add to /etc/networking/interfaces

```bash
  auto brPM
  iface brPM inet static
    address 10.10.0.50
    netmask 255.255.255.240
```

(Then issue the two rc.local commands.)

In poissonmagique/config/localsettings.py you will be setting

```python
server_name_config = 'your PM_DNS'
relay_name_config = 'localhost'
```

You might also want to set

```python
is_silent_config = True
```

to avoid backscatter spam when using a hubbed host.

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
