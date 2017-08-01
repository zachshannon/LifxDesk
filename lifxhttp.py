import requests
import json
import colorsys
import webcolors
from io import StringIO

def str_to_json(json_str):
    'Take a string, get a json object'
    io = StringIO(json_str)
    return json.load(io)
    
class LifxConnection:
    'Class that hides http nonsense for lifx'
   
    def __init__(self, api_token):
        self.api_token = api_token
        self.headers = {
            "Authorization": "Bearer %s" % self.api_token,
        }

    def _request_get(self, url):
        'Put request to lifx url, handles auth'
        response = requests.get(url, headers=self.headers)
        return response

    def _request_put(self, url, payload):
        'Put request to lifx url, handles auth'
        response = requests.put(url, data=payload, headers=self.headers)
        return response

    def _request_post(self, url):
        response = requests.post(url, headers=self.headers)
        return response

    def get_lightable_by_selector(self, selector):
        'Return list containing all bulbs'
        lights_all = self._request_get('https://api.lifx.com/v1/lights/' + selector)
        data = str_to_json(lights_all.text)
        return Lightable(selector, self)

class Color:
    'Class to represent colors and translate'

    def __init__(self):
        self.hue = 0.0
        self.saturation = 0.0
        self.brightness = 0.0
        self.kelvin = 0.0

    def set_from_hex(self, hex_str):
        rgb_val = webcolors.hex_to_rgb(hex_str)
        hsv_val = colorsys.rgb_to_hsv(rgb_val[0], rgb_val[1], rgb_val[2])
        self.hue = hsv_val[0] * 360
        self.saturation = hsv_val[1]
        self.brightness = hsv_val[2] / 255

    def set_from_rgb(self, r, g, b):
        hsv_val = colorsys.rgb_to_hsv(r,g,b)
        self.hue = hsv_val[0] * 360
        self.saturation = hsv_val[1]
        self.brightness = hsv_val[2] / 255
        
    def set_from_hsv(self, h, s, v):
        self.hue = h
        self.saturation = s
        self.brightness = v

    def set_brightness(self, b):
        self.brightness = b
        
    def set_hue(self, h):
        self.hue = h

    def set_saturation(self, s):
        self.saturation = s

class Lightable:
    'Class to represent a generic light unit'

    def __init__(self, selector, con):
        self.con = con
        self.selector = selector 
        
    def _send_payload(self, payload):
        return self.con._request_put('https://api.lifx.com/v1/lights/' + self.selector + '/state', payload)

    def toggle(self):
        'Toggles power state of lightable'
        self.con._request_post('https://api.lifx.com/v1/lights/' + self.selector + '/toggle')

    def set_color(self, color, duration):
       'Sets color - using html hex code'
       my_color = ('hue:' + str(int(color.hue))
                            + ' saturation:'
                            + str(color.saturation)
                            + ' brightness:'
                            + str(color.brightness))
       payload = {
           'power' : 'on',
           'color' : my_color,
       }
       response = self._send_payload(payload)

    def set_brightness(self, new_brightness, duration):
        'Sets brightness - 0.0 to 1.0'
        payload = {
           'brightness': new_brightness,
           'duration' : duration,
        }
        self._send_payload(payload)
        self.brightness = new_brightness
        
