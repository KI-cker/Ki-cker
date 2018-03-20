#!/usr/bin/env bash

v4l2-ctl -d /dev/video1 --set-ctrl focus_auto=0
v4l2-ctl -d /dev/video1 --set-ctrl power_line_frequency=1
v4l2-ctl -d /dev/video1 --set-ctrl backlight_compensation=0
v4l2-ctl -d /dev/video1 --set-ctrl exposure_auto_priority=1
