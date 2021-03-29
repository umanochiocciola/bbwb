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

debug('initializing')

signature = '/* transpiled to python with BBWBC\n https://github.com/umanochiocciola/bbwb */\n'

init = '#include <stdio.h>\n#define CELLS ' + str(cells) + '\nint main() {\nint buff = 0; int tape[CELLS] = {0}; int ptr = 0;'

OUTPUT = signature + init

debug('creating references')

repls = {
    '+': 'buff++; if (buff>255) {buff = 0;}',
    '-': 'buff--; if (buff<0) {buff = 255;}',
    '#': 'buff = 0;',
    '^': 'tape[ptr] = buff;',
    'v': 'buff = tape[ptr];',
    '<': 'ptr++; if (ptr>=CELLS) ptr=0;',
    '>': 'ptr--; if (ptr<0) ptr = CELLS-1;',
    '.': 'printf("%d", buff);',
    ':': 'printf("%c", buff);',
    ',': 'scanf("%d", &buff);',
    ';': 'scanf("%c", &buff);',
    '[': 'while (tape[ptr]) {',
    ']': '}'
}

debug('compiling')


for ch in program:
    if not (ch in repls): continue
    OUTPUT += repls[ch] + '\n'

OUTPUT += 'return 0;}'

debug('writing to out.c')

with open('out.c', 'w') as f:
    f.write(OUTPUT)

debug('done!')
