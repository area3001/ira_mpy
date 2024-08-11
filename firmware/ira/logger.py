import json


class Logger:
    def __init__(self, cfg, upl):
        self._cfg = cfg
        self._upl = upl

    async def log(self, level, message):
        if self._upl.is_connected():
            await self._upl.c.publish(
                'area3001.logs.{}.devices.{}'.format(self._cfg.get_device_group(), self._cfg.get_device_name()),
                json.dumps({"level": level, "message": message})
            )

        print("{} - {}".format(level, message))
