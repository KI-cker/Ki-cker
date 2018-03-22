#!/usr/bin/env bash

v4l2-ctl -d /dev/video1 -p 30 --set-ctrl focus_auto=0,brightness=128,power_line_frequency=1,backlight_compensation=0,exposure_auto_priority=1
