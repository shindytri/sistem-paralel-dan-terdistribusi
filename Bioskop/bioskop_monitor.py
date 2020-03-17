#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from os import system

# import paho mqtt
import paho.mqtt.client as mqtt

# import time for sleep()
from time import sleep
from os import system


# buat callback on_message; jika ada pesan
# maka fungsi ini akan dipanggil secara asynch
########################################
def on_message(client, userdata, message):
    # print pesan
    print(str(message.payload.decode("utf-8")))
    
########################################
    
# buat definisi nama broker yang akan digunakan
broker = '192.168.43.201'
port = 3333

# buat client baru bernama P1
print("creating new instance")
client = mqtt.Client('Bioskop Monitor')


# kaitkan callback on_message ke client
client.on_message=on_message


# buat koneksi ke broker
print("connecting to broker: shindy. publisher: vayu")
client.connect(broker, port=port)
print('Connected to broker: shindy')


system('clear')
# jalankan loop client
client.loop_start()


# client melakukan subsribe ke topik 4
client.subscribe('bioskop')

# loop forever
while True:
    # berikan waktu tunggu 1 detik 
    sleep(1)
    

#stop loop
client.loop_stop()

