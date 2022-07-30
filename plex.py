import argparse
import requests
import requests_cache
import time
from datetime import datetime
import dateutil.parser

import json
import xml.etree.ElementTree as ET

# url constants
url_type = '1%2C4'

default_headers = {
    'Accept': 'application/json'
}

xml_constants = {
    'source-info-url': 'https://www.plex.tv/watch-free-tv/',
    'source-info-name': 'plex.tv',
    'generator-info-name': 'web2tv',
    'generator-info-url': 'https://github.com/ReenigneArcher/web2tv'
}

# dictionary prebuild
rating_system = {
    'tvy': 'TV Parental Guidelines',
    'tvy7': 'TV Parental Guidelines',
    'tvg': 'TV Parental Guidelines',
    'tvpg': 'TV Parental Guidelines',
    'tv14': 'TV Parental Guidelines',
    'tvma': 'TV Parental Guidelines',
    'g': 'MPAA',
    'pg': 'MPAA',
    'pg13': 'MPAA',
    'r': 'MPAA',
    'nc17': 'MPAA',
    'u': 'BBFC',
    # 'pg' : 'BBFC',
    '12': 'BBFC',
    '12a': 'BBFC',
    '15': 'BBFC',
    '18': 'BBFC',
    'r18': 'BBFC',
    '0+': 'GIO',
    '6+': 'GIO',
    '12+': 'GIO',
    '15+': 'GIO',
    '18+': 'GIO',
    'nr': 'n/a',
    'ur': 'n/a'
}

rating_logo = {
    'tvy': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/TV-Y_icon.svg/240px-TV-Y_icon.svg.png',
    'tvy7': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/TV-Y7_icon.svg/240px-TV-Y7_icon.svg.png',
    'tvg': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/TV-G_icon.svg/240px-TV-G_icon.svg.png',
    'tvpg': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/TV-PG_icon.svg/240px-TV-PG_icon.svg.png',
    'tv14': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/TV-14_icon.svg/240px-TV-14_icon.svg.png',
    'tvma': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/TV-MA_icon.svg/240px-TV-MA_icon.svg.png',
    'g': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/RATED_G.svg/276px-RATED_G.svg.png',
    'pg': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/RATED_PG.svg/320px-RATED_PG.svg.png',
    'pg13': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/RATED_PG-13.svg/320px-RATED_PG-13.svg.png',
    'r': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/RATED_R.svg/284px-RATED_R.svg.png',
    'nc17': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Nc-17.svg/320px-Nc-17.svg.png',
    'u': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/BBFC_U_2019.svg/270px-BBFC_U_2019.svg.png',
    # 'pg': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/BBFC_PG_2019.svg/270px-BBFC_PG_2019.svg.png',
    '12': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/BBFC_12_2019.svg/240px-BBFC_12_2019.svg.png',
    '12a': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/BBFC_12A_2019.svg/240px-BBFC_12A_2019.svg.png',
    '15': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/BBFC_15_2019.svg/240px-BBFC_15_2019.svg.png',
    '18': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/BBFC_18_2019.svg/240px-BBFC_18_2019.svg.png',
    'r18': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/BBFC_R18_2019.svg/240px-BBFC_R18_2019.svg.png',
    '0+': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/GSRR_G_logo.svg/240px-GSRR_G_logo.svg.png',
    '6+': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/GSRR_P_logo.svg/240px-GSRR_P_logo.svg.png',
    '12+': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/GSRR_PG_12_logo.svg/240px-GSRR_PG_12_logo.svg.png',
    '15+': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/GSRR_PG_15_logo.svg/240px-GSRR_PG_15_logo.svg.png',
    '18+': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/GSRR_R_logo.svg/240px-GSRR_R_logo.svg.png',
    'nr': 'https://loyoladigitaladvertising.files.wordpress.com/2014/02/nr-logo.png',
    'ur': 'http://3.bp.blogspot.com/-eyIrE_lKiMg/Ufbis7lWLlI/AAAAAAAAAK4/4XTYHCU8Dx4/s1600/ur+logo.png'
}

xml_video_dict = {
    '480': {
        'aspect': '16:9',
        'quality': 'SD'
    },
    '720': {
        'aspect': '16:9',
        'quality': 'HDTV'
    },
    '1080': {
        'aspect': '16:9',
        'quality': 'HDTV'
    }
}


def get_args():
    # argparse
    parser = argparse.ArgumentParser(description="Python script to convert plex livetv guide into xml/m3u format.",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-t', '--token', type=str, required=True,
                        help='Token is required. Follow Plex instructions for finding the token. https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/#toc-0')
    parser.add_argument('-d', '--days', type=int, required=False, default=7,
                        help='Days of info to collect. Max is 21.')
    parser.add_argument('-p', '--pastdays', type=int, required=False, default=0,
                        help='Days in past of info to collect. Max is 1.')
    parser.add_argument('-l', '--language', type=str, required=False, default='en',
                        help='Plex language... Get from url same as token.')
    parser.add_argument('--number_as_name', action='store_true', required=False,
                        help='Use the channel number as the name and id. Improves channel display in Plex Media Server.')

    # xml arguments
    parser.add_argument('-x', '--xmlFile', type=str, required=False, default='plex2.xml',
                        help='Full destination filepath for xml. Full file path can be specified. If only file name '
                             'is specified then file will be placed in the current working directory.')
    parser.add_argument('--xml', action='store_true', required=False, help='Generate the xml file.')
    parser.add_argument('--long_date', action='store_true', required=False,
                        help='Use longer date format. Do not use for Plex Media Server.')
    parser.add_argument('--extended_metadata', action='store_true', required=False,
                        help='Use to get genres for each item. Results in significant API calls.')
    parser.add_argument('--cache_days', type=int, required=False, default=2,
                        help='Use to get genres for each item. Results in significant API calls.')

    # m3u arguments
    parser.add_argument('-m', '--m3uFile', type=str, required=False, default='plex2.m3u',
                        help='Full destination filepath for m3u. Full file path can be specified. If only file name is specified then file will be placed in the current working directory.')
    parser.add_argument('--prefix', type=str, required=False, default='', help='Channel name prefix.')
    parser.add_argument('-s', '--startNumber', type=int, required=False, default=1,
                        help='Start numbering here. For example 9000. If -k, --keepNumber is used then channel 2 would become channel 9002, otherwise the first channel number found would be 9000, second channel found would be 9001, etc.')
    parser.add_argument('-k', '--keepNumber', action='store_true', required=False,
                        help='Keep existing number scheme. Script will add existing number to start number. Recommended start number ends with a 0.')
    parser.add_argument('--m3u', action='store_true', required=False, help='Generate the m3u file.')
    parser.add_argument('--streamlink', action='store_true', required=False,
                        help='Generate the stream urls for use with Streamlink.')

    opts = parser.parse_args()

    # integer arguments
    if opts.days > 21:
        opts.days = 21
    if opts.pastdays > 1:
        opts.pastdays = 1

    return opts


def load_json(url, headers=default_headers):
    try:
        result = requests.get(url=url, headers=headers).json()
    except json.decoder.JSONDecodeError:
        return False
    return result


def isotime_convert(iso_time, short=True):
    time_value = dateutil.parser.isoparse(iso_time)  # https://stackoverflow.com/a/15228038/11214013
    if not short:
        result = time_value.strftime('%Y%m%d%H%M%S')
    else:
        result = time_value.strftime('%Y%m%d')
    return result

def main():
    args = get_args()

    # dictionary arrays to build
    channel_dict = {'data_test': [], 'data': []}
    program_dict = {'data': []}
    item_dict = {}
    stream_dict = {'data_test': [], 'data': []}

    # constants
    day = 24 * 60 * 60
    half_hour = 60 * 60 / 2

    days_total = args.days + args.pastdays  # define the total number of days

    now = time.time()
    now = int(now)
    now_30 = now - (now % half_hour)  # go back to nearest 30 minutes
    epg_begin = now_30 - (args.pastdays * day)  # now - 30 minutes - past days

    x = 0
    while x < days_total:  # do this for each day
        print('Loading Grid for PlexTV, day: ' + str(x + 1) + '/' + str(days_total))
        if x == 0:
            interval_a = int(epg_begin)
        else:
            interval_a = int(interval_b)
        interval_b = int(interval_a + day)

        url = f'https://epg.provider.plex.tv/grid?type={url_type}&sort=beginsAt&endsAt%3E={interval_a}&beginsAt%3C={interval_b}&X-Plex-Token={args.token}&X-Plex-Language={args.language}'

        print('url[' + str(x + 1) + ']: ' + url)
        grid = load_json(url)

        # with open('plex_xml_' + str(x) + '.json', 'w') as write_file:
        #     json.dump(grid, write_file, indent=4)

        y = 0
        for key in grid['MediaContainer']['Metadata']:
            metadata_data = {'thumb': False}

            # try to find thumb
            if not metadata_data['thumb']:  # try to get thumb from images list
                try:
                    for image in grid['MediaContainer']['Metadata'][y]['Image']:
                        if image['type'] == 'coverPoster':
                            metadata_data['thumb'] = image['url']
                            break
                except KeyError:
                    metadata_data['thumb'] = False

            if not metadata_data['thumb']:  # try to get thumb from grandparentthumb
                try:
                    metadata_data['thumb'] = grid['MediaContainer']['Metadata'][y]['grandparentThumb']
                except KeyError:
                    metadata_data['thumb'] = False

            if not metadata_data['thumb']:  # try to get thumb from thumb
                try:
                    metadata_data['thumb'] = grid['MediaContainer']['Metadata'][y]['thumb']
                except KeyError:
                    metadata_data['thumb'] = False

            if not metadata_data['thumb']:
                del metadata_data['thumb']

            metadata_data['media_type'] = grid['MediaContainer']['Metadata'][y]['type']  # episode or movie

            try:
                # episodes
                metadata_data['title'] = grid['MediaContainer']['Metadata'][y]['grandparentTitle']  # show title
                metadata_data['key'] = grid['MediaContainer']['Metadata'][y]['grandparentKey']  # show key
                metadata_data['sub_title'] = grid['MediaContainer']['Metadata'][y]['title']  # episode title
                metadata_data['season_number'] = grid['MediaContainer']['Metadata'][y]['parentIndex']
                try:
                    metadata_data['episode_number'] = grid['MediaContainer']['Metadata'][y]['index']
                except KeyError:
                    pass
            except KeyError:
                metadata_data['title'] = grid['MediaContainer']['Metadata'][y]['title']  # title when not an episode
                metadata_data['key'] = grid['MediaContainer']['Metadata'][y]['key']  # key when not an episode

            metadata_data['added_at'] = grid['MediaContainer']['Metadata'][y]['addedAt']
            metadata_data['year'] = grid['MediaContainer']['Metadata'][y]['year']
            metadata_data['rating_key'] = grid['MediaContainer']['Metadata'][y]['ratingKey']

            try:
                metadata_data['summary'] = grid['MediaContainer']['Metadata'][y]['summary']
            except KeyError:
                pass

            metadata_data['originally_available_at'] = grid['MediaContainer']['Metadata'][y]['originallyAvailableAt']

            try:
                metadata_data['content_rating'] = grid['MediaContainer']['Metadata'][y]['contentRating']
            except KeyError:
                metadata_data['content_rating'] = 'NR'

            z = 0
            for key in grid['MediaContainer']['Metadata'][y]['Media']:
                channel_data = {
                    'id': grid['MediaContainer']['Metadata'][y]['Media'][z]['channelIdentifier'],
                    'short_title': grid['MediaContainer']['Metadata'][y]['Media'][z]['channelShortTitle'],  # real title
                    'title': grid['MediaContainer']['Metadata'][y]['Media'][z]['channelTitle'],
                    'thumb': grid['MediaContainer']['Metadata'][y]['Media'][z]['channelThumb'],
                    'art': grid['MediaContainer']['Metadata'][y]['Media'][z]['channelArt']
                }

                if channel_data['title'] == 'undefined':
                    try:
                        channel_data['title'] = grid['MediaContainer']['Metadata'][y]['Media'][z]['channelCallSign']
                    except KeyError:
                        pass

                if channel_data not in channel_dict['data_test']:
                    channel_dict['data_test'].append(dict(channel_data))  # put into test without channel number

                    channel_data['channel_number'] = int(args.startNumber) - 1 + len(channel_dict['data_test'])
                    channel_dict['data'].append(dict(channel_data))  # put into data with channel number

                else:
                    counter = 0
                    for channel in channel_dict['data_test']:
                        if channel == channel_data:
                            channel_data['channel_number'] = int(args.startNumber) + counter
                        counter += 1

                if args.xml:
                    program_data = {'metadata': metadata_data}
                    program_data['metadata']['begins_at'] = grid['MediaContainer']['Metadata'][y]['Media'][z]['beginsAt']
                    program_data['metadata']['premiere'] = grid['MediaContainer']['Metadata'][y]['Media'][z]['premiere']
                    program_data['metadata']['ends_at'] = grid['MediaContainer']['Metadata'][y]['Media'][z]['endsAt']
                    program_data['metadata']['duration'] = int(grid['MediaContainer']['Metadata'][y]['Media'][z]['duration'] / 1000)
                    program_data['metadata']['resolution'] = grid['MediaContainer']['Metadata'][y]['Media'][z]['videoResolution']
                    program_data['metadata']['channel_data'] = channel_data

                    if program_data['metadata'] not in program_dict['data']:
                        program_dict['data'].append(dict(program_data['metadata']))

                if args.m3u:
                    stream_data = {
                        'CUID': channel_data['id'],
                        'tvg-logo': channel_data['thumb'],
                        'group-title': f'"PLEX.TV",{args.prefix}{channel_data["short_title"]}',
                        'url': f"https://epg.provider.plex.tv/library/parts/{channel_data['id']}?X-Plex-Token={args.token}"
                    }

                    if stream_data not in stream_dict['data_test']:
                        stream_dict['data_test'].append(dict(stream_data))  # put into test without channel number

                        if args.number_as_name:
                            stream_data['tvg-name'] = f"{channel_data['channel_number']}"
                            stream_data['tvg-ID'] = f"{channel_data['channel_number']}"
                        else:
                            stream_data['tvg-name'] = f"{args.prefix}{channel_data['short_title']}"
                            stream_data['tvg-ID'] = f"{args.prefix}{channel_data['short_title']}"

                        stream_data['tvg-chno'] = f"{channel_data['channel_number']}"
                        stream_dict['data'].append(dict(stream_data))  # put into data with channel number

                z += 1
            y += 1
        x += 1

    if args.xml:
        xml_tv = ET.Element("tv", xml_constants)

        for channel in channel_dict['data']:
            if args.number_as_name:
                xml_channel = ET.SubElement(xml_tv, "channel", {"id": f"{channel['channel_number']}"})

            else:
                xml_channel = ET.SubElement(xml_tv, "channel", {"id": f"{args.prefix}{channel['short_title']}"})
            ET.SubElement(xml_channel, "display-name").text = f"{args.prefix}{channel['short_title']}"

            display_names_types = ['title', 'id']
            display_names = []
            for display_name_type in display_names_types:
                try:
                    if channel[display_name_type] not in display_names:
                        display_names.append(channel[display_name_type])
                        ET.SubElement(xml_channel, "display-name").text = f'{channel[display_name_type]}'
                except KeyError:
                    pass

            ET.SubElement(xml_channel, "icon", {'src': channel['thumb']})

        for program in program_dict['data']:
            time_start = datetime.utcfromtimestamp(int(program['begins_at'])).strftime('%Y%m%d%H%M%S')
            time_end = datetime.utcfromtimestamp(int(program['ends_at'])).strftime('%Y%m%d%H%M%S')
            time_added = datetime.utcfromtimestamp(int(program['added_at'])).strftime('%Y%m%d%H%M%S')
            time_original_long = isotime_convert(program['originally_available_at'], short=False)
            time_original_short = isotime_convert(program['originally_available_at'], short=True)

            offset = '+0000'

            if args.number_as_name:
                temp_channel = f"{program['channel_data']['channel_number']}"
            else:
                temp_channel = f"{args.prefix}{program['channel_data']['short_title']}"

            program_header_dict = {
                'start': f'{time_start} {offset}',
                'stop': f'{time_end} {offset}',
                'channel': temp_channel
            }

            xml_program = ET.SubElement(xml_tv, "programme", program_header_dict)

            try:
                ET.SubElement(xml_program, "title", {'lang': args.language}).text = program['title']
                print(program['title'])
            except KeyError:
                pass

            try:
                ET.SubElement(xml_program, "desc", {'lang': args.language}).text = program['summary']
            except KeyError:
                pass

            try:
                ET.SubElement(xml_program, "length", {'units': 'seconds'}).text = str(program['duration'])
            except KeyError:
                pass

            if time_original_long != '' and args.long_date:
                time_original = f'{time_original_long} {offset}'
            elif time_original_short != '':
                time_original = time_original_short
            else:
                time_original = str(program['year'])

            ET.SubElement(xml_program, "date").text = time_original

            try:
                ET.SubElement(xml_program, "sub-title", {'lang': args.language}).text = program['sub_title']
            except KeyError:
                pass

            try:
                ET.SubElement(xml_program, "icon", {'src': program['thumb']})
            except KeyError:
                pass

            numbers = ['season_number', 'episode_number']
            onscreen_ns = ''
            common_ns = ''
            xmltv_ns = ''
            plex_ns = program['rating_key']

            season_found = False

            for number in numbers:
                try:
                    program[number]
                    if number == 'season_number':
                        season_found = True
                except KeyError:
                    pass

                try:
                    if program[number] < 10:
                        program[number] = f'0{program[number]}'
                    else:
                        program[number] = f'{program[number]}'

                    if number == 'season_number':
                        onscreen_ns = f'S{program[number]}'
                        common_ns = f'S{program[number]}'
                        xmltv_ns = f'{int(program[number]) - 1}'
                    else:
                        if season_found:
                            onscreen_ns = f'{onscreen_ns}E{program[number]}'
                            common_ns = f'{common_ns}E{program[number]}'
                            try:
                                xmltv_ns = f'{xmltv_ns}.{int(program[number]) -1}.'
                            except ValueError:
                                pass
                                
                except KeyError:
                    pass

            if onscreen_ns != '':
                ET.SubElement(xml_program, "episode-num", {'system': 'onscreen'}).text = onscreen_ns

            if common_ns != '':
                ET.SubElement(xml_program, "episode-num", {'system': 'common'}).text = common_ns

            if xmltv_ns != '':
                ET.SubElement(xml_program, "episode-num", {'system': 'xmltv_ns'}).text = xmltv_ns

            if plex_ns != '':
                ET.SubElement(xml_program, "episode-num", {'system': 'plex'}).text = plex_ns

            try:
                xml_rating = ET.SubElement(xml_program, "rating", {'system': rating_system[program['content_rating'].lower().replace('-', '')]})
                ET.SubElement(xml_rating, "value").text = program['content_rating']
                ET.SubElement(xml_rating, "icon", {"src": rating_logo[program['content_rating'].lower().replace('-', '')]})
            except KeyError:
                pass

            #extended metadata
            if args.extended_metadata:
                urls_expire_after = {
                    '*/library/metadata/*': 60 * 60 * 24 * args.cache_days,
                    '*': 0,  # Every other non-matching URL: do not cache
                }

                requests_cache.install_cache('cache/web2tv', backend='sqlite', urls_expire_after=urls_expire_after)

                # genre
                item_key = program['key']

                try:
                    item_data = item_dict[item_key]
                except KeyError:
                    item_url = f"https://epg.provider.plex.tv{item_key}?&X-Plex-Token={args.token}&X-Plex-Language={args.language}"
                    item_data = load_json(item_url)
                    if item_data:
                        item_dict[item_key] = item_data

                try:
                    for genre in item_data['MediaContainer']['Metadata'][0]['Genre']:
                        ET.SubElement(xml_program, "category", {'lang': args.language}).text = genre['tag']
                except KeyError:
                    pass

            else:
                if program['media_type'] == 'movie':
                    ET.SubElement(xml_program, "category", {'lang': args.language}).text = 'Movie'

            if not program['premiere']:
                if time_original != '':
                    ET.SubElement(xml_program, "previously-shown", {'start': f'{time_original} {offset}'})
                else:
                    ET.SubElement(xml_program, "previously-shown")
            else:
                ET.SubElement(xml_program, "premiere")

            try:
                xml_video = ET.SubElement(xml_program, "video")
                ET.SubElement(xml_video, "present").text = 'yes'
                ET.SubElement(xml_video, "aspect").text = xml_video_dict[program['resolution']]['aspect']
                ET.SubElement(xml_video, "quality").text = xml_video_dict[program['resolution']]['quality']
            except KeyError:
                pass

        # write the file
        print('xml is being created')
        with open(args.xmlFile, "wb") as f:  # https://stackoverflow.com/a/42495690/11214013
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n'.encode('utf-8'))
            f.write('<!DOCTYPE tv SYSTEM "xmltv.dtd">\n'.encode('utf-8'))

            new_xml = ET.ElementTree(xml_tv)
            try:
                ET.indent(new_xml, space="\t", level=0)
            except AttributeError:
                print('Warning: Upgrade to Python 3.9 to have indented xml')
            new_xml.write(f, encoding='utf-8')

        print('xml has being written')

    if args.m3u:
        # write the file
        print('m3u is being created')
        with open(args.m3uFile, 'w', encoding='utf-8') as f:  # https://stackoverflow.com/a/35086151/11214013
            f.write('#EXTM3U\n')

            x = 0
            for stream in stream_dict['data']:
                f.write(f'#EXTINF:-1 tvg-ID="{stream["tvg-ID"]}" CUID="{stream["CUID"]}" tvg-chno="{stream["tvg-chno"]}" tvg-name="{stream["tvg-name"]}" tvg-logo="{stream["tvg-logo"]}" group-title={stream["group-title"]}\n')

                if args.streamlink:
                    f.write(f"hls://{stream['url']}\n")
                else:
                    f.write(f"{stream['url']}\n")

                x += 1

        print('m3u is being closed')


if __name__ == '__main__':
    main()
