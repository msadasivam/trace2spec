# trace2spec
Generate Open API Spec from Apigee trace file

Works with API calls traced in any order including calls returning error. Supports the following 
 * REST resource paths
 * Query parameters
 * Headers
 * Response codes
 * Response payload schema
 * Hosts
 * Multiple trace file support
 
More to come
 * Request payload to schema

## Usage
```
    python3 trace2spec.py -f <apigee-trace-file.xml> 

        -f apigee trace file
        -X verbose mode


    Multiple trace files
    --------------------
    python3 trace2spec.py -f <apigee-trace-file.xml> -f <apigee-trace-file-2.xml> ...
```

## Apigee offline trace
Learn here to extract offline trace from Apigee
https://docs.apigee.com/api-platform/debug/using-offline-trace-tool

![Trace Download](https://docs.apigee.com/api-platform/images/download-trace-button-full.png "How to download offline trace file")

## Support
Please raise an issue.

## Contributing
Please send a pull request.
