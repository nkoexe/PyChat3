from os.path import dirname, join
from socket import socket
from traceback import print_tb


def update(index=-1):
    versionlist = currentversion.split('.')
    changing = versionlist[index]

    if changing.isdigit():
        versionlist[index] = str(int(changing) + 1)

    else:
        try:
            changing = changing.split()[0]
            newlast = str(int(changing) + 1)
            versionlist[index] = versionlist[-1].replace(changing, newlast, 1)
        except ValueError:
            print('Could not update version automatically.')

    return '.'.join(versionlist)


print('''
                   _                                    _                                             _ _  
                  | |            _                     | |        _                                  | | | 
 ____  _   _  ____| |__  _____ _| |_    _   _ ____   __| |_____ _| |_ _____    _____ ____   ____ ___ | | | 
|  _ \| | | |/ ___)  _ \(____ (_   _)  | | | |  _ \ / _  (____ (_   _) ___ |  | ___ |  _ \ / ___) _ \| | | 
| |_| | |_| ( (___| | | / ___ | | |_   | |_| | |_| ( (_| / ___ | | |_| ____|  | ____| | | | |  | |_| | | | 
|  __/ \__  |\____)_| |_\_____|  \__)  |____/|  __/ \____\_____|  \__)_____)  |_____)_| |_|_|   \___/ \_)_)
|_|   (____/                                 |_|                                                           
''')

filepath = join(dirname(dirname(__file__)), 'data', 'version')
currentversion = open(filepath, 'r').read()

newversion = update()

if newversion == currentversion:
    newversion = input('Inserire manualmente la nuova versione:\n> ')

else:
    print('\t\t\t\t', currentversion, '   >>   ', newversion)
    print('\nPremere <invio> per aggiornare automaticamente alla'
          'nuova versione, altrimenti inserirla manualmente:')
    inp = input('> ').strip()

    if inp:
        newversion = inp


open(filepath, 'w').write(newversion)

s = socket(2, 1)
try:
    s.connect(('localhost', 24839))
    s.send(b'}}}}')
    s.send(newversion.encode())
    print('Successo.')
except:
    print('\nErrore nella connessione al server.')
