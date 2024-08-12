"""
Proyecto Servidor en Linux - Sistemas Operativos
@authors: Araya Valentino, Conforti Angelo, Durán Faustino, Patiño Ignacio
Archivo del servidor 
"""

import os

# Creamos la clase Servidor
class Servidor:
    
    # Constructor de la clase
    def __init__(self):
        
        # Definimos atributos de la clase
        self.fifo_servidor = '/tmp/tmp_servidor_fifo' # Definimos la ruta del servidor como atributo de la clase
        # Palabras reservadas para procesaar
        self.palabras_reservadas = ["body", "header", "footer"]

        # Metodo para crear el FIFO del servidor
        self.crear_fifo(self.fifo_servidor)
        
    # Método que se encarga de verificar si existe la ruta hacia el FIFO, en caso de que no exista la crea
    def crear_fifo(self, path):
        if not os.path.exists(path):
            os.mkfifo(path)
            
    # Método que se encarga de leer el mensaje que envio el cliente
    def leer_msj(self):
        # Abre el archivo(FIFO) donde esta el mensaje del cliente
        with open(self.fifo_servidor, "r") as fifo:
            
            # Leemos el mensaje
            mensaje = fifo.read()
            
            # Divide el mensaje en 2 partes, la primer parte es el ID del cliente y la segunda parte es el mensaje
            partes = mensaje.split(' ', 1)

            # Verifica que el mensaje no contenga menos de 2 partes
            if len(partes) < 2:
                return None, None
            
            # Crea las variables que van a contener el ID y el mensaje del cliente
            id_cliente, contenido = partes[0], partes[1].lower()
            
            # Verifica que no usa la palabra clave "exit", en caso de que no la use envia la respuesta al cliente
            if contenido != "exit":
                if contenido in self.palabras_reservadas:
                    print(f"Mensaje del cliente {id_cliente}: {contenido} (Mensaje aceptado).")
                else:
                    print(f"Mensaje del cliente {id_cliente}: {contenido} (Mensaje rechazado).")
            return id_cliente, contenido
        
    # Método que se encarga de enviar la respuesta hacia el cliente
    def enviar_respuesta(self, id_cliente, respuesta):
        
        # Envía la respuesta al cliente usando su ID (Cada cliente tiene un FIFO diferente por el ID)
        fifo_cliente = f'/tmp/respuesta_cliente_{id_cliente}'
        
        # Verifica que el FIFO del cliente exista, en caso de que no exista lo crea
        if os.path.exists(fifo_cliente):
            
            # Abre el archivo y escribe el contenido de la respuesta del servidor  
            with open(fifo_cliente, 'w') as cliente_fifo:  
                cliente_fifo.write(respuesta)
                
    # Método que se encarga de iniciar el proceso
    def iniciar(self):
        while True:
            
            # Lee los mensajes de los clientes durante toda la ejecucuión
            id_cliente, mensaje = self.leer_msj()
            
            if id_cliente and mensaje:    
                # Si la palabra es "exit" cerramos la conexión
                if mensaje == "exit":
                    respuesta = "Cerrando conexión..."
                    print(f"{id_cliente} cerró sesión.")
                    self.enviar_respuesta(id_cliente, respuesta)
                    
                # Si el mensaje es una de las palabras claves definidas en los atributos de la clase enviamos una respuesta
                elif mensaje in self.palabras_reservadas:
                    respuesta = f"Mensaje '{mensaje}' recibido y procesado."
                
                # Si el mensaje no se encuentra en las palabras reservadar de la clase, enviamos "Mensaje no válido"
                else:
                    respuesta = "Mensaje no válido."
                    
                # Llama al método "enviar_respuesta" dandole los parametros necesarios (ID y Respuesta)
                self.enviar_respuesta(id_cliente, respuesta)

#PROGRAMA
if __name__ == "__main__":
    # Instanciamos la clase e iniciamos el proceso
    servidor = Servidor()
    servidor.iniciar()
