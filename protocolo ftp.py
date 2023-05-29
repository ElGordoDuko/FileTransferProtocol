import socket

class FTPClient:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def send_command(self, command):
        self.socket.sendall(command.encode("ascii"))

    def sv_respon(self):
        response = ""
        while True:
            data = self.socket.recv(1024)
            if not data:
                break
            response += data.decode("ascii")
        return response

    def login(self, username, password):
        self.send_command("USER " + username)
        response = self.sv_respon()
        if response[0] != "2":
            raise Exception("Login failed: " + response)

        self.send_command("PASS " + password)
        response = self.sv_respon()
        if response[0] != "2":
            raise Exception("Login failed: " + response)

    def list_directory(self):
        self.send_command("LIST")
        response = self.sv_respon()
        if response[0] != "1":
            raise Exception("Listing directory failed: " + response)

        lines = response.splitlines()
        for line in lines:
            print(line)

    def descargar(self, filename):
        self.send_command("RETR " + filename)
        response = self.sv_respon()
        if response[0] != "1":
            raise Exception("Downloading file failed: " + response)

        with open(filename, "wb") as f:
            while True:
                data = self.socket.recv(1024)
                if not data:
                    break
                f.write(data)

    def subir(self, filename):
        self.send_command("STOR " + filename)
        response = self.sv_respon()
        if response[0] != "1":
            raise Exception("Uploading file failed: " + response)

        with open(filename, "rb") as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                self.socket.sendall(data)

if __name__ == "__main__":
    client = FTPClient("localhost", 21)
    client.login("user", "password")
    client.list_directory()
    client.descargar("file.txt")
    client.subir("file.txt")
    client.close()
