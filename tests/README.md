# Tests

 * Import proxy 
 * Turn on tracing
 * Run following commands to get a usable trace file for the tool
```
curl -X GET    'https://madhans-trial-test.apigee.net/helloworld/greetings' 
curl -X DELETE 'https://madhans-trial-test.apigee.net/helloworld/greetings' 
curl -X PUT    'https://madhans-trial-test.apigee.net/helloworld/greetings' -H 'Content-Type: application/json' -d '{"balance": "45.23"}' 
curl -X POST   'https://madhans-trial-test.apigee.net/helloworld/greetings' -H 'Content-Type: application/json' -d '{"balance": "45.23"}' 
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

curl -X POST   'https://madhans-trial-test.apigee.net/helloworld/greetings' -H 'Content-Type: application/json' -d '[
  {
    "age": 33
  }
]'
curl -X POST   'https://madhans-trial-test.apigee.net/helloworld/greetings' -H 'Content-Type: application/json' -d '[
  {
    "eye": "green"
  }
]'
curl -X POST   'https://madhans-trial-test.apigee.net/helloworld/greetings' -H 'Content-Type: application/json' -d '[
  {
    "_id": "5e586c56cc99e2c73312cad6",
    "index": 0,
    "guid": "1c6a74fc-5d5f-41ec-8ac1-c9f00dcb3e53",
    "isActive": false,
    "balance": "$2,516.01",
    "picture": "http://placehold.it/32x32",
    "age": 33,
    "eyeColor": "green",
    "name": "Cathryn Patton",
    "gender": "female",
    "company": "ANIXANG",
    "email": "cathrynpatton@anixang.com",
    "phone": "+1 (814) 488-3296",
    "address": "107 Conover Street, Kingstowne, Colorado, 8015",
    "about": "Excepteur sint ad pariatur ut mollit dolore pariatur dolore tempor sit magna. Amet duis dolore do id esse aute cillum qui elit incididunt irure. Excepteur est consequat ut adipisicing amet esse et. Duis do amet minim ullamco sunt ea officia dolor nisi cillum mollit aute cillum. Magna veniam qui laboris officia duis velit.\r\n",
    "registered": "2016-10-03T06:59:39 -11:00",
    "latitude": -48.850479,
    "longitude": -53.658898,
    "tags": [ "eiusmod", "aliquip", "Lorem", "cillum", "ut", "Lorem", "veniam" ],
    "friends": [
      {
        "id": 0,
        "name": "Winnie Schultz"
      },
      {
        "id": 1,
        "name": "Small Sanford"
      },
      {
        "id": 2,
        "name": "Mccoy White"
      }
    ],
    "greeting": "Hello, Cathryn Patton! You have 9 unread messages.",
    "favoriteFruit": "banana"
  }
]'
```
