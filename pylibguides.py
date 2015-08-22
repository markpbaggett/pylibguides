from urllib2 import urlopen
import json
import argparse

# Get API Key and Build URL String
apikey = open('apikey.txt', 'r').read()

# Add Argparse
parser = argparse.ArgumentParser(description='Use LibGuides API to create DC records for Content')
parser.add_argument("-f", "--fromDate", dest="fromDate", help="harvest records from this date yyyy-mm-dd")
parser.add_argument("-g", "--guides", dest="guideType", help="comma separated list with 1 for General, 2 for Course, 3 for Subject, 4 for Topic, 5 for Internal, and 6 for Template")
parser.add_argument("-s", "--status", dest="status", help="comma delimited list with 0 for Unpublished, 1 for Published, 2 for Private, and 3 for Submit for Review")
args = parser.parse_args()

fullURL = 'http://lgapi.libapps.com/1.1/guides/?site_id=681&key=' + apikey.rstrip('\n')

if args.guideType:
	fullURL += "&guide_types={0}".format(args.guideType)
else:
	fullURL += "&guide_types=2,3,4"
if args.fromDate:
	fullURL += "&update_type=since&last_update={0}".format(args.fromDate)
if args.status:
	fullURL += "&status={0}".format(args.status)
else:
	fullURL += "&status=1"

fullURL += "&expand=subjects,owner,tags"

req = urlopen(fullURL).read()
outfile= json.loads(req)
recordCount = 0

for record in outfile:
	if record['description'] != "":
		recordCount += 1
		print "Creating record {0} for research guide: {1}".format(record['id'], record['name'])
		xml = open("temp/{0}.xml".format(record['id']), 'w')
		xml.write('<?xml version="1.0" encoding="UTF-8"?>\n')
		xml.write('<oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd">\n')
		xml.write('\t<dc:title>{0}</dc:title>\n'.format(record['name']))
		if record['friendly_url'] is None:
			xml.write('\t<dc:identifier>{0}</dc:identifier>\n'.format(record['url']))
		else:
			xml.write('\t<dc:identifier>{0}</dc:identifier>\n'.format(record['friendly_url']))
		xml.write('\t<dc:description>{0}</dc:description>\n'.format(record['description']))
		xml.write('\t<dc:creator>{0} {1}</dc:creator>\n'.format(record['owner']['first_name'], record['owner']['last_name']))
		if 'subjects' in record:
			numOfSubs = len(record['subjects'])
			for x in range(0,numOfSubs):
				xml.write('\t<dc:subject>{0}</dc:subject>\n'.format(record['subjects'][x]['name']))
		if 'tags' in record:
			numOfTags = len(record['tags'])
			for x in range(0,numOfTags):
				xml.write('\t<dc:subject>{0}</dc:subject>\n'.format(record['tags'][x]['text']))
		xml.write('\t<dc:date>{0}</dc:date>\n'.format(record['modified']))
		xml.write('\t<dc:publisher>The University of Tennessee Libraries, Knoxville</dc:publisher>\n')
		xml.write('\t<dc:type>text</dc:type>\n')
		xml.write('\t<dc:type>interactive</dc:type>\n')
		xml.write('\t<dc:format>text/HTML</dc:format>\n')
		xml.write('</oai_dc:dc>')
		xml.close()
print "\nCreated %d records\n" % recordCount