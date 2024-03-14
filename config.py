#  ___ ____      _
# |_ _|  _ \    / \
#  | || |_) |  / _ \
#  | ||  _ <  / ___ \
# |___|_| \_\/_/   \_\

wifi_ssid = "Nobelsoft"
wifi_password  = "potvolkoffie"

pixel_count = 4
pinOutNumber = 2

device_id = "0004"
device_name = "2e Badge von Kris"
device_hardware = "Badge"
device_version = "2024.1"

natsServer = "nats://demo.nats.io:4222"

# For MAC
# nats publish -s nats://demo.nats.io:4222 area3001.ira.default.output 'set_pixel 0 #ff0000'

# For Windows (Go) command
# nats-pub -s nats://demo.nats.io:4222 area3001.ira.default.output 'set_pixel 0 #ff0000'
# nats-pub -s nats://demo.nats.io:4222 area3001.ira.default.output 'clear_pixels'