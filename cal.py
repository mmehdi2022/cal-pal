import sys, datetime, pyperclip
from colorama import Fore, init
from sys import exit


init(convert=True)


def bin2text(binary:str) -> str:
    listed = [binary[i*8:i*8+8] for i in range(0, len(binary)//8)] if len(binary) % 8 == 0 else invalid_parameter_error()
    result = ''
    for i in listed:
        ascii_code = 0
        for _ in range(7, -1, -1):
            if i[7-_] == '1':
                ascii_code += 2**_
        result += chr(ascii_code)
    return result

def add2history(entry:str, result:str) -> None:
    with open('D:\programming\cmd_tools\history.txt', '+a') as file:
        file.write(f'entry:{entry} result:{result} date:{datetime.datetime.now()}\n')

def clear_history() -> None:
    file = open('D:\programming\cmd_tools\history.txt', 'w')
    file.close()

def view_history():
    with open('D:\programming\cmd_tools\history.txt', 'r') as file:
        for j,i in enumerate(file.readlines(), start=1):
            print(Fore.YELLOW+'-'*100 + Fore.RESET)
            print(f'{Fore.GREEN}[{j}]{Fore.RESET}')
            print(f'\tEntry: {Fore.GREEN}{i.split(' result')[0].split(':')[1]}{Fore.RESET}')
            print(f'\tResult: {Fore.GREEN}{i.split(' date')[0].split(':')[-1]}{Fore.RESET}')
            print(f'\tDate: {Fore.CYAN}{i.split('date:')[-1]}{Fore.RESET}')

def get_history_result(index:int) -> str:
    with open('D:\programming\cmd_tools\history.txt', 'r') as file:
        try:
            result = file.readlines()[index-1]
            result = result.split(' date')[0].split(':')[-1]
            pyperclip.copy(result)
            print(Fore.GREEN+ 'The result has been copied into clipboard.'+ Fore.RESET)
        except IndexError:
            print(Fore.RED+'The desired index doesn\'t exist.'+Fore.RESET)
            exit(1)

def num2bin(number:int) -> str:
    result = ''
    for i in range(7, -1, -1):
        if 2**i <= number:
            number -= 2**i
            result += '1'
        else:
            result += '0'
    return result


def text2bin(text:str) -> str:
    result = ''
    for i in text:
        result += num2bin(ord(i))
    
    return result


# create XOR, AND, OR, left shift and right shit and also number base convertor and bin to string


def invalid_parameter_error():
    print(Fore.RED+'invalid parameters\nUsage: calc [-opr \'operation\'] [-hi] [-clhi] [-hir] [-bin [binary]] [-text \'plain text\'] [-num [number]] [-rev]')
    print(Fore.RED+f'  -opr  -to type the operation inside \'\'.')
    print(Fore.RED+f'  -hi   -to view the history.')
    print(Fore.RED+f'  -clhi -to clear all the history.')
    print(Fore.RED+f'  -hir  -gets a result of a past operation and put in in clipboard.')
    print(Fore.RED+f'  -bin  -the binary value is optional but it is necessary when using -rev switch.')
    print(Fore.RED+f'  -text -need value when using -bin switch without -rev to make the text binary.')
    print(Fore.RED+f'  -num  -is needed when not using -text when using -bin without -rev.')
    print(Fore.RED+f'  -rev  -will reverse the text to binary operation and it needs the -bin switch to have a value.')
    exit(1)


# length error
if len(sys.argv) < 2:
    invalid_parameter_error()
    
    
# make them easy to find
for i in range(len(sys.argv)):
    if sys.argv[i] in ['-hi', '-hir', '-clhi', '-opr', '-bin', '-text', '-num', '-rev']:
        sys.argv[i] = sys.argv[i].lower()
    

# clear history
if '-clhi' in sys.argv:
    clear_history()
    exit(0)
    
# show history
if '-hi' in sys.argv:
    view_history()
    exit(0)

if '-hir' in sys.argv:
    try:
        index = sys.argv[sys.argv.index('-hir')+1]
        get_history_result(index=int(index))
        exit(0)
    except IndexError:
        invalid_parameter_error()


# the binary part
if '-bin' in sys.argv and not '-rev' in sys.argv:
    try:
        if '-text' in sys.argv:
            entry = sys.argv[sys.argv.index('-text')+1]
        elif '-num' in sys.argv:
            entry = int(sys.argv[sys.argv.index('-num')+1])
        else:
            invalid_parameter_error()
        result = bin(entry)[2:] if type(entry) == int else text2bin(entry)
        print(Fore.GREEN+ f'The bin value of {Fore.BLUE}\'{entry}\'{Fore.GREEN} is {result}'+Fore.RESET)
        add2history(entry=entry, result=result)
        exit(0)
    except IndexError:
        invalid_parameter_error()
    except:
        invalid_parameter_error()
    
# just operation
if '-opr' in sys.argv:
    try:
        entry = sys.argv[sys.argv.index('-opr')+1]
        result = eval(entry) if type(entry) == str else entry
        print(Fore.GREEN+ f'The result of {Fore.BLUE}\'{entry}\'{Fore.GREEN} is {result}'+Fore.RESET)
        add2history(entry=entry, result=result)
        exit(0)
    except IndexError:
        invalid_parameter_error()

# reverse the binary to string
if '-bin' in sys.argv and '-rev' in sys.argv:
    try:
        entry = sys.argv[sys.argv.index('-bin')+1]
        if type(entry) != str:
            invalid_parameter_error()
            
        result = bin2text(entry)
        print(Fore.GREEN+ f'The text value of {Fore.BLUE}\'{entry}\'{Fore.GREEN} is {result}'+Fore.RESET)
        add2history(entry=entry, result=result)
        exit(0)
        
    except IndexError:
        invalid_parameter_error()
elif '-rev' in sys.argv:
    invalid_parameter_error()







# -opr => the actual operation
# -hi => show history
# -hir => get the result of a specific history entry with it's index. it will be copied in clipboard cause I want ;)





