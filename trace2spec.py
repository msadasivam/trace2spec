from urllib import parse
from xml.etree import ElementTree as ET
from optparse import OptionParser
import json
import logging

# TODO : path params support
# TODO : req payload support
# TODO : resp payload support

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

def cli_args():
	parser = OptionParser(version="%prog 0.5")
	parser.add_option("-f", "--file", action="store", dest="file",
	                      default="", type="string",
	                      help="Specify an Apigee trace file")
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
	logging.debug("query st%sr ", url_components.query)
	logging.debug("fragment %s", url_components.fragment)
	logging.debug("hostname %s", url_components.hostname)
	logging.debug("port %s", url_components.port)
	return url_components

def query_params_parse(query_str):
	query_string = parse.parse_qs(query_str)
	logging.debug("query %s", query_string)
	return query_string

def trace_file_parse(trace_file):
	tree = ET.parse(trace_file)
	root = tree.getroot()

	# Intermediate data structure, after parsing XML file
	#	[
	#		 { 
	#		 		"request": {
	#		 			"headers": { },
	#		 			"query": { },
	#		 			"path": "",
	#		 			"verb": "",
	#		 			"content": ""
	#		 		},
	#		 		"respone": {
	#		 			"status_code": "",
	#		 			"reason_phrase": "",
	#		 			"headers": { },
	#		 			"content": ""
	#		 		}
	#		 }
	#	] ...

	api_calls = []

	# XML structure - DebugSession/Messages/Message/Data/Point/RequestMessage]
	for root_elem in root.findall('./Messages/Message'):
		req_resp = {}
		logging.debug("----------------------------------------------------")
		logging.debug(root_elem.find('DebugId').text)
		logging.debug("----------------------------------------------------")
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
				if req_data.find('Content'): 
					payload = req_data.find('Content').text
					if payload:
						logging.debug('payload length %n', len(payload))
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
				resp_content = res_data.find('Content').text

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

		if (path in rest_resources["paths"] and
		 	verb in rest_resources["paths"][path] and
		  	response_code in rest_resources["paths"][path][verb]["responses"]):
		   	logging.debug('known path skipping')
		   	continue

		if path not in rest_resources["paths"]:
			rest_resources["paths"][path] = {}

		if verb not in rest_resources["paths"][path]:
			logging.debug('adding verb %s', verb)

			# query params
			spec_params = []
			for param_name, param_value in api_call["request"]["query"].items():
				spec_params.append({
                        "name": param_name,
                        "in": "query",
                        "description": "",
                        "type": "string"
					}
				)

			# headers
			for header_name, header_value in api_call["request"]["headers"].items():
				if skippable_req_headers(header_name):
					continue
				spec_params.append({
                        "name": header_name,
                        "in": "header",
                        "description": "",
                        "type": "string"
					}
				)

			rest_resources["paths"][path][verb] = {
                "summary": "",
                "description": "",
                "operationId": (verb + path).lower().replace('/','_'),
                "parameters": spec_params,
                "responses": {}
			}

		# response codes
		if response_code not in rest_resources["paths"][path][verb]["responses"]:
			logging.debug('response code added %n', response_code)
			rest_resources["paths"][path][verb]["responses"] = {
                response_code: {
	                "description": api_call["response"]["reason_phrase"],
	                "schema": {}
                }
			}
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
				"email": "admin@example.io"
			},
			"license": {
				"name": "",
				"url": ""
			}
	 	},
	    "tags": [
	    ],
	    "basePath": "",
	}

def spec20_assemble(spec_resources):
	dict_spec = {}
	dict_spec.update(spec20_defaults())
	dict_spec.update(spec_resources)
	return dict_spec

def write_json_spec(dict_spec):
	return json.dumps(dict_spec, indent=4, sort_keys=False)

options = cli_args()

logging.debug('Processing %s', options.file)
api_calls = trace_file_parse(options.file)

spec_resources = spec20_format_calls(api_calls)
dict_spec = spec20_assemble(spec_resources)
json_spec = write_json_spec(dict_spec)

print(json_spec)
