# Banking of Things IoT Python SDK

IoT BoT SDK for Python


## System Requirements

The SDK depends on the following system libraries:

* libssl-dev

```sh
apt-get install libssl-dev
```

## Installation

Install using `pip`:

```sh 
pip install botiotsdk
```

## Configuration

Register as a maker account to get your makerID at [BankingofThings.io](https://bankingofthings.io).

```python
import botiotsdk
botiotsdk.configure({
    "mode": "sandbox", # sandbox or live
    "makerID": "YOUR-MAKER-ID"
})
```

## Tests

```sh 
make tests
```
