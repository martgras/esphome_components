import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import climate, sensor
from .. import wavinAhc9000_ns, WavinAhc9000, CONF_WAVINAHC9000_ID
from esphome.const import (
    CONF_ID,
    CONF_CHANNEL,
    CONF_BATTERY_LEVEL,
    CONF_STATE_CLASS,
    UNIT_PERCENT,
    UNIT_CELSIUS,
    ICON_PERCENT,
    ICON_THERMOMETER,
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_TEMPERATURE,
)

AUTO_LOAD = ['sensor']

CONF_CURRENT_TEMP = "current_temp"
CONF_STATE_CLASS = "measurement"

WavinAhc9000Climate = wavinAhc9000_ns.class_('WavinAhc9000Climate', climate.Climate, cg.Component)
 
CONFIG_SCHEMA = climate.CLIMATE_SCHEMA.extend({
    cv.GenerateID(): cv.declare_id(WavinAhc9000Climate),
    cv.GenerateID(CONF_WAVINAHC9000_ID): cv.use_id(WavinAhc9000),
    cv.Required(CONF_CHANNEL): cv.int_range(min=1, max=16),
    cv.Optional(CONF_BATTERY_LEVEL): sensor.sensor_schema(UNIT_PERCENT, ICON_PERCENT, 0, DEVICE_CLASS_BATTERY),
    cv.Optional(CONF_CURRENT_TEMP): sensor.sensor_schema(UNIT_CELSIUS, ICON_THERMOMETER, 1, DEVICE_CLASS_TEMPERATURE, CONF_STATE_CLASS),
}).extend(cv.COMPONENT_SCHEMA)
 
def to_code(config):
    wavin = yield cg.get_variable(config[CONF_WAVINAHC9000_ID])
    var = cg.new_Pvariable(config[CONF_ID], wavin)
    yield cg.register_component(var, config)
    yield climate.register_climate(var, config)
 
    cg.add(var.set_channel(config[CONF_CHANNEL] - 1))
    if CONF_BATTERY_LEVEL in config:
        sens = yield sensor.new_sensor(config[CONF_BATTERY_LEVEL])
        cg.add(var.set_battery_level_sensor(sens))
    if CONF_CURRENT_TEMP in config:
        sens = yield sensor.new_sensor(config[CONF_CURRENT_TEMP])
        cg.add(var.set_current_temp_sensor(sens))
