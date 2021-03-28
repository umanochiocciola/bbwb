from sys import argv

if len(argv) < 2:
    print("missing file argument"); exit(1)

try:
    with open(argv[1], 'r') as f:
        program = f.read()
except:
    print("no such file"); exit(1)

def debug(txt, typ='info'):
    print(f'[{typ}] {txt}')

try:
    cells = int(argv[2])
except:
    cells = 16
    debug('using deafult tape len (16) because not specified', 'note')

debug('-- BBWB Compiler started --')
debug('setting up')

signature = '# transpiled to python with BBWBC\n# LINK HERE\n'
init = f'tape = [0]*{cells}\nptr = 0\nbuff = 0\n'

OUTPUT = signature + init

debug('creating references')

repls = {
    '+': 'buff += 1',
    '-': 'buff -= 1',
    '#': 'buff = 0',
    '^': 'tape[ptr] = buff',
    'v': 'buff = tape[ptr]',
    '<': f'ptr = ptr-1 if ptr > 0 else {cells}',
    '>': f'ptr = ptr+1 if ptr+1 < {cells} else 0',
    '.': 'print(buff, end="")',
    ':': 'print(chr(buff), end="")',
    ',': 'buff = int(input("i> "))',
    ';': 'buff = ord(input("c> ")[0])',
    '[': 'while tape[ptr]:'
}

debug('compiling')

INDENT = ''
for ch in program:
    
    if ch == ']': INDENT = '    '*(INDENT.count('    ')-1)
    if not (ch in repls): continue
    
    OUTPUT += INDENT+repls[ch]+'\n'
    if ch == '[': INDENT += '    '
    


if INDENT != '':
    debug('last loops not closed, even if it works with python, it won\'t on other compilers', 'warning')

debug('writing to out.py')

with open('out.py', 'w') as f:
    f.write(OUTPUT)

debug('done!')
