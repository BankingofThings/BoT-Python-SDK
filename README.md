![Banking of Things Header](readme-header.png)

# BoT-Python-SDK

[![Build Status](https://travis-ci.com/BankingofThings/BoT-Python-SDK.svg?token=ic37boNh1zbtjppb1zLc&branch=master)](https://travis-ci.com/BankingofThings/BoT-Python-SDK)

[comment]: # (Todo replace build status with open source one)

Banking of Things enables your IoT devices to perform seamless autonomous payments on your behalf. 
For more information, visit [bankingofthings.io](https://bankingofthings.io/).

## Getting Started
Visit our official documentation on [docs.bankingofthings.io](http://docs.bankingofthings.io/) for a complete overview. 
The main steps are:
- Setting up your device (e.g. a Raspberry Pi)
- Installing the SDK
- Defining Actions on the [Maker Portal](https://maker.bankingofthings.io/)
- Pairing the device with your phone (iOS only for now, android on the way)
- Trigger actions on your device
- Check results in the [Maker Portal > Dashboard](https://maker.bankingofthings.io/)

## Installation
Clone the repository on your device, for example with ssh, and enter the folder:
```bash
git clone git@github.com:BankingofThings/BoT-Python-SDK.git
cd BoT-Python-SDK
```

### Prerequisites
Make sure you have python installed on your device. The SDK is tested on Python 2.7+. Inside the `venv` we need python 3.

### Install using a virtual environment
First we install `virtualenv` && create an environment `venv` with:
```bash
# For Raspberry Pi
make environment-raspberry

# For Mac OS X
make environment-osx

# For Windows
make environment-windows
```
Then we run our newly created environment like this:
```bash
source venv/bin/activate
```
To exit the virtual environment, type:
```bash
deactivate
```

> From now on, every command you run should be inside the virtual environment, unless specified differently.

### Installing dependencies
To install dependencies run:
```bash 
make install
```

## Running tests
Now that our environment is up & running, we can try to see if it works. To see if the tests are working, simply run:
```bash
make test
```

## Configuration
On your first run, replace YOUR_MAKER_ID with the makerID from your BoT Account and run:
```bash
make server makerID=YOUR_MAKER_ID
```

## Running the server
To run the server normally after you've configured it, simply run in your venv:
```bash
make server
```

## Troubleshooting
If you've paired your device with the QR code that was generated in the root (`qr.png`), it might not have been paired 
and/or activated. There are a couple of solutions to fix this. 

* You can stop and start your server. Simply `CTRL C` to stop and `make server` to start again.
* You can manually call either `make configuration`, `make pair` or `make activate` in your venv to start the specific process. 
 
This will start polling the API 3 times every 5 seconds to pair or activate the device. 

It will only work if you've successfully paired your device with your phone, using the `/pairing` endpoint, 
or the generated QR code `qr.png`. 


## Using the SDK
All of these commands can be run outside of your virtual environment.

### Pairing your device
To get the device information you need to pair the device (usually done with the BoT Companion App)
```bash
curl localhost:3001/pairing
```

### Retrieving actions
To get a list of the actions from the maker that are published & enabled for this specific device:
```bash
curl localhost:3001/actions
```

### Triggering actions
To trigger an action (e.g. send a push notification):
```bash
curl -d '{"actionID":"YOUR_ACTION_ID"}' -H "Content-Type: application/json" -X POST http://localhost:3001/actions
```

## Contributing
All improvements to Banking of Things SDK are very welcome! Currently, we are running a closed beta test, and will be 
going fully open-source soon. We believe your input can help create a lively community and the best version of Banking 
of Things. We’ve already implemented much of the feedback given to us by community members and will continue to do so. 
Join them by contributing to the SDK or by contributing to the documentation.

## Community

### Slack
[Slack](https://bit.ly/JoinBoTSlack) is our main feedback channel for the SDK and documentation.

### Direct feedback
Use the feedback button on the [Maker Portal](https://maker.bankingofthings.io/).

### Meetups
We also organize meetups, e.g. demo or hands-on workshops. Keep an eye on our meetup group for any events coming up soon. 
Here you will be able to see the BoT software in action and meet the team.  

[meetup.com/Amsterdam-ING-Banking-of-Things/](https://meetup.com/Amsterdam-ING-Banking-of-Things/)

## About Banking of Things
After winning the ING Innovation Bootcamp in 2017, Banking of Things is now part of the ING Accelerator Program. 
Our aim is to become the Internet of Things (IoT) payment standard that enables service-led business models.

BoT offers a very trusted connection between human, phone and connected device (thing).
That secure connection is used to enable any of those things to respond to triggers in a desired way. 
For example: a car pays for charging by itself.

We believe BoT offers tremendous business opportunities. However, at heart, we are enthusiasts.
Every member of the team has a passion for innovation. That’s why we love working on Banking of Things. 
