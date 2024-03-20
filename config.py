#  ___ ____      _
# |_ _|  _ \    / \
#  | || |_) |  / _ \
#  | ||  _ <  / ___ \
# |___|_| \_\/_/   \_\

wifi_ssid = "area3001"
wifi_password  = "hackerspace"

pixel_count = 26
pinOutNumber = 2

enable_debugging = False

device_id = "0001"
device_name = "Daan"
device_hardware = "Badge"
device_version = "2024.2"

natsServer = "nats://demo.nats.io:4222"

# For MAC
# nats publish -s nats://demo.nats.io:4222 area3001.ira.default.output 'set_pixel 0 #ff0000'

# For Windows (Go) command
# nats-pub -s nats://demo.nats.io:4222 area3001.ira.default.output 'set_pixel 0 #ff0000'
# nats-pub -s nats://demo.nats.io:4222 area3001.ira.default.output 'clear_pixels'