# ESPHome AXP192 Component
ESPHome AXP192 Component

This custom component it to implement support for the AXP192 for both the M5Stick-C, and the M5Stack Core2, building on top of airy10's code. 

*Update - 24th January 2024*  

@jdrago (work in progress)
	- Fixed reset of display on power up for M5Stack Core2 AWS (as CORE2).
	- Need to separate out Core2 AWS from Core 2.  Some hardware is different.
	- Added support for the vibrator motor.
	- Added support for Powering off.
	- More to come...

*Update - 17th April 2023*  

@paulchilton has added support for the M5Tough, which requires a different register configuration for the M5Tough ILI9342C display. Other changes include a fix to stop the log being spammed with brightness values continually, these are only logged on change. Also the M5Tough needs resetting once the axp192 registers are set for the display to properly initialise so this version sets up the axp and then resets the ESP32 automatically.

## Installation

Copy the components to a custom_components directory next to your .yaml configuration file, or include directly from this repository.

## Configuration

Sample configurations are found in the `/sample-config` folder.

This component adds a new model configuration to the AXP192 sensor which determines which registers are needed for each device. Available models are `model: M5CORE2`, `model: M5STICKC` and `model: M5TOUGH`.

### Include axp192 component

```yaml
external_components:
  - source: github://martydingo/esphome-axp192
    components: [axp192]
```

### M5Stick-C

```yaml
sensor:
  - platform: axp192
    model: M5STICKC
    address: 0x34
    i2c_id: bus_a
    update_interval: 30s
    battery_level:
      name: "M5Stick Battery Level"
      id: "m5stick_batterylevel"
```

### M5Stack Core2

```yaml
sensor:
  - platform: axp192
    model: M5CORE2
    address: 0x34
    i2c_id: bus_a
    update_interval: 30s
    battery_level:
      name: "${upper_devicename} Battery Level"
      id: "${devicename}_batterylevel"
```

### M5Tough

```yaml
sensor:
  - platform: axp192
    model: M5Tough
    address: 0x34
    i2c_id: bus_a
    update_interval: 30s
    battery_level:
      name: "${upper_devicename} Battery Level"
      id: "${devicename}_batterylevel"
```

The display component required for the M5Tough is as follows:

```yaml
display:
  - platform: ili9341
    # 320x240
    model: M5STACK
    cs_pin: GPIO5
    dc_pin: GPIO15
    lambda: |-
      it.print(160, 0, id(title_font), id(color_white), TextAlign::TOP_CENTER, "Hello World");
```
