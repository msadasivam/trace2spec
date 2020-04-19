from urllib import parse
from xml.etree import ElementTree as ET
from optparse import OptionParser
from genson import SchemaBuilder
import json
import logging

# TODO : path params support, is it even doable

def skippable_req_headers(header):
    return header in {
        "Accept": "",
        "Accept-Encoding": "",
        "Host": "",
        "User-Agent": "",
        "X-Apigee.Message-Timeout": "",
        "X-Forwarded-For": "",
        "X-Forwarded-Port": "",
        "X-Forwarded-Proto": "",
        "Content-Length": "",
        "Content-Type": ""
    }

def usage():
    logging.error("Usage:")
    logging.error("")
    logging.error("trace2spec -f trace-file-1.xml")
    logging.error("trace2spec -f trace-file-1.xml -f trace-file-2.xml")
    logging.error("")
    logging.error("trace2spec -j json-file-1.json")
    logging.error("trace2spec -j json-file-1.json -j json-file-2.json")
    logging.error("trace2spec -j json-file-1.json -s schema-file.json")
    logging.error("")

def cli_args():
    parser = OptionParser(version="%prog 1.0.0")
    parser.add_option("-f", "--file", action="append", dest="file",
                          default=[], type="string",
                          help="Specify an Apigee trace file")
    parser.add_option("-j", "--json-file", action="append", dest="json_file",
                          default=[], type="string",
                          help="Specify a JSON file")
    parser.add_option("-s", "--schema-file", action="append", dest="schema_file",
                          default=[], type="string",
                          help="Specify a Schema file")
    parser.add_option("-X", "--verbose", action="store_true", dest="verbose",
                          default="", 
                          help="debug dump")
    options, args = parser.parse_args()

    if options.verbose: 
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
        logging.info("Verbose mode")
    else:
        logging.basicConfig(format="%(levelname)s: %(message)s")

    return options

def url_parse(url):
    url_components = parse.urlsplit(url)
    url_query = url_components.query

    logging.debug("scheme %s", url_components.scheme)
    logging.debug("netloc %s", url_components.netloc)
    logging.debug("path %s", url_components.path)
    logging.debug("query str %s", url_components.query)
    logging.debug("fragment %s", url_components.fragment)
    logging.debug("hostname %s", url_components.hostname)
    logging.debug("port %s", url_components.port)
    return url_components

def query_params_parse(query_str):
    query_string = parse.parse_qs(query_str)
    logging.debug("query %s", query_string)
    return query_string

def trace_file_parse(trace_file, api_calls):
    logging.debug('Processing ====> %s', trace_file)
    tree = ET.parse(trace_file)
    root = tree.getroot()

    # Intermediate data structure, after parsing XML file
    #    [
    #         { 
    #                 "request": {
    #                     "headers": { },
    #                     "query": { },
    #                     "path": "",
    #                     "verb": "",
    #                     "content": ""
    #                 },
    #                 "respone": {
    #                     "status_code": "",
    #                     "reason_phrase": "",
    #                     "headers": { },
    #                     "content": ""
    #                 }
    #         }
    #    ] ...

    # XML structure - DebugSession/Messages/Message/Data/Point/RequestMessage]
    for root_elem in root.findall('./Messages/Message'):
        req_resp = {}
        # logging.debug("----------------------------------------------------")
        logging.debug("msgid %s", root_elem.find('DebugId').text)
        # logging.debug("----------------------------------------------------")
        for data_point_elem in root_elem.findall('./Data/Point[@id=\'StateChange\']'):
            phase = data_point_elem.find('./DebugInfo/Properties/Property[@name=\'To\']').text

            # request
            if phase == 'REQ_HEADERS_PARSED':
                logging.debug('phase %s', phase)
                req_data = data_point_elem.find('./RequestMessage')
                verb = req_data.find('Verb').text
                url = req_data.find('URI').text

                logging.debug("%s | %s" % (verb, url))
                headers = {}
                for header in req_data.findall('./Headers/Header'):
                    header_value = header.text
                    header_name = header.attrib["name"]
                    logging.debug('header %s %s', header_name, header_value)
                    headers[header_name] = header_value
                url_components = url_parse(url)
                query_params = query_params_parse(url_components.query)
                req_resp["request"] = {
                    "path": url_components.path,
                    "query": query_params,
                    "verb": verb,
                    "headers": headers 
                }

            # request payload
            if phase == 'PROXY_REQ_FLOW':
                logging.debug('phase %s', phase)
                req_data = data_point_elem.find('./RequestMessage')
                node = req_data.find('Content')
                if node is not None: 
                    payload = node.text
                    logging.debug('payload length %s', len(payload))
                    req_resp["request"]["content"] = payload

            # response
            if phase == 'RESP_SENT':
                logging.debug('phase %s', phase)
                res_data = data_point_elem.find('./ResponseMessage')
                for header in res_data.findall('./Headers/Header'):
                    header_value = header.text
                    header_name = header.attrib["name"]
                    logging.debug('header %s %s', header_name, header_value)

                status_code = res_data.find('StatusCode').text
                reason_phrase = res_data.find('ReasonPhrase').text
                node = res_data.find('Content')
                if node is not None:
                    resp_content = node.text
                else:
                    resp_content = ""

                req_resp["response"] = {
                    "status_code": status_code,
                    "reason_phrase": reason_phrase,
                    "headers": headers,
                    "content": resp_content
                }

                logging.debug('status_code %s', status_code)
                logging.debug('reason_phrase %s', reason_phrase)
                logging.debug('resp_content %s', resp_content)
        api_calls.append(req_resp)
    return api_calls

# gather hosts from all calls
def find_hosts(api_calls):
    hosts = {}
    for api_call in api_calls:
        host_value = api_call["request"]["headers"]["Host"]
        hosts[host_value] = "";
    logging.debug('all_hosts %s', list(hosts.keys()))
    return list(hosts.keys())[0]

def find_schemes(api_calls):
    return ["https"]

def json2schema(seed, payload):
    # can return None
    logging.debug("seed schema %s resp payload %s", seed, payload)
    builder = SchemaBuilder(schema_uri=None)
    if seed:
        builder.add_schema(seed)

    if payload.endswith('.....'):
        logging.warn('skipping truncated payload')
        return None

    payload_dict = None
    try:
        payload_dict = json.loads(payload)
    except ValueError as e:
        logging.warn('skipping unrecognized payload')
        return None

    builder.add_object(payload_dict)
    schema = builder.to_schema()
    logging.debug('schema updated %s', schema)
    return schema

def spec20_format_request_payload(spec_operation, request_payload):
    spec_params = spec_operation.get("parameters", [])

    if not request_payload:
        return spec_params

    existing_schema = None
    existing_body_param = None
    for param in spec_params:
        if param['in'] == 'body':
            existing_schema = param["schema"]
            existing_body_param = param
            break

    new_schema = json2schema(existing_schema, request_payload)
    if not new_schema:
        return spec_params

    if existing_body_param:
        existing_body_param["schema"] = new_schema
    else:
        spec_params.append({
            "in": "body",
            "name": "body",
            "description": "",
            "schema": new_schema
        })
    return spec_params

def spec20_format_response(spec_response, response_payload):
    if "schema" in spec_response:
        existing_schema = spec_response["schema"]
    else:
        existing_schema = None
    return json2schema(existing_schema, response_payload)

def spec20_format_headers(spec_operation, api_call):
    spec_params = spec_operation.get("parameters", [])
    for header_name in api_call["request"]["headers"].keys():
        if skippable_req_headers(header_name):
            continue

        if any(param['name'] == header_name and
                param['in'] == 'header' for param in spec_params):
            continue

        spec_params.append({
                "name": header_name,
                "in": "header",
                "description": "",
                "type": "string"
            }
        )
    return spec_params

def spec20_format_qparams(spec_operation, api_call):
    spec_params = spec_operation.get("parameters", [])

    # Note: param_value is a list, hence keys()
    # 'query': {'errorcode': ['401']}
    for param_name in api_call["request"]["query"].keys():
        if any(param['name'] == param_name and
                param['in'] == 'query' for param in spec_params):
            continue

        spec_params.append({
                "name": param_name,
                "in": "query",
                "description": "",
                "type": "string"
            }
        )
    return spec_params

def spec20_format_calls(api_calls):
    rest_resources = {}
    rest_resources["host"] = find_hosts(api_calls)
    rest_resources["schemes"] = find_schemes(api_calls)
    rest_resources["paths"] = {}

    for api_call in api_calls:
        path = api_call["request"]["path"]
        verb = api_call["request"]["verb"].lower()
        response_code = api_call["response"]["status_code"]

        if response_code == 404: continue

        if path not in rest_resources["paths"]:
            rest_resources["paths"][path] = {}

        if verb not in rest_resources["paths"][path]:
            logging.debug('adding verb %s', verb)
            rest_resources["paths"][path][verb] = {
                "summary": "",
                "description": "",
                "operationId": (verb + path).lower().replace('/','_'),
                "responses": {}
            }

        spec_operation = rest_resources["paths"][path][verb]
        # query params
        spec_operation["parameters"] = spec20_format_qparams(spec_operation, api_call)
        # headers
        spec_operation["parameters"] = spec20_format_headers(spec_operation, api_call)
        # request payload
        if not "content" in api_call["request"]:
            request_payload = None
        else:    
            request_payload = api_call["request"]["content"]
        spec_operation["parameters"] = spec20_format_request_payload(spec_operation, request_payload)

        logging.debug('request_content %s', request_payload)

        # response code
        logging.debug('response code found %s', response_code)
        spec_responses = spec_operation["responses"]
        if response_code not in spec_responses:
            spec_responses[response_code] = {
                "description": api_call["response"]["reason_phrase"]
            }

        # response payload
        if not "content" in api_call["response"]:
            continue

        response_payload = api_call["response"]["content"]
        spec_response = spec_responses[response_code]
        updated_schema = spec20_format_response(spec_response, response_payload)
        if updated_schema: spec_response["schema"] = updated_schema
    return rest_resources

def spec20_defaults():
    return {
        "swagger": "2.0",
        "info": {
            "description": "This is an auto-generated spec from Apigee offline trace",
            "version": "1.0.0",
            "title": "Auto generated spec",
            "termsOfService": "",
            "contact": {
                "email": "apiteam@apigee.io"
            },
            "license": {
                "name": "Apache 2.0",
                "url": "http://www.apache.org/licenses/LICENSE-2.0.html"
            }
         },
        "tags": [
        ],
        "basePath": "/",
    }

def spec20_assemble(spec_resources):
    dict_spec = {}
    dict_spec.update(spec20_defaults())
    dict_spec.update(spec_resources)
    return dict_spec

def write_json_spec(dict_spec):
    return json.dumps(dict_spec, indent=4, sort_keys=False)

def tracefile2spec(trace_files):
    logging.debug("tracefile2spec %s", trace_files)
    api_calls = []
    for trace_file in trace_files:
        trace_file_parse(trace_file, api_calls)

    logging.debug("--------------------- generating spec ---------------------")
    spec_resources = spec20_format_calls(api_calls)
    dict_spec = spec20_assemble(spec_resources)
    json_spec = write_json_spec(dict_spec)
    print(json_spec)

def jsonfile2schema(json_files):
    logging.debug("jsonfile2schema %s", json_files)
    return

def main():
    options = cli_args()

    if options.file:
        tracefile2spec(options.file)
        return

    if options.json_file:        
        jsonfile2schema(options.json_file)
        return

    usage()

main()
