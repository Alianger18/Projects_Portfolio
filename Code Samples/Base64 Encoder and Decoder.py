import base64

class b64() :
    def __init__(self) :
        return None
    def encode(string) :
        """
        Requires plain text as input, not some sort of other coded format.
        """
        result = str(base64.b64encode(string.encode()))
        return result[1:]
    def decode(string) :
        """
        Requires a base64 coded format as a string.
        """
        result = str(base64.b64decode(string))
        return result[1:]        

print(b64.encode("Ali loves Karima"))
print(b64.decode("QWxpIGxvdmVzIEthcmltYQ=="))
