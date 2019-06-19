#！/usr/bin/env python
#_*_coding:utf-8_*_

from xml.etree import ElementTree as et;
import re

namespace = {'wsdl': 'http://schemas.xmlsoap.org/wsdl/', 'soap': 'http://schemas.xmlsoap.org/wsdl/soap/'}
regex = re.compile(':[0-9]+')

def XMLToJSON(xmlFile):
    root = et.parse(xmlFile)
    node_root = root.getroot()
    service_node = node_root.find('wsdl:service', namespace);
    port_node = service_node.find('wsdl:port', namespace)
    address_ode = port_node.find('soap:address', namespace)

    location = address_ode.get('location')
    location_span = regex.search(location).span()
    ret_map = {
        "portName": port_node.get('name'),
        "location": address_ode.get('location'),
        "path": location[location_span[1]:]
    }
    return ret_map;
