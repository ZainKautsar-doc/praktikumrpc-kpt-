from xmlrpc.server import SimpleXMLRPCServer

def tambah(a, b):
    return a + b

def kali(a, b):
    return a * b

def bagi(a, b):
    if b == 0:
        raise ValueError("Pembagian dengan nol")
    return a / b

if __name__ == "__main__":
    server = SimpleXMLRPCServer(("0.0.0.0", 8000), allow_none=True, logRequests=True)
    server.register_introspection_functions()
    server.register_function(tambah, "tambah")
    server.register_function(kali, "kali")
    server.register_function(bagi, "bagi")
    print("Server XML-RPC berjalan di port 8000...")
    server.serve_forever()
