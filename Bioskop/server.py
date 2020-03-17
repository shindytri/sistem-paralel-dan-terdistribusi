# indirect communication
import paho.mqtt.client as mqtt
import socket
from time import sleep
import datetime

log = []

socketPort = 14045
socketBuffer 1024

_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# lakukan bind
_socket.bind((IP, PORT))

# server akan listen menunggu hingga ada koneksi dari client
_socket.listen(1)

conn, addr = _socket.accept()


for elem in log:
    msg += elem + '\n'

conn.send(msg)

# definisikan nama broker yang akan digunakan
broker = '192.168.43.201'
port = 3333

# buat client baru bernama P2
print("creating new instance")
client = mqtt.Client('Bioskop server')


# koneksi ke broker
print("connecting to broker")
client.connect(broker, port=port)
client.loop_start()

# RPC
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import threading

# Batasi hanya pada path /RPC2 saja supaya tidak bisa mengakses path lainnya
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

def publishHistory():
    msg = ''
    for elem in log:
        msg += elem + '\n'
    client.publish('bioskop', msg, 1)

# Buat server
with SimpleXMLRPCServer(("192.168.43.40", 1803),
                        requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    # buat data struktur dictionary untuk menampung nama_kandidat dan hasil voting
    data = {
                "Teman Tapi Menikah 2" : {
                    "price" : 50000,
                    "ticket_count" : 30,
                    "is_now_playing" : 1
                }, 
                "Mulan" : {
                    "price" : 35000,
                    "ticket_count" : 50,
                    "is_now_playing" : 1
                },
                "Avatar 2" : {
                    "price" : 35000,
                    "ticket_count" : 70,
                    "is_now_playing" : 1
                },
                "Sonic The Hedgehog" : {
                    "price" : 40000,
                    "ticket_count" : 40,
                    "is_now_playing" : 1
                },
                "Milea" : {
                    "price" : 35000,
                    "ticket_count" : 50,
                    "is_now_playing" : 1
                },
                "Titanic" : {
                    "price" : 70000,
                    "ticket_count" : 35,
                    "is_now_playing" : 1
                }
            }
    
    # kode setelah ini adalah critical section, menambahkan vote tidak boeh terjadi race condition
    # siapkan lock
    lock = threading.Lock()
    
    # Create

    def addMovie(title, price, ticket_count):
        # critical section dimulai
        lock.acquire()
        
        # tambah movie dengan key title
        data[title] = {
            'price': price,
            'ticket_count': ticket_count,
            'is_now_playing': True
        }
        
        # critical section berakhir
        lock.release()

        # siapkan return value
        msg = 'Movie added: {}'.format(title)
        global log
        log.append(msg)
        publishHistory()

        return True

    def order_movie_ticket(ticket_amount, movie_title):
        # critical section dimulai harus dilock
        lock.acquire()
        
        # validasi input
        if movie_title not in data:
            lock.release()
            return "Movie not found!"
        if (data[movie_title]['ticket_count'] < ticket_amount):
            lock.release()
            return "Too much"

        # proses pembelian
        data[movie_title]['ticket_count'] -= ticket_amount
        lock.release()

        # siapkan pesan untuk monitor
        msg = 'Movie ordered: {} for {} ticket'.format(movie_title, ticket_amount)
        global log
        log.append(msg)
        publishHistory()

        # return value
        return "Succesfully booked the ticket!"
    
    # Read
    def display_ticket_price():
        lock.acquire()

        # menyiapkan film
        now_playings = []
        for key in data:
            if data[key]['is_now_playing']:
                now_playings.append('Rp. {}'.format(data[key]['price']))

        lock.release()
        return now_playings

    def display_ticket_remaining():
        lock.acquire()

        # menyiapkan film
        tickets = [{
                'title': key,
                'amount': data[key]['ticket_count'],
                'price': data[key]['price']
            } for key in data]

        lock.release()

        return tickets

    def movieList():
        # critical section dimulai
        lock.acquire()
        
        # mengambil judul film
        titles = [key for key in data]
        
        # critical section berakhir
        lock.release()
        return titles

    # Update
    def change_ticket_price(movie_title, price):
        lock.acquire()

        # menyimpan variabel untuk monitor
        oldPrice = data[movie_title]['price']

        # mengupdate harga
        data[movie_title]['price'] = price
        lock.release()

        # mengirim pesan ke monitor
        msg = 'Ticket price changed: {} from Rp. {} to Rp. {}'.format(movie_title, oldPrice, price)
        global log
        log.append(msg)
        publishHistory()

        return True
    
    # Delete
    def removeMovie(title):
        # critical section dimulai
        lock.acquire()
        
        # menghapus film by key
        del data[title]
        
        # critical section berakhir
        lock.release()

        # mengirim pesan ke monitor
        msg = 'Movie removed: {}'.format(title)
        global log
        log.append(msg)
        publishHistory()

        return True
    
    # Create
    server.register_function(addMovie, 'add_movie')
    server.register_function(order_movie_ticket, 'order_ticket')

    # Read
    server.register_function(movieList, 'movie_list')
    server.register_function(display_ticket_price, 'ticket_price')
    server.register_function(display_ticket_remaining, 'remaining_ticket')
    
    # Update
    server.register_function(change_ticket_price, 'update_ticket_price')
    
    #Delete
    server.register_function(removeMovie, 'remove_movie')
    


    print ("Server bioskop berjalan...")
    # Jalankan server
    server.serve_forever()

client.loop_stop()