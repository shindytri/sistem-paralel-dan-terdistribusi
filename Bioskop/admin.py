
# coding: utf-8

# In[ ]:


import xmlrpc.client
from os import system

# buat stub (proxy) untuk client
s = xmlrpc.client.ServerProxy('http://192.168.43.40:1803')

#Menambah film dengan harga > 0 dan jumlah tiket >= 1
def addMovie():
    cls()
    print('Tambah film')
    title = input('Masukkan judul: ')
    price = -1
    ticket_count = -1
    print()
    while price < 0:
        price = int(input('Harga: '))
    while ticket_count < 1:
        ticket_count = int(input('Jumlah tiket: '))
    s.add_movie(title, price, ticket_count)

#Mengubah harga dengan menulis judulnya    
def updatePrice():
    cls()
    print('Perbarui harga tiket\n')
    movies = s.movie_list()
    prices = s.ticket_price()
    print('Daftar film:')
    for i in range(len(movies)):
        print('{}: {}'.format(movies[i], prices[i]))
    title = ''
    print()
    while title not in movies:
        title = input('Pilih judul: ')
    price = -1
    while price < 0:
        price = int(input('Harga: '))
    s.update_ticket_price(title, price)

#Menghapus film berdasarkan judul film
def removeMovie():
    print('Daftar film:\n')
    movies = s.movie_list()
    for i in range(len(movies)):
        print('{}'.format(movies[i]))
    print()
    title = ''
    while title not in movies:
        title = input('Pilih judul: ')
    s.remove_movie(title)

#Daftar menu yang bisa dilakukan client-admin
actions = [
    {
        'name': 'Tambah film',
        'callback': addMovie
    },
    {
        'name': 'Perbarui harga tiket',
        'callback': updatePrice
    },
    {
        'name': 'Hapus film',
        'callback': removeMovie
    }
]

#Membersihkan layar
def cls():
    system('clear')

#Memilih aksi untuk menu
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

