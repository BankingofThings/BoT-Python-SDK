#!/usr/bin/env bash

curl localhost:3001/pairing

curl localhost:3001/actions

curl -d '{"actionID":"YOUR_ACTION_ID"}' -H "Content-Type: application/json" -X POST http://localhost:3001/
