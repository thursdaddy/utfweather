utfweather
=======

Configurable forecast module for Polybar.

### utfweather.conf
> ~/.config/utfweather/utfweather.conf
```
[general]
forecast_type = short
cache_ageout = 3600
use_geoloc = 0 
zipcode = 10001
```
###### Description:
``` 
cache_age:    time in seconds to update weather cache (5 minutes)
use_geoloc:   1 uses IP to get location, 0 to use zipcode
zipcode:      5 digit US Postal Code
```

### Polybar Config

####Add nerd-font to your bar configs, adjust size to your liking:
```
font-4 = "FuraMono Nerd Font Mono:style=Regular:pixelsize=22;2"
```
####Configure weather module:
```
[module/weather]
type = custom/script
interval = 1
exec = ~/.config/scripts/weather.py
click-left = ~/.config/scripts/weather.py -t
click-right = ~/.config/scripts/weather.py -n
```
###### Arguments:
```
-t : Toggles display between current forecast and detailed forecast
-n : Notification for 5 Day forecast sent via send-notify
```

## Requirements
* nerd-fonts-complete (UTF weather icons)
* Python 3.6 
* pip packages:
  * requests
  * zipcode
