from urllib2 import urlopen
import json
from optparse import OptionParser

# Get API Key and Build URL String
apikey = open('apikey.txt', 'r').read()

# Add Option Parser
parser = OptionParser()
parser.add_option("-f", "--from", dest="fromDate", help="harvest records from this date yyyy-mm-dd")
parser.add_option("-g", "--guides", dest="guideType", help="comma separated list with 1 for General, 2 for Course, 3 for Subject, 4 for Topic, 5 for Internal, and 6 for Template")
parser.add_option("-s", "--status", dest="status", help="comma delimited list with 0 for Unpublished, 1 for Published, 2 for Private, and 3 for Submit for Review")

(options, args) = parser.parse_args()

if options:
	guideType = guideStatus = fromDate = ''
	if options.guideType:
		guideType = options.guideType
	if options.fromDate:
		fromDate = options.fromDate
	if options.status:
		guideStatus = options.status

fullURL = 'http://lgapi.libapps.com/1.1/guides/?site_id=681&key=' + apikey.rstrip('\n')

if guideType:
	fullURL += '&guide_types=%s' % guideType
else:
	fullURL += '&guide_types=%s' % '2,3,4'
if fromDate:
	fullURL += '&update_type=since&last_update=%s' % fromDate
if guideStatus:
	fullURL += '&status=%s' % guideStatus
else:
	fullURL += '&status=%s' % '1'

fullURL += '&expand=subjects,owner,tags'

req = urlopen(fullURL).read()
outfile= json.loads(req)
recordCount = 0

for record in outfile:
	if record['description'] != "":
		recordCount += 1
		print 'Creating record ' + record['id'] + ' for research guide: ' + record['name']
		xml = open('temp/' + record['id'] + '.xml', 'w')
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
		if 'tags' in record:
			numOfTags = len(record['tags'])
			for x in range(0,numOfTags):
				xml.write('\t<dc:subject>' + record['tags'][x]['text'] + '</dc:subject>\n')
		xml.write('\t<dc:date>' + record['modified'] + '</dc:date>\n')
		xml.write('\t<dc:publisher>The University of Tennessee Libraries, Knoxville</dc:publisher>\n')
		xml.write('\t<dc:type>text</dc:type>\n')
		xml.write('\t<dc:type>interactive</dc:type>\n')
		xml.write('\t<dc:format>text/HTML</dc:format>\n')
		xml.write('</oai_dc:dc>')
		xml.close()
print "\nCreated %d records\n" % recordCount