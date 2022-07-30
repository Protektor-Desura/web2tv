import argparse
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import sys
import zipfile
import tarfile
import json
import xml.etree.ElementTree as ET

import re
from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumwire import webdriver

xml_constants = {
    'source-info-url': 'https://ustvgo.tv',
    'source-info-name': 'ustvgo.tv',
    'generator-info-name': 'web2tv',
    'generator-info-url': 'https://github.com/ReenigneArcher/web2tv'
}

default_headers = {
    'Accept': 'application/json'
}

channel_logos = {
    'abc': 'https://zap2it.tmsimg.com/h3/NowShowing/10003/s10003_h3_aa.png',
    'acc network': 'https://zap2it.tmsimg.com/h3/NowShowing/111871/s111871_h3_aa.png',
    'ae': 'https://zap2it.tmsimg.com/h3/NowShowing/10035/s10035_h3_aa.png',
    'amc': 'https://zap2it.tmsimg.com/h3/NowShowing/10021/s10021_h3_aa.png',
    'animal': 'https://zap2it.tmsimg.com/h3/NowShowing/16331/s16331_h3_aa.png',
    'bbcamerica': 'https://zap2it.tmsimg.com/h3/NowShowing/18332/s18332_h3_aa.png',
    'big ten network': 'https://zap2it.tmsimg.com/h3/NowShowing/56783/s56783_h3_aa.png',
    'bet': 'https://zap2it.tmsimg.com/h3/NowShowing/10051/s10051_h3_aa.png',
    'boomerang': 'https://zap2it.tmsimg.com/h3/NowShowing/21883/s21883_h3_aa.png',
    'bravo': 'https://zap2it.tmsimg.com/h3/NowShowing/10057/s10057_h3_aa.png',
    'c-span': 'https://zap2it.tmsimg.com/h3/NowShowing/10161/s10161_h3_aa.png',
    'cbs': 'https://zap2it.tmsimg.com/h3/NowShowing/10098/s10098_h3_aa.png',
    'cbs sports network': 'https://zap2it.tmsimg.com/h3/NowShowing/16365/s16365_h3_aa.png',
    'cinemax': 'https://zap2it.tmsimg.com/h3/NowShowing/10120/s10120_h3_aa.png',
    'cmt': 'https://zap2it.tmsimg.com/h3/NowShowing/10138/s10138_h3_aa.png',
    'cartoon network': 'https://zap2it.tmsimg.com/h3/NowShowing/12131/s12131_h3_aa.png',
    'cnbc': 'https://zap2it.tmsimg.com/h3/NowShowing/10139/s10139_h3_aa.png',
    'cnn': 'https://zap2it.tmsimg.com/h3/NowShowing/10142/s10142_h3_aa.png',
    'comedy': 'https://zap2it.tmsimg.com/h3/NowShowing/10149/s10149_h3_aa.png',
    'cw': 'https://zap2it.tmsimg.com/h3/NowShowing/51306/s51306_h3_aa.png',
    'destination america': 'https://zap2it.tmsimg.com/h3/NowShowing/16617/s16617_h3_aa.png',
    'discovery': 'https://zap2it.tmsimg.com/h3/NowShowing/11150/s11150_h3_aa.png',
    'disney': 'https://zap2it.tmsimg.com/h3/NowShowing/10171/s10171_h3_aa.png',
    'disneyjr': 'https://zap2it.tmsimg.com/h3/NowShowing/74796/s74796_h3_aa.png',
    'disneyxd': 'https://zap2it.tmsimg.com/h3/NowShowing/18279/s18279_h3_aa.png',
    'do it yourself ( diy )': 'https://zap2it.tmsimg.com/h3/NowShowing/67375/s67375_h3_aa.png',
    'e!': 'https://zap2it.tmsimg.com/h3/NowShowing/10989/s10989_h3_aa.png',
    'espn': 'https://zap2it.tmsimg.com/h3/NowShowing/10179/s10179_h3_aa.png',
    'espn2': 'https://zap2it.tmsimg.com/h3/NowShowing/12444/s12444_h3_aa.png',
    'espnu': 'https://zap2it.tmsimg.com/h3/NowShowing/45654/s45654_h3_aa.png',
    'espnews': 'https://zap2it.tmsimg.com/h3/NowShowing/16485/s16485_h3_aa.png',
    'foodnetwork': 'https://zap2it.tmsimg.com/h3/NowShowing/12574/s12574_h3_aa.png',
    'fox': 'https://zap2it.tmsimg.com/h3/NowShowing/10212/s10212_h3_aa.png',
    'foxbusiness': 'https://zap2it.tmsimg.com/h3/NowShowing/58649/s58649_h3_aa.png',
    'foxnews': 'https://zap2it.tmsimg.com/h3/NowShowing/16374/s16374_h3_aa.png',
    'freeform': 'https://zap2it.tmsimg.com/h3/NowShowing/10093/s10093_h3_aa.png',
    'fox sports 1 (fs1)': 'https://zap2it.tmsimg.com/h3/NowShowing/82541/s82541_h3_aa.png',
    'fox sports 2 (fs2)': 'https://zap2it.tmsimg.com/h3/NowShowing/33178/s33178_h3_aa.png',
    'fx': 'https://zap2it.tmsimg.com/h3/NowShowing/14321/s14321_h3_aa.png',
    'fx movie channel': 'https://zap2it.tmsimg.com/h3/NowShowing/14988/s14988_h3_aa.png',
    'fxx': 'https://zap2it.tmsimg.com/h3/NowShowing/17927/s17927_h3_aa.png',
    'golf channel': 'https://zap2it.tmsimg.com/h3/NowShowing/14899/s14899_h3_aa.png',
    'game show network': 'https://zap2it.tmsimg.com/h3/NowShowing/14909/s14909_h3_aa.png',
    'hallmark channel': 'https://zap2it.tmsimg.com/h3/NowShowing/11221/s11221_h3_aa.png',
    'hbo': 'https://zap2it.tmsimg.com/h3/NowShowing/10240/s10240_h3_aa.png',
    'hgtv': 'https://zap2it.tmsimg.com/h3/NowShowing/14902/s14902_h3_aa.png',
    'history': 'https://zap2it.tmsimg.com/h3/NowShowing/14771/s14771_h3_aa.png',
    'hln': 'https://zap2it.tmsimg.com/h3/NowShowing/10145/s10145_h3_aa.png',
    'hallmark movies & mysteries': 'https://zap2it.tmsimg.com/h3/NowShowing/46710/s46710_h3_aa.png',
    'investigation discovery': 'https://zap2it.tmsimg.com/h3/NowShowing/16615/s16615_h3_aa.png',
    'lifetime': 'https://zap2it.tmsimg.com/h3/NowShowing/10918/s10918_h3_aa.png',
    'lifetime movie network': 'https://zap2it.tmsimg.com/h3/NowShowing/18480/s18480_h3_aa.png',
    'mlb network': 'https://zap2it.tmsimg.com/h3/NowShowing/62081/s62081_h3_aa.png',
    'motor trend': 'https://zap2it.tmsimg.com/h3/NowShowing/31046/s31046_h3_aa.png',
    'msnbc': 'https://zap2it.tmsimg.com/h3/NowShowing/16300/s16300_h3_aa.png',
    'mtv': 'https://zap2it.tmsimg.com/h3/NowShowing/10986/s10986_h3_aa.png',
    'national geographic': 'https://zap2it.tmsimg.com/h3/NowShowing/24959/s24959_h3_aa.png',
    'nat geo wild': 'https://zap2it.tmsimg.com/h3/NowShowing/66804/s66804_h3_aa.png',
    'nba tv': 'https://zap2it.tmsimg.com/h3/NowShowing/32281/s32281_h3_aa.png',
    'nbc': 'https://zap2it.tmsimg.com/h3/NowShowing/10991/s10991_h3_aa.png',
    'nbc sports ( nbcsn )': 'https://zap2it.tmsimg.com/h3/NowShowing/15952/s15952_h3_aa.png',
    'nfl network': 'https://zap2it.tmsimg.com/h3/NowShowing/45399/s45399_h3_aa.png',
    'nfl redzone': 'https://zap2it.tmsimg.com/h3/NowShowing/65025/s65025_h3_aa.png',
    'nickelodeon': 'https://zap2it.tmsimg.com/h3/NowShowing/11006/s11006_h3_aa.png',
    'nicktoons': 'https://zap2it.tmsimg.com/h3/NowShowing/30420/s30420_h3_aa.png',
    'one america news network': 'https://zap2it.tmsimg.com/h3/NowShowing/82542/s82542_h3_aa.png',
    'oprah winfrey network (own)': 'https://zap2it.tmsimg.com/h3/NowShowing/70387/s70387_h3_aa.png',
    'olympic channel': 'https://zap2it.tmsimg.com/h3/NowShowing/104089/s104089_h3_aa.png',
    'oxygen': 'https://zap2it.tmsimg.com/h3/NowShowing/21484/s21484_h3_aa.png',
    'paramount': 'https://zap2it.tmsimg.com/h3/NowShowing/11163/s11163_h3_aa.png',
    'pbs': 'https://zap2it.tmsimg.com/h3/NowShowing/11039/s11039_h3_aa.png',
    'pop': 'https://zap2it.tmsimg.com/h3/NowShowing/16715/s16715_h3_aa.png',
    'science': 'https://zap2it.tmsimg.com/h3/NowShowing/16616/s16616_h3_aa.png',
    'sec network': 'https://zap2it.tmsimg.com/h3/NowShowing/89714/s89714_h3_aa.png',
    'showtime': 'https://zap2it.tmsimg.com/h3/NowShowing/11115/s11115_h3_aa.png',
    'starz': 'https://zap2it.tmsimg.com/h3/NowShowing/12719/s12719_h3_aa.png',
    'sundancetv': 'https://zap2it.tmsimg.com/h3/NowShowing/16108/s16108_h3_aa.png',
    'syfy': 'https://zap2it.tmsimg.com/h3/NowShowing/11097/s11097_h3_aa.png',
    'tbs': 'https://zap2it.tmsimg.com/h3/NowShowing/11867/s11867_h3_aa.png',
    'turner classic movies (tcm)': 'https://zap2it.tmsimg.com/h3/NowShowing/12852/s12852_h3_aa.png',
    'telemundo': 'https://zap2it.tmsimg.com/h3/NowShowing/10239/s10239_h3_aa.png',
    'tennis channel': 'https://zap2it.tmsimg.com/h3/NowShowing/60316/s60316_h3_aa.png',
    'tlc': 'https://zap2it.tmsimg.com/h3/NowShowing/11158/s11158_h3_aa.png',
    'tnt': 'https://zap2it.tmsimg.com/h3/NowShowing/11164/s11164_h3_aa.png',
    'travel channel': 'https://zap2it.tmsimg.com/h3/NowShowing/11180/s11180_h3_aa.png',
    'trutv': 'https://zap2it.tmsimg.com/h3/NowShowing/10153/s10153_h3_aa.png',
    'tv land': 'https://zap2it.tmsimg.com/h3/NowShowing/16123/s16123_h3_aa.png',
    'the weather channel': 'https://zap2it.tmsimg.com/h3/NowShowing/11187/s11187_h3_aa.png',
    'univision': 'https://zap2it.tmsimg.com/h3/NowShowing/11118/s11118_h3_aa.png',
    'usa network': 'https://zap2it.tmsimg.com/h3/NowShowing/11207/s11207_h3_aa.png',
    'vh1': 'https://zap2it.tmsimg.com/h3/NowShowing/11218/s11218_ll_h15_ab.png',
    'we tv': 'https://zap2it.tmsimg.com/h3/NowShowing/16409/s16409_h3_aa.png',
    'wwe network': 'https://upload.wikimedia.org/wikipedia/commons/f/fc/WWENetworkLogo.png',  # only image not from zap2it
    'yes network': 'https://zap2it.tmsimg.com/h3/NowShowing/63558/s63558_h3_aa.png'
}


def check_gecko_driver():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bin_dir = os.path.join(script_dir, 'bin')

    if sys.platform.startswith('linux'):
        platform = 'linux'
        url = 'https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz'
        local_platform_path = os.path.join(bin_dir, platform)
        local_driver_path = os.path.join(local_platform_path, 'geckodriver')
        var_separator = ':'
    elif sys.platform == 'darwin':
        platform = 'mac'
        url = 'https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-macos.tar.gz'
        local_platform_path = os.path.join(bin_dir, platform)
        local_driver_path = os.path.join(local_platform_path, 'geckodriver')
        var_separator = ':'
    elif sys.platform.startswith('win'):
        platform = 'win'
        url = 'https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-win64.zip'
        local_platform_path = os.path.join(bin_dir, platform)
        local_driver_path = os.path.join(local_platform_path, 'geckodriver.exe')
        var_separator = ';'
    else:
        raise RuntimeError('Could not determine your OS')

    if not os.path.isdir(bin_dir):
        os.mkdir(bin_dir)

    if not os.path.isdir(local_platform_path):
        os.mkdir(local_platform_path)

    if not os.path.isfile(local_driver_path):
        print('Downloading gecko driver...', file=sys.stderr)
        data_resp = requests.get(url, stream=True)
        file_name = url.split('/')[-1]
        tgt_file = os.path.join(local_platform_path, file_name)
        with open(tgt_file, 'wb') as f:
            for chunk in data_resp.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        if file_name.endswith('.zip'):
            with zipfile.ZipFile(tgt_file, 'r') as f_zip:
                f_zip.extractall(local_platform_path)
        else:
            with tarfile.open(tgt_file, 'r') as f_gz:
                f_gz.extractall(local_platform_path)

        if not os.access(local_driver_path, os.X_OK):
            os.chmod(local_driver_path, 0o744)

        os.remove(tgt_file)

    if 'PATH' not in os.environ:
        os.environ['PATH'] = local_platform_path
    elif local_driver_path not in os.environ['PATH']:
        os.environ['PATH'] = local_platform_path + var_separator + os.environ['PATH']


def get_args():
    # argparse
    parser = argparse.ArgumentParser(description="Python script to convert ustvgo.tv guide into xml/m3u format.",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--number_as_name', action='store_true', required=False,
                        help='Use the channel number as the name and id. Improves channel display in Plex Media Server.')
    parser.add_argument('--proxy', type=str, default=None, help='Use proxy.')


    # xml arguments
    parser.add_argument('-x', '--xml_file', type=str, required=False, default='ustvgo.xml',
                        help='Full destination filepath. Full file path can be specified. If only file name is specified then file will be placed in the current working directory.')
    parser.add_argument('--xml', action='store_true', required=False, help='Generate the xml file.')
    parser.add_argument('--long_date', action='store_true', required=False,
                        help='Use longer date format. Do not use for Plex Media Server.')

    # m3u arguments
    parser.add_argument('-m', '--m3u_file', type=str, required=False, default='ustvgo.m3u',
                        help='Full destination filepath. Full file path can be specified. If only file name is specified then file will be placed in the current working directory.')
    parser.add_argument('-p', '--prefix', type=str, required=False, default='', help='Channel name prefix.')
    parser.add_argument('-s', '--start_number', type=int, required=False, default=1,
                        help='Start numbering here. For example 9000.')
    parser.add_argument('--m3u', action='store_true', required=False, help='Generate the m3u file.')
    parser.add_argument('--streamlink', action='store_true', required=False,
                        help='Generate the stream urls for use with Streamlink.')
    parser.add_argument('-d', '--debug', action='store_true', required=False,
                        help='Turn of headless mode for Firefox.')
    parser.add_argument('-t', '--timeout', type=int, default=10,
                        help='Maximum number of seconds to wait for the response')
    parser.add_argument('--max_retries', type=int, default=3,
                        help='Maximum number of attempts to collect data')

    opts = parser.parse_args()

    opts.language = 'en'

    return opts


def load_json(url, headers=default_headers):
    result = requests.get(url=url, headers=headers).json()
    return result


def build_channel_list(args):
    url = 'https://ustvgo.tv/'

    try:
        response = requests.get(url)
    except requests.RequestException as e:
        return False

    soup = BeautifulSoup(response.content, "lxml")

    channels = {}

    x = 0
    for item in soup.find('ol').find_all('li'):
        number = x + args.start_number

        try:
            channels[number] = {
                'name': item.find('a').text.strip(),
                'url': item.find('a').get('href')
            }

            x += 1
        except:
            pass

    return channels


def get_channel_data(args, channels):
    authentication = False

    for channel_number, channel_data in channels.items():
        response = requests.get(channel_data['url'])

        soup = BeautifulSoup(response.content, "lxml")

        if args.xml:
            json_url = False
            for item in soup.find_all('iframe'):
                if item['src'].startswith('/tvguide/index.html#'):
                    json_url = f"https://ustvgo.tv{item['src']}.json".replace('index.html#', 'JSON2/')
                    break

            channel_data['programs'] = []
            if json_url:
                grid = load_json(json_url)

                for day, programs in grid['items'].items():
                    for program in programs:
                        channel_data['programs'].append(dict(program))

        if args.m3u:
            for item in soup.find_all('iframe'):
                if item['src'].startswith('/clappr.php?stream='):
                    stream = item['src'].rsplit('=', 1)[-1]
                    channel_data['stream'] = stream

            if not authentication:
                authentication = update_authentication(args, channel_data)

    return channels, authentication


def update_authentication(args, channel):
    # https://github.com/interlark/ustvgo_downloader/blob/master/update.py
    ff_options = FirefoxOptions()
    if not args.debug:
        ff_options.headless = True

    seleniumwire_options = {
        'connection_timeout': None,
        'verify_ssl': True,
        'suppress_connection_errors': True
    }

    if args.proxy:  # failing when trying to use proxy...
        seleniumwire_options['proxy'] = {
            'https': f'{args.proxy}',
            'https': f'{args.proxy}',
            'no_proxy': 'localhost,127.0.0.1'
        }

    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference('permissions.default.image', 2)
    firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    firefox_profile.set_preference('dom.disable_beforeunload', True)
    firefox_profile.set_preference('browser.tabs.warnOnClose', False)
    firefox_profile.set_preference('media.volume_scale', '0.0')

    driver = webdriver.Firefox(
        seleniumwire_options=seleniumwire_options,
        options=ff_options,
        firefox_profile=firefox_profile
    )

    IFRAME_CSS_SELECTOR = '.iframe-container>iframe'
    POPUP_ACCEPT_XPATH_SELECTOR = '//button[contains(text(),"AGREE")]'

    retry = 1
    url_parts = False

    while retry < args.max_retries and not url_parts:
        try:
            driver.get(channel['url'])

            # Get iframe
            iframe = None
            try:
                iframe = driver.find_element_by_css_selector(IFRAME_CSS_SELECTOR)
            except NoSuchElementException:
                break

            # Detect VPN-required channels
            try:
                driver.switch_to.frame(iframe)
                driver.find_element_by_xpath("//*[text()='Please use our VPN to watch this channel!']")
                need_vpn = True
            except NoSuchElementException:
                need_vpn = False
            finally:
                driver.switch_to.default_content()

            if need_vpn:
                break

            # close popup if it shows up
            try:
                driver.find_element_by_xpath(POPUP_ACCEPT_XPATH_SELECTOR).click()
            except NoSuchElementException:
                pass

            # Autoplay
            iframe.click()

            try:
                playlist = driver.wait_for_request('/playlist.m3u8', timeout=args.timeout)
            except TimeoutException:
                playlist = None

            if playlist:
                video_link = str(playlist)

                url_parts = video_link.split(f"/{channel['stream']}/", 1)

                if len(url_parts) == 2:
                    break
            else:
                raise Exception()

        except Exception as e:
            print('Failed to get key, retry(%d) ...' % retry)
            retry += 1

        except KeyboardInterrupt:
            driver.close()
            driver.quit()
            sys.exit(1)

    driver.close()
    driver.quit()

    return url_parts

    try:
        return captured_key
    except NameError:
        return False


def main():
    args = get_args()

    if args.xml:
        xml_tv = ET.Element("tv", xml_constants)

    if args.m3u:
        check_gecko_driver()
        m3u_f = open(args.m3u_file, "w", encoding='utf-8')

        m3u_f.write('#EXTM3U\n')

    channels = build_channel_list(args)
    channels, authentication = get_channel_data(args, channels)

    for channel_number, channel in channels.items():
        if args.number_as_name:
            channel_id = str(channel_number)

        else:
            channel_id = f"{args.prefix}{channel['name']}"

        if args.xml:
            xml_channel = ET.SubElement(xml_tv, "channel", {"id": channel_id})

            if args.prefix != '':
                ET.SubElement(xml_channel, "display-name").text = f"{args.prefix}{channel['name']}"
            print(channel['name'])

            display_names_types = ['name']
            display_names = []
            for display_name_type in display_names_types:
                try:
                    if channel[display_name_type] not in display_names:
                        display_names.append(channel[display_name_type])
                        ET.SubElement(xml_channel, "display-name").text = f'{channel[display_name_type]}'
                except KeyError:
                    pass

            try:
                ET.SubElement(xml_channel, "icon", {'src': channel_logos[channel['name'].lower()]})
            except KeyError:
                pass

            for program in channel['programs']:
                time_start = datetime.utcfromtimestamp(int(program['start_timestamp'])).strftime('%Y%m%d%H%M%S')
                time_end = datetime.utcfromtimestamp(int(program['end_timestamp'])).strftime('%Y%m%d%H%M%S')

                offset = '+0000'

                program_header_dict = {
                    'start': f'{time_start} {offset}',
                    'stop': f'{time_end} {offset}',
                    'channel': channel_id
                }

                xml_program = ET.SubElement(xml_tv, "programme", program_header_dict)

                try:
                    ET.SubElement(xml_program, "title", {'lang': args.language}).text = program['name']
                    print(program['name'])
                except KeyError:
                    pass

                try:
                    if program['description'] != "":
                        ET.SubElement(xml_program, "desc", {'lang': args.language}).text = program['description']
                except KeyError:
                    pass

                try:
                    ET.SubElement(xml_program, "length", {'units': 'seconds'}).text = str(program['end_timestamp'] - program['start_timestamp'])
                except KeyError:
                    pass

                try:
                    if program['image'] != "":
                        ET.SubElement(xml_program, "icon", {'src': program['image']})
                except KeyError:
                    pass

                try:
                    ET.SubElement(xml_program, "episode-num", {'system': 'ustvgo'}).text = str(program['id'])
                except KeyError:
                    pass

                xml_video = ET.SubElement(xml_program, "video")
                ET.SubElement(xml_video, "present").text = 'yes'

        if args.m3u:
            print(channel['url'])

            if authentication:
                if args.number_as_name:
                    tvg_name = f"{channel_number}"
                    tvg_id = f"{channel_number}"
                    cuid = f"{channel_number}"
                else:
                    tvg_name = f"{args.prefix}{channel['name']}"
                    tvg_id = f"{args.prefix}{channel['name']}"
                    cuid = f"{args.prefix}{channel['name']}"

                tvg_chno = f"{channel_number}"
                group_title = f'"USTVGO.TV",{args.prefix}{channel["name"]}'

                try:
                    tvg_logo = channel_logos[channel['name'].lower()]
                    m3u_f.write(
                        f'#EXTINF:-1 tvg-ID="{tvg_id}" CUID="{cuid}" tvg-chno="{tvg_chno}" tvg-name="{tvg_name}" tvg-logo="{tvg_logo}" group-title={group_title}\n')
                except KeyError:
                    m3u_f.write(
                        f'#EXTINF:-1 tvg-ID="{tvg_id}" CUID="{cuid}" tvg-chno="{tvg_chno}" tvg-name="{tvg_name}" group-title={group_title}\n')

                if args.streamlink:
                    m3u_f.write(f"hls://{authentication[0]}/{channel['stream']}/{authentication[1]}\n")

                else:
                    m3u_f.write(f"{authentication[0]}/{channel['stream']}/{authentication[1]}\n")

    if args.xml:
        # write the xml file
        print('xml is being created')
        with open(args.xml_file, "wb") as xml_f:  # https://stackoverflow.com/a/42495690/11214013
            xml_f.write('<?xml version="1.0" encoding="UTF-8"?>\n'.encode('utf-8'))
            xml_f.write('<!DOCTYPE tv SYSTEM "xmltv.dtd">\n'.encode('utf-8'))

            new_xml = ET.ElementTree(xml_tv)

            try:
                ET.indent(new_xml, space="\t", level=0)
            except AttributeError:
                print('Warning: Upgrade to Python 3.9 to have indented xml')
            new_xml.write(xml_f, encoding='utf-8')

        print('xml has being written')

    if args.m3u:
        print('m3u is being closed')
        m3u_f.close()


if __name__ == '__main__':
    main()
