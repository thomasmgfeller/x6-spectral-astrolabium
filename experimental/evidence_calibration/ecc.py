"""Educational Hamming(7,4) single-error-correcting reference; NOT GF-651."""
def encode_hamming74(data):
    if len(data)!=4 or any(type(b) is not int or b not in (0,1) for b in data):
        raise ValueError("four binary bits required")
    a,b,c,d=data
    return [a^b^d,a^c^d,a,b^c^d,b,c,d]

def decode_hamming74(word):
    if len(word)!=7 or any(type(b) is not int or b not in (0,1) for b in word):
        raise ValueError("seven binary bits required")
    bits=list(word)
    syndrome=sum(1<<i for i in range(3) if sum(bits[j] for j in range(7) if (j+1)&(1<<i))%2)
    if syndrome: bits[syndrome-1]^=1
    return {"data":[bits[i] for i in (2,4,5,6)],"syndrome":syndrome,
            "status":"CORRECTED_OR_UNDETECTED_MULTI_ERROR" if syndrome else "NO_SYNDROME"}

def exhaustive_single_error_check():
    count=0
    for v in range(16):
        data=[(v>>i)&1 for i in (3,2,1,0)]
        word=encode_hamming74(data)
        for pos in range(8):
            corrupted=word.copy()
            if pos<7: corrupted[pos]^=1
            if decode_hamming74(corrupted)["data"]!=data:
                return {"passed":False,"cases":count}
            count+=1
    return {"passed":True,"cases":count,"scope":"zero and single-bit errors only"}
