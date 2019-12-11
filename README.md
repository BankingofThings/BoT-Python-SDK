![readme-header](readme-header.png)

[![Build Status](https://travis-ci.com/BankingofThings/BoT-Python-SDK.svg?branch=master)](https://travis-ci.com/BankingofThings/BoT-Python-SDK)

FINN enables your IoT devices to perform seamless autonomous payments on your behalf. 
For more information, visit us at [makethingsfinn.com](https://www.makethingsfinn.com)

# Getting Started
Visit our [official documentation](http://docs.bankingofthings.io/) for a complete overview. 
The main steps are:

- Setting up your device (e.g. a Raspberry Pi)
- Installing the SDK
- Defining Actions on the [Maker Portal](https://maker.bankingofthings.io/)
- Pairing the device with the [Finn Mobile Application](https://docs.bankingofthings.io/mobile-app)
- Trigger actions on your device
- Check results in the [Maker Portal > Dashboard](https://maker.bankingofthings.io/)

# Supported Features
   | Sl. No        | SDK Feature                                | Status      | Remarks |
   | :-----------: |:-------------------------------------------| :-----------| :-------|
   |        1      | Pairing through Bluetooth Low Energy (BLE) | :thumbsup: | Supported with Android Mobile Application |
   |        2      | Pairing through QR Code                    | :thumbsup: | Supported only in Webserver mode using end point /qrcode to get generated QRCode for device to be paired for both iOS and Android Mobile Applications|
   |        3      | Secured HTTP with BoT Service              | :thumbsup: | Supported for all interactions with backend server |
   |        4      | Logging                                    | :thumbsup: | Console Logging is implemented|
   |        5      | Offline Actions                            | :thumbsdown: | Helps to persist the autonomous payments on the device when there is no internet connectivity available. The saved offline actions get completed when the next action trigger happens and internet connectivity is available. This feature is in plan for implementation.|
   
# Installation
Clone the repository on your device and enter the folder:
```bash
git clone https://github.com/BankingofThings/BoT-Python-SDK.git
cd BoT-Python-SDK
```

## Prerequisites
Make sure you have python installed on your device. The SDK is tested on Python 2.7+. Inside the `venv` we need python 3.


## Install using a virtual environment
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
To exit the virtual environment, type the following command. If you execute this, you need to rerun the previous one.
```bash
deactivate
```

> From now on, every command you run should be inside the virtual environment, unless specified differently.

## Installing dependencies
To install dependencies run (inside the venv):
```bash 
make install
```

# Running tests
Now that our environment is up & running, we can try to see if it works. To see if the tests are working, simply run:
```bash
make test
```

# Configuration
Sign in to the [Maker Portal](https://maker.bankingofthings.io/) and get the makerID from your account.
On your first run, replace YOUR_ID with the productID or the makerID from your Maker portal, and run:
```bash
make server makerID=YOUR_ID
```
Webserver supports endpoint `/qrcode` to retrieve the generated Qrcode for the device to pair with the [Finn Mobile Application](https://docs.bankingofthings.io/mobile-app). Make a note of webserver's base url displayed in the above command's output and append `/qrcode`. The Webserver can be accessed remotely from any system connected to same network as that of the device.

Note: You can also use a productID from your product page in the Maker portal, like this: `makerID=PRODUCT_ID`

# Running the server
To run the server normally after you've configured it, simply run in your venv:
```bash
make server
```
The Webserver supports below end points to be consumed by remote clients:
- /qrcode : To retrieve qrcode for device pairing with the [Finn Mobile Application](https://docs.bankingofthings.io/mobile-app)
- /actions : To retrieve and post autonomous payments to the BoT Service
- /pairing : To pair the device if it's not get paired within the max interval of pairing time
- /activate : To enable the devicve for autonomous payments post pairing the device

## Pairing and activating action(s)
Pair your device and activate an action using the companion app either using the BLE Service (Supported only for Android Application) or using the QR code that was generated for the device by accessing the webserver's end point `/qrcode`.

The device QRCode can also be viewed locally on the device by running the `showqr.py` script as shown below:

```bash
export LC_ALL=en_US.UTF-8
python showqr.py
```

OR

You can stop your server (e.g. with `CTRL + C`) or open a separate tab to open `BoT-Python-SDK/storage/qr.png`. 
Then, to open the QR code:
```bash
sudo apt-get install feh
feh storage/qr.png
```

Now you scan it with the Finn Companion App.

After this you can restart the server again with:
```bash
make server
```

# Troubleshooting
If you've paired your device with the QR code that was generated in the root (`qr.png`), it might not have been paired 
and/or activated. There are a couple of solutions to fix this. 

* You can stop and start your server. Simply `CTRL C` to stop and `make server` to start again.
* You can manually call either `make configuration`, `make pair` or `make activate` in your venv to start the specific process. 
 
This will start polling the API 3 times every 5 seconds to pair or activate the device. 

It will only work if you've successfully paired your device with your phone, using the `/pairing` endpoint, 
or the generated QR code `qr.png`. 


# Using the SDK
The following commands can be run outside of your virtual environment.

## Pairing your device
To get the device information you need to pair the device (usually done with the BoT Companion App)
```bash
curl localhost:3001/pairing
```

## Retrieving actions
To get a list of the actions from the maker that are published & enabled for this specific device:
```bash
curl localhost:3001/actions
```

## Triggering actions
To create actions you need to go to the [Maker Portal](https://maker.bankingofthings.io/). 
Follow the steps on the screen to create the action. You will get an actionID at the end.

To trigger an action (e.g. send a push notification):
```bash
curl -d '{"actionID":"YOUR_ACTION_ID"}' -H "Content-Type: application/json" -X POST http://localhost:3001/actions
```

###
If you get an error in which your device is not paired or activated, you can call the following endpoint to continue this process:
```bash
curl localhost:3001/activation
```

# Contributing
Any improvement to the FINN SDK are very much welcome! Our software is open-source and we believe your input can help create a lively community and the best version of FINN. We’ve already implemented much of the feedback given to us by community members and will continue to do so. Join them by contributing to the SDK or by contributing to the documentation.

## Automated testing
At the moment we do not have high test-coverage. You're free to make a PR to add tests! To run the tests:
```bash
make test
```

# Community

## Slack
Slack is our main feedback channel for the SDK and documentation. Join our [Slack channel](https://ing-bankingofthings.slack.com/join/shared_invite/enQtNDEyODg3MDE1NDg4LWJhNGFiOTFhZmVlNGQwMTM4ZjQzNmZmZDk5ZGZiNjNlZTVjZjNmYjE0Y2MxZjU5MWQxNmY5MTgzYzAxNmFiNGU) and be part of the FINN community.<br/>

## Meetups
We also organize meetups, e.g. demo or hands-on workshops. Keep an eye on our meetup group for any events coming up soon. Here you will be able to see the FINN software in action and meet the team.<br/>
[Meetup/Amsterdam-ING-Banking-of-Things](meetup.com/Amsterdam-ING-Banking-of-Things/).
 
# About FINN
After winning the ING Innovation Bootcamp in 2017, FINN is now part of the ING Accelerator Program. Our aim is to become the new Internet of Things (IoT) payment standard that enables service-led business models. FINN offers safe, autonomous transactions for smart devices.
We believe our software offers tremendous business opportunities. However, at heart, we are enthusiasts. Every member of our team has a passion for innovation. That’s why we love working on FINN.
[makethingsfinn.com](makethingsfinn.com)
 
