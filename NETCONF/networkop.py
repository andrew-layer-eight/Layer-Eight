from ncclient import manager

m = manager.connect(host='ios-xe-mgmt.cisco.com', port=10000, username='developer', password='C1sco12345', device_params={'name': 'iosxe'})

print (m.server_capabilities)

schema = m.get_schema('ietf-ip')
#print (schema)

import xml.etree.ElementTree as ET
root = ET.fromstring(schema.xml)
yang_text = list(root)[0].text
write_file('ietf-ip.yang', yang_text)