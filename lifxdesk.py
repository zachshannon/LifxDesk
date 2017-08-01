import json
from os.path import expanduser
import lifxhttp
import argparse

_home = expanduser("~")
_wal_color_file = _home + '/.cache/wal/colors.json'

def wal_color(num, data):
   return data["colors"]["color" + str(num)]

def set_from_wal(mytoken, colornum):
   #Open wal file.
   with open(_wal_color_file) as data_file:
      data = json.load(data_file)

   #Here is the color we are using (from wal)
   hex_color = wal_color(colornum, data)

   #And go
   lifxcon = lifxhttp.LifxConnection(mytoken)
   my_bulb = lifxcon.get_lightable_by_selector('label:My Room')
   my_color = lifxhttp.Color()
   my_color.set_from_hex(hex_color)
   my_bulb.set_color(my_color,2) #Using 2 sec duration

def main():
   parser = argparse.ArgumentParser(description='lifxdesk is a programm for setting the colour of your lights based on your desktop \o/')
   parser.add_argument('-t','--token', dest='token', action='store', required=True, help='The lifx token to use.')
   parser.add_argument('-w','--wal', dest='wal', action='store', help='Set colour from wal')
   args=parser.parse_args()

   #Set to wal.
   if args.wal is not None:
      set_from_wal(args.token, args.wal)

main()
