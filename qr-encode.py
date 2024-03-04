import sys

alphabet = '0123456789ABCDEFGHIJKLMNOPQTRSUVWXYZ-.'
print('len(alphabet: %d'%(len(alphabet)))

if len(sys.argv) < 2 :
    raise RuntimeError('Usage: %s <byte-string>'%(sys.argv[0]))

text = sys.argv[1]
if len(text) & 1 :
    raise RuntimeError('Two hex digits per byte')

length = len(text) >> 1
count3 = length // 3
lengthRemain = length % 3

chunks = []
for i in range(count3) :
    chunks.append(text[6*i:][:6])
if lengthRemain > 0 :
    chunks.append(text[6*count3:])

print('length: %d'%(length))
print(chunks)

substrings = []
for chunk in chunks :
    value = 0
    for i in range(len(chunk)>>1) :
        shift = i << 3
        value |= (int(chunk[i<<1:][:2],16) << shift)
    if 6 == len(chunk) :
        digits = 5
    elif 4 == len(chunk) :
        digits = 4
    else :
        digits = 2
    substring = ''
    for i in range(digits) :
        index = value % 38
        value //= 38
        #print(index,value)
        substring += alphabet[index]
    substrings.append(substring)

print(substrings)
quit()

