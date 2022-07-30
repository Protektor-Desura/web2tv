# -*- coding: utf-8 -*-

import argparse
import requests

if __name__ == '__main__':
    def quote_remover(string):
        if string.startswith('"') and string.endswith('"'):
            string = string[1:-1]
        elif string.startswith("'") and string.endswith("'"):
            string = string[1:-1]
        else:
            string = string
        return string

    def get_number(channel):
        return channel.get('channelNumber')

    def doRequest5(method, isJSON = True):
        retval = False
        getResult = None
        url = "http://" + ip + ":" + str(port) + '/service?method=' + method
        if (not 'session.initiate' in method):
            url += '&sid=' + sid
        #print(url)
        try:
            headers={"Accept" : "application/json"}
            getResult = requests.get(url, headers=headers).json()
            retval = True
        except Exception as e:
            print(str(e))

        return retval, getResult

    def hashMe (thedata):
        import hashlib
        h = hashlib.md5()
        h.update(thedata.encode('utf-8'))
        return h.hexdigest()

    def sidLogin5():
        method = 'session.initiate&ver=1.0&device=emby'
        ret, keys = doRequest5(method)
        global sid
        if ret == True:
            sid =  keys['sid']
            salt = keys['salt']
            method = 'session.login&md5=' + hashMe(':' + hashMe(pin) + ':' + salt)
            ret, login  = doRequest5(method)
            if ret and login['stat'] == 'ok':
                sid =  login['sid']
            else:
                print ("Fail")
        else:
            print ("Fail")

    #argparse
    parser = argparse.ArgumentParser(description="Python script to convert pluto tv channels into m3u format.", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-f', '--file', type=str, nargs=1, required=False, default=['nextpvr.m3u'], help='Full destination filepath. Default is nextpvr.m3u. Full file path can be specified. If only file name is specified then file will be placed in the current working directory.')
    parser.add_argument('-p', '--prefix', type=str, nargs=1, required=False, default=[''], help='Channel name prefix.')
    parser.add_argument('-s', '--startNumber', type=int, nargs=1, required=False, default=[1], help='Start numbering here. For example 9000. If -k, --keepNumber is used then channel 2 would become channel 9002, otherwise the first channel number found would be 9000, second channel found would be 9001, etc.')
    parser.add_argument('-k', '--keepNumber', action='store_true', required=False, help='Keep existing number scheme. Script will add existing number to start number. Recommended start number ends with a 0.')
    parser.add_argument('-i', '--ip', type=str, nargs=1, required=False, default=['127.0.0.1'], help='IP Address of NextPVR server. Default is 127.0.0.1')
    parser.add_argument('--port', type=int, nargs=1, required=False, default=[8866], help='Port number of NextPVR server. Default is 8866.')
    parser.add_argument('--pin', type=str, nargs=1, required=False, default=['0000'], help='Pin used to access NextPVR api. Default is 0000.')
    parser.add_argument('--streamlink', action='store_true', required=False, help='Generate the stream urls for use with Streamlink.')
    opts = parser.parse_args()
    
    #string agruments
    destination = quote_remover(opts.file[0])
    prefix = quote_remover(opts.prefix[0])
    ip = quote_remover(opts.ip[0])
    pin = quote_remover(opts.pin[0])
    
    #integer arguments
    startNumber = opts.startNumber[0]
    port = opts.port[0]
    
    #bool arguments
    keepNumber = opts.keepNumber
    streamlink = opts.streamlink

    #blank variables to get later
    sid = ''
    
    #dictionary arrays to build
    channel_dict = {'data': []}
    
    page = sidLogin5()
    method = 'channel.list'
    ret, grid = doRequest5(method)
    
    newNumber = startNumber
    #print(len(grid))
    #print(grid)
    x = 0
    for key in grid['channels']:
        if keepNumber == False:
            newNumber =+ x
        elif keepNumber == True:
            newNumber = startNumber + float(grid['channels'][x]['channelNumberFormated'])
            '''#removing these because no duplicates should be possible in next pvr, unlike pluto.tv
            r = 0
            index = 0
            while r < len(channel_numbers):
                if str(newNumber) == str(channel_numbers[r][0]):
                    index = r
                    s = len(channel_numbers[r])
                    channel_numbers[r].append(str(newNumber) + '.' + str(s))
                    print('Added sub channel: ' + channel_numbers[r][-1])
                    newNumber = channel_numbers[r][-1]
                    break
                r += 1
            if index == 0:
                channel_numbers.append([str(newNumber)])
                print('Added channel: ' + str(channel_numbers[-1][0]))

        #print(channel_numbers)
        '''
        channel_dict['data'].append({
            'channelName': grid['channels'][x]['channelName'], #name
            'channelNumber': grid['channels'][x]['channelNumber'], #channel number
            'channelMinor': grid['channels'][x]['channelMinor'], #channel number minor
            'channelNumberFormated': grid['channels'][x]['channelNumberFormated'], #channel number formated
            'channelId': grid['channels'][x]['channelId'], #id
            'channelType': grid['channels'][x]['channelType'], #type? 1 = OTA
            'channelDetails': grid['channels'][x]['channelDetails'], #details... frequency, tuner id, stream type
            'channelIcon': grid['channels'][x]['channelIcon'], #icon... true/false... true if icon exists
            'newNumber': newNumber })
        x += 1
    
    # remove duplicates
    channel_list = [i for n, i in enumerate(channel_dict['data']) if i not in channel_dict['data'][n + 1:]]
    print('Channels Found: ' + str(len(channel_list)+1))
    
    # sort by channel number (Ascending order)
    channel_list.sort(key=get_number) #https://www.programiz.com/python-programming/methods/list/sort#:~:text=%20Python%20List%20sort%20%28%29%20%201%20sort,an%20optional%20argument.%20Setting%20reverse%20%3D...%20More%20
    #print(channel_list)

    url_base = "http://" + ip + ":" + str(port)
    url = url_base + '/service?method='

    if streamlink == True:
        url_prefix = 'httpstream://'
    else:
        url_prefix = ''
    
    #start the m3u file
    m3u = '#EXTM3U'

    x = 0
    while x < len(channel_list): #do this for each channel
        m3u += '\n#EXTINF:-1 tvg-ID="NextPVR.' + str(channel_list[x]['channelId'])
        m3u += '" CUID="' + str(channel_list[x]['channelId'])
        m3u += '" tvg-chno="' + str(channel_list[x]['newNumber'])
        m3u += '" tvg-name="' + prefix + channel_list[x]['channelNumberFormated'] + ' ' + channel_list[x]['channelName']
        if channel_list[x]['channelIcon'] == True:
            m3u += '" tvg-logo="' + url + 'channel.icon&channel_id=' + str(channel_list[x]['channelId'])
        m3u += '" group-title="NextPVR",' + prefix + channel_list[x]['channelNumberFormated'] + ' ' + channel_list[x]['channelName']
        
        m3u += '\n' + url_prefix + url_base + '/live?channel_id=' + str(channel_list[x]['channelId'])

        print(channel_list[x]['channelName'] + ' will be added to the m3u.' + str(x+1) + '/' + str(len(channel_list)))

        x += 1

    m3u += '\n'
    
    print('m3u is ready to write')
    #print(m3u)

    #write the file
    file_handle = open(destination, "w")
    print('m3u is being created')
    file_handle.write(m3u)
    print('m3u is being written')
    file_handle.close()
    print('m3u is being closed')

