import os, time

# Creamos la clase Cliente
class Cliente:
    
    # # Constructor de la clase
    def __init__(self): 
        
        # Definimos atributos de la clase
        self.cliente_id = os.getpid() # Obtenemos el id del proceso
        self.fifo_cliente = f'/tmp/respuesta_cliente_{self.cliente_id}' # Creamos la ruta hacia el FIFO del cliente
        self.fifo_servidor = '/tmp/tmp_servidor_fifo' # Creamos la ruta hacia el FIFO del servidor

        # Método para crear el FIFO del cliente
        self.crear_fifo(self.fifo_cliente)

    # Método que se encarga de verificar si existe la ruta hacia el FIFO, en caso de que no exista la crea
    def crear_fifo(self, path):
        if not os.path.exists(path):
            os.mkfifo(path)
    
    # Método para enviar mensaje al FIFO del servidor
    def enviar_mensaje(self, mensaje):
        with open(self.fifo_servidor, "w") as fifo:
            fifo.write(f"{self.cliente_id} {mensaje}")
        print(f"Mensaje enviado: {mensaje}")

    # Método para recibir las respuestas del servidor
    def recibir_respuesta(self):
        with open(self.fifo_cliente, "r") as fifo:
            respuesta = fifo.read()
            print(f"Respuesta: {respuesta}")

    # Método para iniciar el proceso
    def iniciar(self):
        while True:
            
            # Pedimos mensaje y enviamos
            mensaje = input("Ingrese mensaje para el servidor ('exit' para salir): ")
            self.enviar_mensaje(mensaje)

            # Si el mensaje es "exit" cerramos la conexión
            if mensaje == "exit":
                print("Cerrando cliente...")
                break

            time.sleep(1)
            self.recibir_respuesta()

        # Eliminamos el fifo del cliente
        os.remove(self.fifo_cliente)

if __name__ == "__main__":
    cliente = Cliente()
    cliente.iniciar()


