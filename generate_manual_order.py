#! /usr/bin/env python
#
# Wolfinch Auto trading Bot
# Desc: Generate manual trading signal
#  Copyright: (c) 2017-2019 Joshith Rayaroth Koderi
#  This file is part of Wolfinch.
# 
#  Wolfinch is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
# 
#  Wolfinch is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with Wolfinch.  If not, see <https://www.gnu.org/licenses/>.

import json
import argparse
import os
import pprint
from decimal import *

getcontext().prec = 8 #decimal precision

######### ******** MAIN ****** #########
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate manual trading signal')
    # parser.add_argument('integers', metavar='N', type=int, nargs='+',
    #                    help='an integer for the accumulator')
    
    parser.add_argument('--exchange',  help='Exchange', required=True)
    parser.add_argument('--product',  help='Product', required=True)
    parser.add_argument('--size',  help='BUY in $USD | SELL BTC', required=True)
    parser.add_argument('type', choices =['BUY', 'SELL'], help='generate sell request')
    parser.add_argument('--limit', help='limit price', required=True, type=float)
    parser.add_argument('--stop', help='Post the order at specified (STOP) price', type=float )
    
    args = parser.parse_args()
    
    '''
            -- Manual Override file: "override/TRADE_<exchange_name>.<product>"
                Json format:
                {
                 product : <ETH-USD|BTC-USD>
                 side    : <BUY|SELL>
                 size    : <$USD|BTC>
                 type    : <limit|market>
                 price   : <limit-price>
                 stop  : <Post order At Price>
                }
    '''
    
    print (str(args))
    json_data = {}
    
    json_data['product'] = args.product
    json_data['price'] = args.limit
    json_data['stop'] = args.stop
    amount = 0.0
    json_data['type'] = ('stop' if (args.stop) else 'limit')
    if (args.type == 'BUY' ):
        json_data["side"] = 'BUY'
        #see if the size is in USD
        if (args.size[-1] != '$'):
            print ("ERROR: Please Specify Buy size in USD. (eg. 2000$)")
            exit()
        size = Decimal (args.size[:-1])
        size = round(Decimal(size)/Decimal(args.limit), 8)
        json_data['size'] = size
        if (args.stop and args.limit > args.stop):
            print ("ERROR: 'stop' price has to be higher than 'limit' for BUY")
            exit()
    else:
        json_data["side"] = 'SELL'
        json_data['size'] = Decimal(args.size)
        if (args.stop and args.limit < args.stop):
            print ("ERROR: 'stop' price has to be lower than 'limit' for SELL")
            exit()    
    
    print ("Order Being generated on Exchange: %s \n*****************\n %s"
          "\n****************\n"%( args.exchange, pprint.pformat(json_data, 4, 10)))
    
    yes = {'yes','y', 'ye'}
    
    print ("\nConfirm Order (yes/no):")
    choice = input().lower()
    if choice in yes:
        order_file_name = "override/TRADE_%s.%s"%(args.exchange, args.product)
        with open (order_file_name, "w") as fp:
            json.dump(json_data, fp)
        print ("Order Generated!")
    else:
        print ("Order Cancelled!\n")
    
#EOF
