# Tests

 * Import proxy 
 * Turn on tracing
 * Run following commands to get a usable trace file for the tool
```
curl -X GET    'https://madhans-trial-test.apigee.net/helloworld/greetings' 
curl -X DELETE 'https://madhans-trial-test.apigee.net/helloworld/greetings' 
curl -X PUT    'https://madhans-trial-test.apigee.net/helloworld/greetings' -H 'Content-Type: application/json' -d '{"balance": "45.23"}' 
curl -X POST   'https://madhans-trial-test.apigee.net/helloworld/greetings' -H 'Content-Type: application/json' -d '{"balance": "45.23"}' 
curl -X PATCH  'https://madhans-trial-test.apigee.net/helloworld/greetings' -H 'Content-Type: application/json' -d '{"balance": "45.23"}'
curl -X GET    'https://madhans-trial-test.apigee.net/helloworld/greetings?errorcode=500'
curl -X DELETE 'https://madhans-trial-test.apigee.net/helloworld/greetings?errorcode=500' 
curl -X PUT    'https://madhans-trial-test.apigee.net/helloworld/greetings?errorcode=500' -H 'Content-Type: application/json' -d '{"balance": "45.23"}' 
curl -X POST   'https://madhans-trial-test.apigee.net/helloworld/greetings?errorcode=500' -H 'Content-Type: application/json' -d '{"balance": "45.23"}' 
curl -X PATCH  'https://madhans-trial-test.apigee.net/helloworld/greetings?errorcode=500' -H 'Content-Type: application/json' -d '{"balance": "45.23"}'
curl -X GET    'https://madhans-trial-test.apigee.net/helloworld/greetings?errorcode=400'
curl -X DELETE 'https://madhans-trial-test.apigee.net/helloworld/greetings?errorcode=400' 
curl -X PUT    'https://madhans-trial-test.apigee.net/helloworld/greetings?errorcode=400' -H 'Content-Type: application/json' -d '{"balance": "45.23"}' 
curl -X POST   'https://madhans-trial-test.apigee.net/helloworld/greetings?errorcode=400' -H 'Content-Type: application/json' -d '{"balance": "45.23"}' 
curl -X PATCH  'https://madhans-trial-test.apigee.net/helloworld/greetings?errorcode=400' -H 'Content-Type: application/json' -d '{"balance": "45.23"}'
curl -X GET    'https://madhans-trial-test.apigee.net/helloworld/greetings?errorcode=401'
curl -X DELETE 'https://madhans-trial-test.apigee.net/helloworld/greetings?errorcode=401' 
curl -X PUT    'https://madhans-trial-test.apigee.net/helloworld/greetings?errorcode=401' -H 'Content-Type: application/json' -d '{"balance": "45.23"}' 
curl -X POST   'https://madhans-trial-test.apigee.net/helloworld/greetings?errorcode=401' -H 'Content-Type: application/json' -d '{"balance": "45.23"}' 
curl -X PATCH  'https://madhans-trial-test.apigee.net/helloworld/greetings?errorcode=401' -H 'Content-Type: application/json' -d '{"balance": "45.23"}'
curl -X GET    'https://madhans-trial-test.apigee.net/helloworld/greetings?errorcode=403'
curl -X DELETE 'https://madhans-trial-test.apigee.net/helloworld/greetings?errorcode=403' 
curl -X PUT    'https://madhans-trial-test.apigee.net/helloworld/greetings?errorcode=403' -H 'Content-Type: application/json' -d '{"balance": "45.23"}' 
curl -X POST   'https://madhans-trial-test.apigee.net/helloworld/greetings?errorcode=403' -H 'Content-Type: application/json' -d '{"balance": "45.23"}' 
curl -X PATCH  'https://madhans-trial-test.apigee.net/helloworld/greetings?errorcode=403' -H 'Content-Type: application/json' -d '{"balance": "45.23"}'
```