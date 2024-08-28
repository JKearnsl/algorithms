# Hamming Coder

In computer science and telecommunication, Hamming codes are a family of linear 
error-correcting codes. Hamming codes can detect one-bit and two-bit errors, 
or correct one-bit errors without detection of uncorrected errors. 
By contrast, the simple parity code cannot correct errors, and can detect only an odd number of 
bits in error. Hamming codes are perfect codes, that is, they achieve the highest possible rate 
for codes with their block length and minimum distance of three.

Richard W. Hamming invented Hamming codes in 1950 as a way of automatically correcting errors 
introduced by punched card readers. In his [original paper](https://calhoun.nps.edu/server/api/core/bitstreams/0d21de63-5f08-4f42-899d-7ccb9b07980f/content), 
Hamming elaborated his general idea, but specifically focused on the Hamming(7,4) code 
which adds three parity bits to four bits of data.

### Encoding

https://github.com/JKearnsl/HammingCoder/blob/1e8a5f7362ff3808bf504ce91cde813116e8b495/src/core/hamming.py#L10-L70


### Decoding

https://github.com/JKearnsl/HammingCoder/blob/1e8a5f7362ff3808bf504ce91cde813116e8b495/src/core/hamming.py#L73-L143