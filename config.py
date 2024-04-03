#  ___ ____      _
# |_ _|  _ \    / \
#  | || |_) |  / _ \
#  | ||  _ <  / ___ \
# |___|_| \_\/_/   \_\

wifi_ssid = "area3001"
wifi_password  = "hackerspace"

pixel_count = 16
pinOutNumber = 14

enable_debugging = False
heardbeat_interval = 30 # seconden

device_id = "0006"
device_name = "ESP von Kris"
device_hardware = "IRA"
device_version = "2024.3"

natsServer = "nats://demo.nats.io:4222"

# URL of the version file and the new main.py on the server
VERSION_URL = 'http://ira.makerspace-baasrode.be/version.txt'
UPDATE_URL = 'http://ira.makerspace-baasrode.be/main.py'

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
# nats-pub -s nats://demo.nats.io:4222 area3001.ira.default.output 'flash_firmware 2024.5'