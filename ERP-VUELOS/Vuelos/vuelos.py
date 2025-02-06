import customtkinter as ctk
import requests
from datetime import datetime

class VuelosSeccion:
    def __init__(self, parent):
        self.parent = parent
    
    def avisoVuelo(self, numero_vuelo, fecha_vuelo):
        api_key = "bf04807e05ccba8776180a2b456e5011"  # Reemplaza con tu clave de API
        url = "http://api.aviationstack.com/v1/flights"
        
        params = {
            'access_key': api_key,  # La clave debe estar bien configurada
            'flight_iata': numero_vuelo,  # Número de vuelo
            'flight_date': fecha_vuelo  # Fecha del vuelo (en formato YYYY-MM-DD)
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()

            # Verificar si la respuesta contiene la estructura esperada
            if 'data' in data and len(data['data']) > 0:
                vuelo = data['data'][0]

                # Extraer la información deseada
                numero_vuelo = vuelo['flight']['iata']
                aerolinea = vuelo['airline']['name']
                origen = vuelo['departure']['airport']
                destino = vuelo['arrival']['airport']
                fecha_salida = vuelo['departure']['estimated']
                fecha_salida_dt = datetime.fromisoformat(fecha_salida)
                puerta = vuelo['departure']['gate']
                terminal = vuelo['departure']['terminal']
                
                # Formatear el mensaje
                mensaje = (f"Tu vuelo {numero_vuelo} con la aerolínea {aerolinea}, "
                        f"desde {origen} hacia {destino} sale el {fecha_salida_dt.strftime('%d/%m/%Y a las %H:%M')}.")
                
                if puerta:
                    mensaje += f" La puerta de embarque es {puerta}."
                if terminal:
                    mensaje += f" El vuelo sale desde la terminal {terminal}."
                
                return mensaje
            else:
                return "No se encontraron datos para el vuelo."
        else:
            return f"Error en la solicitud: {response.status_code}, {response.text}"


    def render(self):
        # Agregar widgets para la sección de vuelos
        label = ctk.CTkLabel(self.parent, text="Sección de Vuelos", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(pady=20)
        add_button = ctk.CTkButton(self.parent, text="Buscar Vuelo", command=lambda:self.on_button_click(vuelo,fecha_vuelo))
        add_button.pack(pady=10)
        vuelo = ctk.CTkEntry(self.parent, placeholder_text="Ingrese el vuelo: ")
        vuelo.pack(pady=10)  
        # Crear un Label para mostrar los resultados
        self.result_label = ctk.CTkLabel(self.parent, text="Fecha de salida: ")
        self.result_label.pack(pady=10)
        fecha_vuelo = ctk.CTkEntry(self.parent, placeholder_text="Ingrese la fecha del vuelo: ")
        fecha_vuelo.pack(pady=10)  


    def on_button_click(self,vuelo,fecha_vuelo):
        numero_vuelo = vuelo.get()
        salida_vuelo = self.avisoVuelo(numero_vuelo,fecha_vuelo)
        self.result_label.configure(text=f"Fecha de salida: {salida_vuelo}")

