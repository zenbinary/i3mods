#!/bin/sh
# display brightness script
# author: lswest

display_brightness=$(cat /sys/class/backlight/acpi_video0/actual_brightness)
icon_name="1"

if [ "$icon_name" = "1" ]; then
    if [ "$display_brightness" = "0" ]; then
        icon_name="notification-display-brightness-off"
    else
        if [ "$display_brightness" -lt "5" ]; then
            icon_name="notification-display-brightness-low"
        else
            if [ "$display_brightness" -lt "10" ]; then
                icon_name="notification-display-brightness-medium"
            else
                if [ "$display_brightness" -lt "15" ]; then
                     icon_name="notification-display-brightness-high"
                else
                     icon_name="notification-display-brightness-full"
                fi
            fi
        fi
    fi
fi

display100=$(echo $display_brightness*6.67|bc) 
echo $display100

notify-send " " -i $icon_name -h int:value:$display100 -h string:synchronous:brightness
