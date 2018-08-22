<img src="https://bankingofthings.io/img/github-header.png" style="margin:auto" alt="BoT">

# BoT-Python-SDK

[![Build Status](https://travis-ci.com/BankingofThings/BoT-Python-SDK.svg?token=ic37boNh1zbtjppb1zLc&branch=master)](https://travis-ci.com/BankingofThings/BoT-Python-SDK)

[comment]: # (Todo replace build status with open source one)

This is our Banking of Things SDK that enables your IoT devices to perform seamless autonomous payments.

## Installation
Clone the repository on your device, for example with ssh:
```bash
git clone git@github.com:BankingofThings/BoT-Python-SDK.git
```

### Install using a virtual environment
First we install `virtualenv` && create an environment `venv` with:
```bash
make environment
```
Then we run our newly created environment like this:
```bash
source venv/bin/activate
```

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

## Using the SDK
### Pairing your device
```bash
curl localhost:3001/pairing
```

### Retrieving actions
```bash
curl localhost:3001/actions
```

### Triggering actions
```bash
curl -d '{"actionID":"YOUR_ACTION_ID"}' -H "Content-Type: application/json" -X POST http://localhost:3001/
```

## Troubleshooting
If you've paired your device with the QR code that was generated in the root (`qr.png`), it might not have been activated.

Run the next command in your venv to start the activation process:
```bash
make activate
``` 

Please refer to the complete [Banking of Things Documentation](https://docs.bankingofthings.io) for more information.
