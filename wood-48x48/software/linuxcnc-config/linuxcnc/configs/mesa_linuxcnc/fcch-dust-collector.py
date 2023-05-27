#!/usr/bin/env python2

import hal
import paho.mqtt.publish as publish
import time

mqtt_hostname = '10.1.10.156'
mqtt_port = 1883
mqtt_user = None
mqtt_pass = None
mqtt_client_id = 'FIXME'
mqtt_topic = 'stat/cnc-wood-48x48/STATE'

mqtt_auth = None
if mqtt_user is not None:
    mqtt_auth = {'username': mqtt_user, 'password': mqtt_pass}

h = hal.component("fcch-dust-collector")
h.newpin("ui-request", hal.HAL_BIT, hal.HAL_IN)
h.newpin("is-auto", hal.HAL_BIT, hal.HAL_IN)
h.newpin("rfid-present", hal.HAL_BIT, hal.HAL_IN)
h.ready()

val_last_publish = None
time_last_publish = time.time()
try:
    while True:
        val_now = (h['ui-request'] or h['is-auto']) and h['rfid-present']
        time_since_last_publish = time.time() - time_last_publish
        if val_now != val_last_publish or time_since_last_publish > 10:
            if val_now:
                msg = 'ON'
            else:
                msg = 'OFF'
            publish.single(
                mqtt_topic,
                msg,
                qos = 0,
                retain = False,
                hostname = mqtt_hostname,
                port = mqtt_port,
                client_id = mqtt_client_id,
                keepalive = 60,
                will = None,
                auth = mqtt_auth,
                tls = None)
            time_last_publish = time.time()
        time.sleep(1)
except KeyboardInterrupt:
    raise SystemExit
