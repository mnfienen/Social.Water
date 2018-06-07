# encode as string, decode as unicode bytes
def asciidammit(x):
    if type(x) is str:
        try:
            return x.decode('ascii')
        except:
            return x.decode('ascii', 'ignore')
    elif type(x) is str:
        try:
            s = x.encode('ascii')
            return s.decode('ascii')
        except:
            s = x.encode('ascii', 'ignore')
            return s.decode('ascii')
    else:
        x = str(x)
        return asciidammit(x)

def remove_punctuation(s):
    if s is None: return s
    s = s.replace(","," ").replace("."," ").replace("-"," ").replace(":"," ")
    return s

def validate_string(s):
    if s is None: return False
    try:
        if len(s) == 0: return False
    except:
        return False
    return True

def remove_cr(s):
    s = s.replace('\r', ' ')
    return s


def full_process(s):
    s = s.lower()
    s = s.strip()
    s = s.remove_cr(s)
    s = remove_punctuation(s)
    x = asciidammit(s)
    return x


def correct_subject(subject):
    return 'sms from' in subject.lower()


