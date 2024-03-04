# Example Usage
<pre>
$ python3 qr-decode.py MT:4CT9142C00KA0648G00
decoded: 40f427004400e04b846802
version:0,
vendorId:0xfe88,
productId:0x8004,
customFlow:0,
discoveryCapabilities:
  BLE
Descriminator: 0xf00
passcode: 20202021 0x1344225 
</pre>

## Even more basic encoding:
<pre>
$ python3 qr-encode.py 40f427004400e04b846802
len(alphabet: 38
length: 11
['40f427', '004400', 'e04b84', '6802']
['4CT91', '42C00', 'KA064', '8G00']
</pre>