#!/usr/bin/env bash

curl localhost:3001/pairing # GET /pairing -> return pairing details (e.g. deviceID)

curl localhost:3001/actions # GET /actions -> return actions that the device could trigger

# POST /actions -> Trigger an action
curl -d '{"actionID":"YOUR_ACTION_ID"}' -H "Content-Type: application/json" -X POST http://localhost:3001/actions
