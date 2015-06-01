from urllib2 import urlopen
import json

# Get API Key and Build URL String
f = open('apikey.txt', 'r')
apikey = f.read()
fullURL = apikey.rstrip('\n') + '&guide_types=2,3,4&status=1&expand=subjects,owner'

req = urlopen(fullURL).read()
outfile= json.loads(req)

for record in outfile:
	if record['description'] != "":
		print 'Creating record ' + record['id'] + ' for research guide: ' + record['name']
		xml = open('temp/' + record['id'] + '.xml'.format(record['id']), 'w')
		xml.write('<?xml version="1.0" encoding="UTF-8"?>\n')
		xml.write('<oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd">\n')
		xml.write('\t<dc:title>' + record['name'] + '</dc:title>\n')
		if record['friendly_url'] is None:
			xml.write('\t<dc:identifier>' + record['url'] + '</dc:identifier>\n')
		else:
			xml.write('\t<dc:identifier>' + record['friendly_url'] + '</dc:identifier>\n')
		xml.write('\t<dc:description>' + record['description'] + '</dc:description>\n')
		xml.write('\t<dc:creator>' + record['owner']['first_name'] + " " + record['owner']['last_name'] + '</dc:creator>\n')
		if 'subjects' in record:
			numOfSubs = len(record['subjects'])
			for x in range(0,numOfSubs):
				xml.write('\t<dc:subject>' + record['subjects'][x]['name'] + '</dc:subject>\n')
		xml.write('\t<dc:date>' + record['modified'] + '</dc:date>\n')
		xml.write('\t<dc:publisher>The University of Tennessee Libraries, Knoxville</dc:publisher>\n')
		xml.write('\t<dc:type>text</dc:type>\n')
		xml.write('\t<dc:type>interactive</dc:type>\n')
		xml.write('\t<dc:format>text/HTML</dc:format>\n')
		xml.write('</oai_dc:dc>')
		xml.close()