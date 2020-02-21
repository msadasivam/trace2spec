# trace2spec
Generate Open API Spec from Apigee trace file

Works with API calls traced in any order including calls returning error. Supports the following 
 * REST resource paths
 * Query parameters
 * Headers
 * Response codes
 * Hosts

More to come
 * Multiple trace file support
 * Payload to schema

## Usage
```
    python3 trace2spec.py -f <apigee-trace-file.xml>

      -f apigee trace file
      -X verbose mode
```

## Apigee offline trace
Learn here to extract offline trace from Apigee
https://docs.apigee.com/api-platform/debug/using-offline-trace-tool

![Trace Download](https://docs.apigee.com/api-platform/images/download-trace-button-full.png "How to download offline trace file")

## JSON to schema
For JSON payload to schema generation use the following tool. Hoping to incorporate it into trace2spec for processing payload.
https://pypi.org/project/genson/

## Support
Please raise an issue.

## Contributing
Please send a pull request.
