#!/usr/bin/env python3
# coding: utf-8

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

    #argparse
    parser = argparse.ArgumentParser(description="Python script to convert m3u for use with streamlink.", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--inFile', type=str, nargs=1, required=False, default=['streamlink.m3u'], help='Full input file filepath. Full file path can be specified. If only file name is specified then file will be used from the current working directory if it exists.')
    parser.add_argument('-o', '--outFile', type=str, nargs=1, required=False, default=['streamlink.m3u'], help='Full destination filepath. Full file path can be specified. If only file name is specified then file will be placed in the current working directory.')
    parser.add_argument('-p', '--protocol', type=str, nargs=1, required=False, default=['httpstream://'], help='Stream url protocol.')
    opts = parser.parse_args()
    
    #string agruments
    destination = quote_remover(opts.outFile[0])
    input = quote_remover(opts.inFile[0])
    protocol = quote_remover(opts.protocol[0])
    
    
    if input.startswith('http'): #https://www.tutorialspoint.com/python/string_startswith.htm
        inputFile = requests.get(url=input).text #https://stackoverflow.com/a/1393367/11214013
        data = inputFile.split('\n')
        #print(len(data))
        x = 0
        while x < len(data):
            data[x] = data[x] + '\n'
            x += 1
    else:
        inputFile = open (input, 'r')
        print(type(inputFile))
        data = inputFile.readlines()
        inputFile.close()
        
    #start the m3u file
    m3u = ''
    
    #for line in data: #https://thispointer.com/5-different-ways-to-read-a-file-line-by-line-in-python/
    for line in data: #https://thispointer.com/5-different-ways-to-read-a-file-line-by-line-in-python/
        if line.startswith ('#'):
            m3u += line
        elif line.startswith ('\n'):
            pass
        elif line.startswith (protocol) != True:
            m3u += protocol + line
            print('Prepending stream: ' + line + ' ... with ' + protocol)
        else:
            m3u += line
            print('Stream already set to specified protocol')

    print('m3u is ready to write')
    #print(m3u)

    #write the file
    file_handle = open(destination, "w")
    print('m3u is being created')
    file_handle.write(m3u)
    print('m3u is being written')
    file_handle.close()
    print('m3u is being closed')

