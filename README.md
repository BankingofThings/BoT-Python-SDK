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
### Installing Hatch

First things first, make sure you have python 3.5+ and [Install Hatch](https://pypi.org/project/hatch/).

### Creating the virtual environment
```bash
hatch env BoT-Python-SDK
hatch shell BoT-Python-SDK
```

### Installing dependencies
```bash 
make install
```

## Configuration

### First run
Get your makerID from your BoT Account and run the server in your virtual environment in the root of the SDK:

```bash
make server makerID=YOUR_MAKER_ID
```

replacing `YOUR_MAKER_ID` with your own BoT makerID.

To run the server normally after you've configured it, simply run in your venv:
```bash
make server
```

## Using the SDK

### Retrieving actions
```bash
GET /actions
```

### Triggering actions
```bash
POST /
body: {
  "actionID": YOUR_ACTION_ID,
  "value": OPTIONAL_VALUE
}
```

## Troubleshooting

If you've paired your device with the QR code that was generated in the root (`qr.png`), it might not have been activated.

Run the next command in your venv to start the activation process:
```bash
make activate
``` 

Please refer to the complete [Documentation](https://docs.bankingofthings.io)
