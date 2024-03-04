import sys

alphabet = '0123456789ABCDEFGHIJKLMNOPQTRSUVWXYZ-.'
# print('len(alphabet: %d'%(len(alphabet)))

if len(sys.argv) < 2 :
    raise RuntimeError('Usage: %s <base-38-string>'%(sys.argv[0]))

code = sys.argv[1]
if 'MT:' == code[:3]:
    code = code[3:]
length = len(code)
count5 = length // 5
lengthRemain = length % 5
if lengthRemain & 1 :
    raise RuntimeError('lengthRemain:%d'%(lengthRemain))

text = b''

def getCode(digit) :
    index = alphabet.find(digit)
    if index < 0 :
        raise RuntimeError('"%s" not in alphabet'%(digit))
    return index

def decode(code) :
    value = 0
    multiplier = 1
    for i in range(len(code)) :
        digit = code[i:][:1]
        value += multiplier * getCode(digit)
        multiplier *= 38
    #print('acc: 0x%x (code:%s)'%(value,code))
    if 5 == len(code) :
        digits = 3
    elif 4 == len(code) :
        digits = 2
    else :
        digits = 1
    reverse = '%%0%dx'%(digits<<1)%(value)
    forward = ''
    for i in range(digits) :
        forward += reverse[(digits-i-1)<<1:][:2]
    #print('forward: %s'%(forward))
    return forward
    return value.to_bytes(digits,'little')

substrings = []
for i in range(count5) :
    substrings.append(code[5*i:][:5])
if lengthRemain > 0 :
    substrings.append(code[5*count5:])
# print(substrings)

result = ''
for substring in substrings :
    result += decode(substring)

class Bitstream :
    def __init__(self,hexstr) :
        s = ''
        l = len(hexstr)
        if 1 & l :
            raise RuntimeError('odd length')
        l >>= 1
        for i in range(l) :
            s += hexstr[(l-i-1)<<1:][:2]
        self.bitsRemain = l << 3
        self.value = int(s,16)
    def get(self,bits) :
        mask = (1 << bits) - 1
        value = self.value & mask
        self.value >>= bits
        self.bitsRemain -= bits
        return value
    
print('decoded: %s'%(result))
s = Bitstream(result)
version = s.get(3)
vendorId = s.get(16)
productId = s.get(16)
customFlow = s.get(2)
discoveryCapabilities = s.get(8)
descriminator = s.get(12)
passcode = s.get(27)
padding = s.get(4)
if s.bitsRemain != 0 :
    raise RuntimeError('bitsRemain: %d'%(s.bitsRemain))

print('version:%d,\nvendorId:0x%04x,\nproductId:0x%04x,\ncustomFlow:%d,\ndiscoveryCapabilities:'%(version, vendorId, productId, customFlow))
if 1 & discoveryCapabilities :
    print('  Soft-AP')
if 2 & discoveryCapabilities :
    print('  BLE')
if 4 & discoveryCapabilities :
    print('  On IP network')
if 0xf8 & discoveryCapabilities :
    print('  Reserved bits set %08b'%(discoverCapabilities))
print('Descriminator: 0x%03x'%(descriminator))
comment = ''
if 0 == passcode or passcode > 99999998 :
    comment = '(Out of bounds)'
print('passcode: %d 0x%x %s'%(passcode, passcode, comment))
