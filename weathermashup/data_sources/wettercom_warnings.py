"""
Example response:
{
  "warnings":[
    {
      "valid_from": "2011-06-04 16:35:00",
      "valid_to": "2011-06-04 20:00:00",
      "region_id": "09471",
      "region_name": "Kreis und Stadt Bamberg",
      "headline": "Amtliche WARNUNG vor GEWITTER mit STURMB\u00d6EN, STARKREGEN und HAGEL<br \/>\r",
      "content": "..."
    }
  ]
}

This API is valid only for Germany.

"""

import lxml.etree
from datetime import datetime
import urllib
import simplejson

def source(location):
    query = urllib.urlencode(dict(query="select ?code { "
            "<http://de.dbpedia.org/resource/%s> "
            "<http://dbpedia.org/ontology/vehicleCode> ?code . }"
            % (location,)))
    code = lxml.etree.parse("http://de.dbpedia.org/sparql?%s"
            % (query,)).find(
            "//{http://www.w3.org/2005/sparql-results#}literal").text
    print code
    # country code is silently ignored by the API
    url = ("http://www.wetter.com"
           "/svc/ajax/?ajax=warning_json&s_path=%s&country=DE&group=1"
           % (code,))
    info = simplejson.loads(urllib.urlopen(url).read())
    warnings = info.get('warnings', ())
    for warning in warnings:
        headline = warning['headline'][:-len("<br />\r")]
        yield dict(
            time_from = datetime.strptime(warning['valid_from'], '%Y-%m-%d %H:%M:%S'),
            time_to = datetime.strptime(warning['valid_to'], '%Y-%m-%d %H:%M:%S'),
            warnings = [headline],
        )
