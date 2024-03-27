#  ___ ____      _
# |_ _|  _ \    / \
#  | || |_) |  / _ \
#  | ||  _ <  / ___ \
# |___|_| \_\/_/   \_\

wifi_ssid = "area3001"
wifi_password  = "hackerspace"

pixel_count = 5
pinOutNumber = 2

enable_debugging = False
heardbeat_interval = 30 # seconden

device_id = "0004"
device_name = "2e Badge von Kris"
device_hardware = "Badge"
device_version = "2024.2"

natsServer = "nats://demo.nats.io:4222"

# For MAC
# nats publish -s nats://demo.nats.io:4222 area3001.ira.default.output 'set_pixel 0 #ff0000'

# For Windows
# install Go from https://go.dev/dl/
# In terminal change variable after install:
#   go env -w GO111MODULE=auto
# In terminal install packages
#   go get github.com/nats-io/go-nats-examples/tools/nats-pub
#   go get github.com/nats-io/go-nats-examples/tools/nats-sub

# From this point you can listen and send messages.
# nats-pub -s nats://demo.nats.io:4222 area3001.ira.default.output 'set_pixel 0 #ff0000'
# nats-pub -s nats://demo.nats.io:4222 area3001.ira.default.output 'clear_pixels'