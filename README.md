# web2tv
This project contains python scripts which load and parse tv guide information and return the information in [xml](http://wiki.xmltv.org/index.php/XMLTVFormat) [format](https://github.com/XMLTV/xmltv/blob/master/xmltv.dtd). You can then use the xml in various other programs such as [xTeVe](https://github.com/xteve-project/xTeVe) or other iptv clients that allow epg in xml format.

Additionally there are scripts which generate [m3u](https://en.wikipedia.org/wiki/M3U) lists as well as some helper scripts.

All scripts were tested using Python 3.8

________________
*EPG Generation*
- plex.tv (plextv.py)
- pluto.tv (plutotv.py)
- schedules direct (schedules_direct.py)
- ustvgo.tv (ustvgo.py)
- zap2it (zap2xml.py)
________________
*M3U Generation*
- NextPVR (nextpvr.py)
- plex.tv (plextv.py)
- plutotv.com (plutotv.py)
- ustvgo.tv (ustvgo.py)
________________
*Helper Scripts*
- m3u_modder (convert m3u for use with [Streamlink](https://github.com/streamlink/streamlink))
________________

# m3u_modder
description="Python script to convert m3u for use with streamlink."

'-i', '--inFile', type=str, nargs=1, required=False, default=['streamlink.m3u'], help='Full input file filepath. Full file path can be specified. If only file name is specified then file will be used from the current working directory if it exists.'
    
'-o', '--outFile', type=str, nargs=1, required=False, default=['streamlink.m3u'], help='Full destination filepath. Full file path can be specified. If only file name is specified then file will be placed in the current working directory.'

'-p', '--protocol', type=str, nargs=1, required=False, default=['httpstream://'], help='Stream url protocol.'

# nextpvr
description="Python script to convert pluto tv channels into m3u format."

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

'-t', '--token', type=str, nargs=1, required=True, help='Token is required. Follow Plex instructions for finding the token. https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/#toc-0')

'-d', '--days', type=int, nargs=1, required=False, default=[7], help='Days of info to collect. Max if 21.'

'-p', '--pastdays', type=int, nargs=1, required=False, default=[0], help='Days in past of info to collect. Max is 1.'

'-l', '--language', type=str, nargs=1, required=False, default=['en'], help='Plex language... Get from url same as token.'

#xml arguments

'-x', '--xmlFile', type=str, nargs=1, required=False, default=['plex2.xml'], help='Full destination filepath for xml. Full file path can be specified. If only file name is specified then file will be placed in the current working directory.'

'--xml', action='store_true', required=False, help='Generate the xml file.'
    
#m3u arguments

'-m', '--m3uFile', type=str, nargs=1, required=False, default=['plex2.m3u'], help='Full destination filepath for m3u. Full file path can be specified. If only file name is specified then file will be placed in the current working directory.'

'--prefix', type=str, nargs=1, required=False, default=[''], help='Channel name prefix.'

'-s', '--startNumber', type=int, nargs=1, required=False, default=[1], help='Start numbering here. For example 9000. If -k, --keepNumber is used then channel 2 would become channel 9002, otherwise the first channel number found would be 9000, second channel found would be 9001, etc.'

'-k', '--keepNumber', action='store_true', required=False, help='Keep existing number scheme. Script will add existing number to start number. Recommended start number ends with a 0.'

'--m3u', action='store_true', required=False, help='Generate the m3u file.'

'--streamlink', action='store_true', required=False, help='Generate the stream urls for use with Streamlink.'


# plutotv
description="Python script to convert pluto tv guide into xml/m3u format."

'-e', '--epgHours', type=int, nargs=1, required=False, default=[10], help='Hours of EPG to collect. Pluto.TV only provides a few hours of EPG. Max allowed is 12.'

#xml arguments

'-x', '--xmlFile', type=str, nargs=1, required=False, default=['plutotv.xml'], help='Full destination filepath. Full file path can be specified. If only file name is specified then file will be placed in the current working directory.'

'--xml', action='store_true', required=False, help='Generate the xml file.'
    
#m3u arguments

'-m', '--m3uFile', type=str, nargs=1, required=False, default=['plutotv.m3u'], help='Full destination filepath. Full file path can be specified. If only file name is specified then file will be placed in the current working directory.'

'-p', '--prefix', type=str, nargs=1, required=False, default=[''], help='Channel name prefix.'

'-s', '--startNumber', type=int, nargs=1, required=False, default=[1], help='Start numbering here. For example 9000. If -k, --keepNumber is used then channel 2 would become channel 9002, otherwise the first channel number found would be 9000, second channel found would be 9001, etc.'

'-k', '--keepNumber', action='store_true', required=False, help='Keep existing number scheme. Script will add existing number to start number. Recommended start number ends with a 0.'

'--m3u', action='store_true', required=False, help='Generate the m3u file.'

'--streamlink', action='store_true', required=False, help='Generate the stream urls for use with Streamlink.'

# schedules_direct
description="Calls Schedules Direct JSON API and convert the retrieved schedules and programs to an XMLTV EPG file."

#xml & m3u arguments
```
-h, --help            show this help message and exit
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
description="Python script to convert ustvgo.tv guide into xml/m3u format."

'--long_date', action='store_true', required=False, help='Use longer date format. Do not use for Plex Media Server.'

'-d', '--debug', action='store_true', required=False, help='Turn off headless mode for Firefox.'

'-t', '--timeout', type=int, default=10, help='Maximum number of seconds to wait for the response'

'--max_retries', type=int, default=3,help='Maximum number of attempts to collect data'

#xml arguments

'-x', '--xml_file', default='ustvgo.xml', required=False, help='Full destination filepath. Full file path can be specified. If only file name is specified then file will be placed in the current working directory.'

#m3u arguments

'-m', '--m3u_file', required=False, default='ustvgo.m3u', help='Full destination filepath. Full file path can be specified. If only file name is specified then file will be placed in the current working directory.'

'-p', '--prefix', type=str, required=False, default='', help='Channel name prefix.'

'-s', '--start_number', type=int, required=False, default=1, help='Start numbering here. For example 9000.'

'--m3u', action='store_true', required=False, help='Generate the m3u file.'

'--streamlink', action='store_true', required=False, help='Generate the stream urls for use with Streamlink.'

# zap2xml-py

A very simple script to fetch EPG data from zap2it.com and write it to XMLTV format.
