import xmlrpc.client

def main():
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

    