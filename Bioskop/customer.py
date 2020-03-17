#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import xmlrpc.client
from os import system

# buat stub (proxy) untuk client
s = xmlrpc.client.ServerProxy('http://192.168.43.40:1803')

# beli tiket 
def buyTicket():
    cls()
    print('Beli tiket')
    # memanggil function remaining_ticket() pada server
    movies = s.remaining_ticket()
    print('Daftar film:')
    for elem in movies:
        # menampilkan judul film, sisa tiket, dan harga 
        print('{}: {}'.format(elem['title'], elem['amount']))
    print()
    title = ''
    while title not in [elem['title'] for elem in movies]:
        title = input('Pilih judul: ') # Pilih judul film yang ingin dibeli
    amount = int(input('Jumlah tiket: ')) # Masukkan jumlah tiket yang ingin dibeli
    print(s.order_ticket(amount, title)) # Memanggil function order_ticket pada server 

# menampilkan daftar film
def getMovies():
    cls()
    print('Judul film\n')
    for elem in s.movie_list(): # menampilkan setiap film pada function movie_list di server
        print(elem)

# menampilkan daftar harga ticket
def getPrice():
    cls()
    print('Harga tiket\n')
    # memanggil function movie_list
    movies = s.movie_list() 
    # memanggil function ticket price
    prices = s.ticket_price()
    for i in range(len(movies)):
        print('{}: {}'.format(movies[i], prices[i]))

def getAvailableTicket():
    cls()
    print('Tiket tersedia\n')
    movies = s.remaining_ticket()
    for elem in movies:
        print('{}: {}'.format(elem['title'], elem['amount']))

actions = [
    {
        'name': 'Beli tiket',
        'callback': buyTicket
    },
    {
        'name': 'Daftar film',
        'callback': getMovies
    },
    {
        'name': 'Daftar harga tiket',
        'callback': getPrice
    },
    {
        'name': 'Tiket tersedia',
        'callback': getAvailableTicket
    }
]

def cls():
    system('clear')

def action():
    print('Pilih aksi')
    for i in range(len(actions)):
        print('{}. {}'.format(i, actions[i]['name']))
    print('-1. Keluar')

    print()
    actionId = int(input('Aksi: '))
    return actionId

def main():
    actionId = action()
    while actionId != -1:
        print()
        actions[actionId]['callback']()
        print()
        print('OK! Tekan enter untuk melanjutkan')
        input()
        cls()       
        actionId = action()
    cls()
    print('Thankyou')

main()


# print(1)
# from os import system
# system('cls')
# print(2)
# system('clear')

# In[ ]:




