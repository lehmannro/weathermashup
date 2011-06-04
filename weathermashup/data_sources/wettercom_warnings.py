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

def source(location):
    code = "B"
    # country code is silently ignored by the API
    url = ("http://www.wetter.com"
           "/svc/ajax/?ajax=warning_json&s_path=%s&country=DE&group=1"
           % (code,))
    info = lxml.etree.parse(url)
    warnings = info.get('warnings', ())
    for warning in warnings:
        yield dict(
            time_from = datetime.strptime(warning['valid_from'], '%Y-%m-%d %H:%M:%S'),
            time_to = datetime.strptime(warning['valid_to'], '%Y-%m-%d %H:%M:%S'),
            warnings = [headline],
        )
