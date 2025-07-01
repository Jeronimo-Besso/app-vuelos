# ✈️ Flight Manager App

Una aplicación de escritorio para la gestión integral de vuelos, pasajeros y finanzas, diseñada con `customtkinter` y `SQLite`. Permite registrar clientes, agendar vuelos, controlar pagos, finalizar tramos y visualizar estadísticas en tiempo real.

---

## 📦 Características Principales

- **Gestión de Clientes**
  - Alta, edición y eliminación de clientes.
  - Estadísticas en vivo (clientes totales, recientes, del último mes).
  - Buscador por nombre, apellido, DNI o teléfono.

- **Gestión de Vuelos**
  - Registro de vuelos con detalles completos (origen, destino, horarios, aerolínea, aeropuertos, pasajero, etc.).
  - Estado de pago con checkbox interactivo.
  - Finalización de vuelos (mueve el vuelo al historial y lo sincroniza con el dashboard financiero).

- **Historial de Vuelos**
  - Visualización filtrada por cliente.
  - Datos completos del tramo finalizado.

- **Dashboard Financiero**
  - Vuelos activos, ventas brutas y comisión calculada automáticamente.
  - Ajuste dinámico del porcentaje de comisión.
  - Detección de vuelos pendientes de cobro.

---

## 🧱 Tecnologías Usadas

- **Frontend**: [customtkinter](https://github.com/TomSchimansky/CustomTkinter)
- **Backend**: Python 3 + SQLite3
- **Extras**:
  - `tkcalendar` para selección de fechas
  - `CTkMessagebox` para diálogos amigables

---

## 🛠️ Estructura General

