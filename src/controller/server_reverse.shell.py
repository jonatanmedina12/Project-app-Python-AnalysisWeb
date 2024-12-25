import  socket

#Escuchando conexiones en todas las interfaces disponibles
server_ip ="0.0.0.0"

server_port =4242

server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server_socket.bind((server_ip,server_port))

#Escuchando conexiones

server_socket.listen(5)
print(f"Escuchando conexiones en {server_ip}:{server_port}.....")
#Aceptar conexiones entrantes

client_socket,client_address =server_socket.accept()
try:
    while True:
        # Solicitar al usuario el comando a ejecutar
        command = input("> ")+"\n"

        # Enviar el comando al cliente
        client_socket.send(command.encode())

        # Recibir y mostrar la respuesta

        response = client_socket.recv(1024)

        print(response.decode())


except KeyboardInterrupt:
    print("Cerrando conexion.")

finally:
    client_socket.close()
    server_socket.close()