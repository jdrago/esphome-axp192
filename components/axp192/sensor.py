import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import i2c, sensor
from esphome.const import CONF_ID,\
    CONF_BATTERY_LEVEL, CONF_BRIGHTNESS, UNIT_PERCENT, ICON_BATTERY, CONF_MODEL

CONF_VIBRATOR_MOTOR = 'vibrator_motor'
CONF_POWER_OFF = 'power_off'
CONF_RESET_DISPLAY = 'reset_display'
CONF_GREEN_LED = 'enable_green_led'

DEPENDENCIES = ['i2c']

axp192_ns = cg.esphome_ns.namespace('axp192')
AXP192Component = axp192_ns.class_('AXP192Component', cg.PollingComponent, i2c.I2CDevice)
AXP192Model = axp192_ns.enum("AXP192Model")

MODELS = {
    "M5CORE2": AXP192Model.AXP192_M5CORE2,
    "M5STICKC": AXP192Model.AXP192_M5STICKC,
    "M5TOUGH": AXP192Model.AXP192_M5TOUGH,
}

AXP192_MODEL = cv.enum(MODELS, upper=True, space="_")

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(AXP192Component),
    cv.Required(CONF_MODEL): AXP192_MODEL,
    cv.Optional(CONF_BATTERY_LEVEL):
        sensor.sensor_schema(
            unit_of_measurement=UNIT_PERCENT,
            accuracy_decimals=1,
            icon=ICON_BATTERY,
        ),
    cv.Optional(CONF_BRIGHTNESS, default=1.0): cv.percentage,
    cv.Optional(CONF_VIBRATOR_MOTOR, default=False): cv.boolean,
    cv.Optional(CONF_POWER_OFF, default=False): cv.boolean,
    cv.Optional(CONF_RESET_DISPLAY, default=True): cv.boolean,
    cv.Optional(CONF_GREEN_LED, default=True): cv.boolean,
}).extend(cv.polling_component_schema('60s')).extend(i2c.i2c_device_schema(0x77))

def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    yield cg.register_component(var, config)
    yield i2c.register_i2c_device(var, config)

    cg.add(var.set_model(config[CONF_MODEL]))
    if CONF_BATTERY_LEVEL in config:
        conf = config[CONF_BATTERY_LEVEL]
        sens = yield sensor.new_sensor(conf)
        cg.add(var.set_batterylevel_sensor(sens))

    if CONF_BRIGHTNESS in config:
        conf = config[CONF_BRIGHTNESS]
        cg.add(var.set_brightness(conf))

    if CONF_VIBRATOR_MOTOR in config:
        conf = config[CONF_VIBRATOR_MOTOR]
        cg.add(var.enable_vibrator_motor(conf))

    if CONF_POWER_OFF in config:
        conf = config[CONF_POWER_OFF]
        cg.add(var.force_power_off(conf))

    if CONF_RESET_DISPLAY in config:
        conf = config[CONF_RESET_DISPLAY]
        cg.add(var.reset_display(conf))

    if CONF_GREEN_LED in config:
        conf = config[CONF_GREEN_LED]
        cg.add(var.enable_green_led(conf))

