from header import *

# สร้าง API สำหรับแปลงสี RGB เป็น HSL
# https://www.rapidtables.com/convert/color/rgb-to-hsl.html
def rgb_to_hsl(red:float,green:float,blue:float):
    r = red/255; g = green/255; b = blue/255
    cmin = min(r,g,b); cmax = max(r,g,b); d = cmax-cmin
    if cmax == 0 or d == 0: h = 0
    elif r == cmax: h = 60*((g-b)%6)/d
    elif g == cmax: h = 60*(2+(b-r)/d)
    elif b == cmax: h = 60*(4+(r-g)/d)
    l = (cmax+cmin)/2
    if d==0: s = 0
    else: s = d/(1-abs(2*l-1))
    return {"hue": h, "saturation": s, "lightness": l}
@app.get("/rgb2hsl/{red}/{green}/{blue}/")
def rgb2hsl(red:float,green:float,blue:float):
    hsl = rgb_to_hsl(red,green,blue)
    return {"hue": hsl['hue'], "saturation": hsl['saturation'], "lightness": hsl['lightness']}

# สร้าง API สำหรับแปลงสี HSL เป็น RGB
# https://www.rapidtables.com/convert/color/hsl-to-rgb.html
def hsl_to_rgb(hue:float,saturation:float,lightness:float):
    h, s, l = hue, saturation, lightness
    c = (1-abs(2*l-1))*s
    x = c*(1-abs(((h/60)%2)-1))
    m = l-c/2
    if 0<=h<60: r,g,b = c,x,0.
    elif 60<=h<120: r,g,b = x,c,0
    elif 120<=h<180: r,g,b = 0,c,x
    elif 180<=h<240: r,g,b = 0,x,c
    elif 240<=h<300: r,g,b = x,0,c
    elif 300<=h<360: r,g,b = c,0,x
    red = (r+m)*255
    green = (g+m)*255
    blue = (b+m)*255
    return {"red": red, "green": green, "blue": blue}
@app.get("/hsl2rgb/{hue}/{saturation}/{lightness}/")
def hsl2rgb(hue:float,saturation:float,lightness:float):
    rgb = hsl_to_rgb(hue,saturation,lightness)
    return {"red": rgb['red'], "green": rgb['green'], "blue": rgb['blue']}

# สร้าง API สำหรับแปลงสี RGB เป็น HSV
# https://www.rapidtables.com/convert/color/rgb-to-hsv.html
def rgb_to_hsv(red:float,green:float,blue:float):
    r = red/255; g = green/255; b = blue/255
    cmin = min(r,g,b); cmax = max(r,g,b); d = cmax-cmin
    if cmax == 0 or d == 0: h = 0
    elif r == cmax: h = 60*((g-b)%6)/d
    elif g == cmax: h = 60*(2+(b-r)/d)
    elif b == cmax: h = 60*(4+(r-g)/d)
    v = cmax/2
    if cmax==0: s = 0
    else: s = d/cmax
    return {"hue": h, "saturation": s, "value": v}
@app.get("/rgb2hsv/{red}/{green}/{blue}/")
def rgb2hsv(red:float,green:float,blue:float):
    hsv = rgb_to_hsv(red,green,blue)
    return {"hue": hsv['hue'], "saturation": hsv['saturation'], "value": hsv['value']}

# สร้าง API สำหรับแปลงสี HSV เป็น RGB
# https://www.rapidtables.com/convert/color/hsv-to-rgb.html
def hsv_to_rgb(hue:float,saturation:float,value:float):
    h, s, v = hue, saturation, value
    c = v*s
    x = c*(1-abs(((h/60)%2)-1))
    m = v-c
    if 0<=h<60: r,g,b = c,x,0.
    elif 60<=h<120: r,g,b = x,c,0
    elif 120<=h<180: r,g,b = 0,c,x
    elif 180<=h<240: r,g,b = 0,x,c
    elif 240<=h<300: r,g,b = x,0,c
    elif 300<=h<360: r,g,b = c,0,x
    red = (r+m)*255
    green = (g+m)*255
    blue = (b+m)*255
    return {"red": red, "green": green, "blue": blue}
@app.get("/hsv2rgb/{hue}/{saturation}/{value}/")
def hsv2rgb(hue:float,saturation:float,value:float):
    rgb = hsv_to_rgb(hue,saturation,value)
    return {"red": rgb['red'], "green": rgb['green'], "blue": rgb['blue']}


# สร้าง API สำหรับแปลงสี RGB เป็น CMYK
# https://www.rapidtables.com/convert/color/rgb-to-cmyk.html
def rgb_to_cmyk(red:float,green:float,blue:float):
    r = red/255; g = green/255; b = blue/255
    k = 1-max(r,g,b) # black
    c = (1-r-k)/(1-k)
    m = (1-g-k)/(1-k)
    y = (1-b-k)/(1-k)
    return {"cyan":c,"magenta":m,"yellow":y,"key":k}
@app.get("/rgb2cmyk/{red}/{green}/{blue}/")
def rgb2cmyk(red:float,green:float,blue:float):
    cmyk = rgb_to_cmyk(red,green,blue)
    return {"cyan":cmyk['cyan'],"magenta":cmyk['magenta'],"yellow":cmyk['yellow'],"key":cmyk['key']}

# สร้าง API สำหรับแปลงสี CMYK เป็น RGB
# https://www.rapidtables.com/convert/color/cmyk-to-rgb.html
def cmyk_to_rgb(cyan:float,magenta:float,yellow:float,key:float):
    c,m,y,k = cyan,magenta,yellow,key
    r = 255*(1-c)*(1-k)
    g = 255*(1-m)*(1-k)
    b = 255*(1-y)*(1-k)
    return {"red": r, "green": g, "blue": b}
@app.get("/cmyk2rgb/{cyan}/{magenta}/{yellow}/{key}/")
def cmyk2rgb(cyan:float,magenta:float,yellow:float,key:float):
    rgb = cmyk_to_rgb(cyan,magenta,yellow,key)
    return {"red": rgb['red'], "green": rgb['green'], "blue": rgb['blue']}

# api แปลงโหมดสี r,g,b [0-255] h[0-360] s,l,v,c,m,y,k [0-1]
@app.get('/convert-color-mode/{color_array}/{from_mode}/{to_mode}')
def convert_color_mode(color_array:str,from_mode:str,to_mode:str):
    color_array = json.loads(color_array)
    if from_mode == 'rgb' and to_mode == 'hsl':
        return rgb_to_hsl(*color_array)
    elif from_mode == 'rgb' and to_mode == 'hsv':
        return rgb_to_hsv(*color_array)
    elif from_mode == 'rgb' and to_mode == 'cmyk':
        return rgb_to_cmyk(*color_array)
    elif from_mode == 'hsl' and to_mode == 'rgb':
        return hsl_to_rgb(*color_array)
    elif from_mode == 'hsl' and to_mode == 'hsv':
        rgb = hsl_to_rgb(*color_array)
        return rgb_to_hsv(rgb['red'],rgb['green'],rgb['blue'])
    elif from_mode == 'hsl' and to_mode == 'cmyk':
        rgb=hsl_to_rgb(*color_array)
        return rgb_to_cmyk(rgb['red'],rgb['green'],rgb['blue'])
    elif from_mode == 'hsv' and to_mode == 'rgb':
        return hsv_to_rgb(*color_array)
    elif from_mode == 'hsv' and to_mode == 'hsl':
        rgb = hsv_to_rgb(*color_array)
        return rgb_to_hsl(rgb['red'],rgb['green'],rgb['blue'])
    elif from_mode == 'hsv' and to_mode == 'cmyk':
        rgb = hsv_to_rgb(*color_array)
        return rgb_to_cmyk(rgb['red'],rgb['green'],rgb['blue'])
    elif from_mode == 'cmyk' and to_mode == 'rgb':
        return cmyk_to_rgb(*color_array)
    elif from_mode == 'cmyk' and to_mode == 'hsl':
        rgb = cmyk_to_rgb(*color_array)
        return rgb_to_hsl(rgb['red'],rgb['green'],rgb['blue'])
    elif from_mode == 'cmyk' and to_mode == 'hsv':
        rgb = cmyk_to_rgb(*color_array)
        return rgb_to_hsv(rgb['red'],rgb['green'],rgb['blue'])