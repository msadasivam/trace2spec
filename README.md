# trace2spec
Generate Open API Spec from Apigee trace files.

This script helps reverse engineer API calls traced on [Apigee](https://cloud.google.com/apigee) to create an [Open API Spec](https://en.wikipedia.org/wiki/OpenAPI_Specification). OAS is now a widely accepted mechanism to capture RESTful web APIs design and serve as a starting point to create API proxies, API documentation, stubs, testcases, etc. 

Several systems exist today without a well defined spec. Creating a passthrough layer in Apigee allows one to capture traffic and [export as trace files](https://docs.apigee.com/api-platform/debug/using-offline-trace-tool). These trace files can then be fed to this tool to create OAS.  The generated specs are only a best effort attempt, they require some cleanup to update business context in description. Further work may be needed to clean and consolidate schema reused in multiple resources. 
 
The tool supports the following features:
 * Hosts
 * REST resource paths
 * Query parameters
 * Headers
 * Request payload JSON schema
 * Success and error response codes
 * Response payload JSON schema
 * Multiple trace file support
 
More features being considered are as follows:
 * Resource path params
 * Security schemes
 * Non-JSON content types

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
