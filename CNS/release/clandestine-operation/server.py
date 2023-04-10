#!/usr/sbin/python3
from cryptoFunc import *
from menus import *
import secret

JOB_TITLE = 'Grand Disciplinary Officer'
NAME = 'Cyno'

def choicePrompt():
    choice = input('Your choice: ').strip()
    try:
        choice = int(choice)
    except:
        choice = -1
    return choice

def genID():
    info = f'job title:{JOB_TITLE}||name:{NAME}||secret word:{secret.flag1}'.encode()
    return encrypt(info)

def printIDCard():
    ID = genID()
    print('Someone lost his ID card...')
    print('+' + '-'*51 + '+')
    print('| Job title: %s' % JOB_TITLE + ' '*13 + '|')
    print('| Name: %s' % NAME + ' '*40 + '|')
    print('| ID: %s |' % ID[0:45])
    print('| %s |' % ID[45:94])
    print('| %s |' % ID[94:143])
    print('| %s |' % ID[143:])
    print('+' + '-'*51 + '+')

def authenticate(ID):
    if True:
        info = decrypt(ID)
        # print('Analyzing info:', info)
        info = info.split('||')
        
        # print("info[0][:10]")
        # print("info[1][:5]")
        # print("info[2][:12]")
        # print("info[1][5:]")
        # import pdb
        # pdb.set_trace()
        # "['job title:Grand Disciplinary Officer', 'name:Cyno', 'secret word:CNS{IloveChihuahua_1?!}']"
        if len(info) != 3:
            raise formatError('Invalid format')

        if info[0][:10] != 'job title:':
            raise formatError('Job title field not found')
        
        if info[1][:5] != 'name:':
            raise formatError('Name field not found')

        if info[2][:12] != 'secret word:':
            raise formatError('Secret word field not found')
        

        if info[1][5:] == 'Azar':
            print('Welcome! The Grand Scholar. %s' % secret.flag2)
            return True
        else:
            print('Only Azar can enter!!!')
            return False
    else:
        print('Authentication failed')
        return False


if __name__ == '__main__':
    correctSecret = False
    printIDCard()

    while True:
        if not correctSecret:
            beforeEnterAkademiya()

            choice = choicePrompt()
            if choice == 1:
                secretWord = input('Please speak out the secret word: ').strip()
                if secretWord == secret.flag1:
                    correctSecret = True
                else:
                    print('Get out, stranger!')
            elif choice == 2:
                askNahida()
            elif choice == 3:
                print('( ´•̥̥̥ω•̥̥̥` )')
                break
            else:
                print('Invalid command')
        else:
            beforeEnterSurasthana()
            # print("PASS")
            choice = choicePrompt()
            if choice == 1:
                ID = input('Please enter your ID (hex encoded): ').strip()
                if authenticate(ID):
                    break
            elif choice == 2:
                askNahida()
            elif choice == 3:
                print('( ´•̥̥̥ω•̥̥̥` )')
                break
            else:
                print('Invalid command')
            
