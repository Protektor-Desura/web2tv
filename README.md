# web2tv
This project contains python and perl scripts which load and parse streaming TV information from the web and return the information in [xml format](http://wiki.xmltv.org/index.php/XMLTVFormat) for TV guide information and [m3u format](https://en.wikipedia.org/wiki/M3U) for TV channel lists. You can then use the xml and m3u in various other programs such as [xTeVe](https://github.com/xteve-project/xTeVe) or other iptv clients.

Additionally there are some helper scripts as well. All scripts were tested using Python 3.8
________________
*[EPG Generation](https://en.wikipedia.org/wiki/Electronic_program_guide)*
- [plex.tv](https://watch.plex.tv/) (plextv.py)
- [pluto.tv](https://pluto.tv/) (plutotv.py)
- [schedulesdirect.org](https://schedulesdirect.org/) (schedules_direct.py)
- [ustvgo.tv](https://ustvgo.tv/) (ustvgo.py)
- [zap2it.com](https://tvlistings.zap2it.com/) (zap2xml.py)
________________
*[M3U Generation](https://en.wikipedia.org/wiki/M3U)*
- [plex.tv](https://watch.plex.tv/) (plextv.py)
- [pluto.tv](https://pluto.tv/) (plutotv.py)
- [ustvgo.tv](https://ustvgo.tv/) (ustvgo.py)
- [ustvgo.tv](https://ustvgo.tv/) (ustvgo_m3ugrabber.py)
________________
*Helper Scripts*
- m3u_modder (m3u_modder.py) (convert m3u for use with [Streamlink](https://github.com/streamlink/streamlink))
- nextpvr (nextpvr.py) (convert Pluto TV channels into m3u format for use with [NextPVR](https://www.nextpvr.com/))
________________

# m3u_modder
Python script to convert m3u for use with streamlink.

### m3u arguments
'-i', '--inFile', type=str, nargs=1, required=False, default=['streamlink.m3u'], help='Full input file filepath. Full file path can be specified. If only file name is specified then file will be used from the current working directory if it exists.'
    
'-o', '--outFile', type=str, nargs=1, required=False, default=['streamlink.m3u'], help='Full destination filepath. Full file path can be specified. If only file name is specified then file will be placed in the current working directory.'

'-p', '--protocol', type=str, nargs=1, required=False, default=['httpstream://'], help='Stream url protocol.'


# nextpvr
Python script to convert pluto tv channels into m3u format.

### m3u arguments
-f', '--file', type=str, nargs=1, required=False, default=['nextpvr.m3u'], help='Full destination filepath. Default is nextpvr.m3u. Full file path can be specified. If only file name is specified then file will be placed in the current working directory.'

'-p', '--prefix', type=str, nargs=1, required=False, default=[''], help='Channel name prefix.'

'-s', '--startNumber', type=int, nargs=1, required=False, default=[1], help='Start numbering here. For example 9000. If -k, --keepNumber is used then channel 2 would become channel 9002, otherwise the first channel number found would be 9000, second channel found would be 9001, etc.'

'-k', '--keepNumber', action='store_true', required=False, help='Keep existing number scheme. Script will add existing number to start number. Recommended start number ends with a 0.'

'-i', '--ip', type=str, nargs=1, required=False, default=['127.0.0.1'], help='IP Address of NextPVR server. Default is 127.0.0.1'

'--port', type=int, nargs=1, required=False, default=[8866], help='Port number of NextPVR server. Default is 8866.'

'--pin', type=str, nargs=1, required=False, default=['0000'], help='Pin used to access NextPVR api. Default is 0000.'

'--streamlink', action='store_true', required=False, help='Generate the stream urls for use with Streamlink.'


# plextv
description="Python script to convert plex livetv guide into xml/m3u format."
    
### m3u arguments
'-m', '--m3uFile', type=str, nargs=1, required=False, default=['plex2.m3u'], help='Full destination filepath for m3u. Full file path can be specified. If only file name is specified then file will be placed in the current working directory.'

'--prefix', type=str, nargs=1, required=False, default=[''], help='Channel name prefix.'

'-s', '--startNumber', type=int, nargs=1, required=False, default=[1], help='Start numbering here. For example 9000. If -k, --keepNumber is used then channel 2 would become channel 9002, otherwise the first channel number found would be 9000, second channel found would be 9001, etc.'

'-k', '--keepNumber', action='store_true', required=False, help='Keep existing number scheme. Script will add existing number to start number. Recommended start number ends with a 0.'

'--m3u', action='store_true', required=False, help='Generate the m3u file.'

'--streamlink', action='store_true', required=False, help='Generate the stream urls for use with Streamlink.'

### xml arguments
'-t', '--token', type=str, nargs=1, required=True, help='Token is required. Follow Plex [instructions](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/#toc-0) for finding the token.'

'-d', '--days', type=int, nargs=1, required=False, default=[7], help='Days of info to collect. Max if 21.'

'-p', '--pastdays', type=int, nargs=1, required=False, default=[0], help='Days in past of info to collect. Max is 1.'

'-l', '--language', type=str, nargs=1, required=False, default=['en'], help='Plex language... Get from url same as token.'

'-x', '--xmlFile', type=str, nargs=1, required=False, default=['plex2.xml'], help='Full destination filepath for xml. Full file path can be specified. If only file name is specified then file will be placed in the current working directory.'

'--xml', action='store_true', required=False, help='Generate the xml file.'


# plutotv
Python script to convert pluto tv guide into xml/m3u format.

### m3u arguments
'-m', '--m3uFile', type=str, nargs=1, required=False, default=['plutotv.m3u'], help='Full destination filepath. Full file path can be specified. If only file name is specified then file will be placed in the current working directory.'

'-p', '--prefix', type=str, nargs=1, required=False, default=[''], help='Channel name prefix.'

'-s', '--startNumber', type=int, nargs=1, required=False, default=[1], help='Start numbering here. For example 9000. If -k, --keepNumber is used then channel 2 would become channel 9002, otherwise the first channel number found would be 9000, second channel found would be 9001, etc.'

'-k', '--keepNumber', action='store_true', required=False, help='Keep existing number scheme. Script will add existing number to start number. Recommended start number ends with a 0.'

'--m3u', action='store_true', required=False, help='Generate the m3u file.'

'--streamlink', action='store_true', required=False, help='Generate the stream urls for use with Streamlink.'

### xml arguments
'-e', '--epgHours', type=int, nargs=1, required=False, default=[10], help='Hours of EPG to collect. Pluto.TV only provides a few hours of EPG. Max allowed is 12.'

'-x', '--xmlFile', type=str, nargs=1, required=False, default=['plutotv.xml'], help='Full destination filepath. Full file path can be specified. If only file name is specified then file will be placed in the current working directory.'

'--xml', action='store_true', required=False, help='Generate the xml file.'


# schedules_direct
Calls Schedules Direct JSON API and convert the retrieved schedules and programs to an XMLTV EPG file.

### xml & m3u arguments
```
  -U SD_URL, --sd-url SD_URL
                        Schedules Direct URL (no trailing '/')
  -u USERNAME, --username USERNAME
                        Schedules Direct username
  -p PASSWORD_SHA1, --password-sha1 PASSWORD_SHA1
                        Schedules Direct SHA1-hashed password
  -c COUNTRY, --country COUNTRY
                        3-character country code
  -z POSTALCODE, --postalcode POSTALCODE
                        Postal Code
  -l LINEUP, --lineup LINEUP
                        Lineup Code
  -H HEADERS, --headers HEADERS
                        HTTP Headers
  -M, --verboseMap      verboseMap off
  -T TIMEDELTA_DAYS, --timedelta-days TIMEDELTA_DAYS
                        Number of days retrieved
  -q, --quiet           Quiet on
  -v, --verbose         Verbose on
  -g, --debug           Debug on
  -A API_CALL, --api-call API_CALL
                        Schedules Direct API Call
  -S SERVICE, --service SERVICE
                        Schedules Direct Service name
  -X XMLTV_FILE, --xmltv-file XMLTV_FILE
  ```
                  
# ustvgo
Python script to convert ustvgo.tv guide into xml/m3u format.

### m3u arguments
'-m', '--m3u_file', required=False, default='ustvgo.m3u', help='Full destination filepath. Full file path can be specified. If only file name is specified then file will be placed in the current working directory.'

'-p', '--prefix', type=str, required=False, default='', help='Channel name prefix.'

'-s', '--start_number', type=int, required=False, default=1, help='Start numbering here. For example 9000.'

'--m3u', action='store_true', required=False, help='Generate the m3u file.'

'--streamlink', action='store_true', required=False, help='Generate the stream urls for use with Streamlink.'

### xml arguments
'--long_date', action='store_true', required=False, help='Use longer date format. Do not use for Plex Media Server.'

'-d', '--debug', action='store_true', required=False, help='Turn off headless mode for Firefox.'

'-t', '--timeout', type=int, default=10, help='Maximum number of seconds to wait for the response'

'--max_retries', type=int, default=3,help='Maximum number of attempts to collect data'

'-x', '--xml_file', default='ustvgo.xml', required=False, help='Full destination filepath. Full file path can be specified. If only file name is specified then file will be placed in the current working directory.'


# ustvgo_m3ugrabber
Python script to convert ustvgo.tv channels into m3u format.

### m3u arguments
None


# zap2xml-py
description="Python script to convert pull TV guide from Zap2It into xml format."

### xml arguments
'--aid', dest='zap_aid', type=str, default='gapzap',help='Raw zap2it input parameter.  (Affiliate ID?)'

'-c', '--country', dest='zap_country', type=str, default='USA',help='Country identifying the listings to fetch.'

'-d', '--delay', dest='delay', type=int, default=5, help='Delay, in seconds, between server fetches.'

'--device', dest='zap_device', type=str, default='-', help='Raw zap2it input parameter.  (?)'

'--headend-id', dest='zap_headendId', type=str, default='lineupId', help='Raw zap2it input parameter.  (?)'
      
'--is-override', dest='zap_isOverride', type=bool, default=True, help='Raw zap2it input parameter.  (?)'
      
'--language', dest='zap_languagecode', type=str, default='en', help='Raw zap2it input parameter.  (Language.)'

'--pref', dest='zap_pref', type=str, default='', help='Raw zap2it input parameter.  (Preferences?)'

'--timespan', dest='zap_timespan', type=int, default=3, help='Raw zap2it input parameter.  (Hours of data per fetch?)'

'--timezone', dest='zap_timezone', type=str, default='', help='Raw zap2it input parameter.  (Time zone?)'

'--user-id', dest='zap_userId', type=str, default='-', help='Raw zap2it input parameter.  (?)'

'-z', '--zip', '--postal', dest='zap_postalCode', type=str, required=True, help='The zip/postal code identifying the listings to fetch.'
