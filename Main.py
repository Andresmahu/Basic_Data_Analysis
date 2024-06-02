# Importar la clase Tk de la biblioteca tkinter
from tkinter import Tk

from Storage.CsvWriter import CsvUpdater
# Importar el módulo GeneratorView que contiene la interfaz gráfica
from Views import GeneratorView
def main():
    # Crear una instancia de la clase Tk para la ventana principal
    ventana = Tk()
    # Configurar el título de la ventana principal
    ventana.wm_title("Registro de Datos en MySQL")
    # Configurar el color de fondo de la ventana principal
    ventana.config(bg='gray22')
    # Configurar las dimensiones de la ventana principal (ancho x alto)
    ventana.geometry('900x530')
    # Bloquear el cambio de tamaño de la ventana principal
    ventana.resizable(0, 0)
    # Crear una instancia de la clase Registro del módulo GeneratorView, pasando la ventana principal como argumento
    app = GeneratorView.Registro(ventana)
    # Iniciar el bucle principal de la aplicación
    app.mainloop()
    # Llamar a la función CsvWriter para escribir los datos en formato CSV, pasando el DataFrame de la aplicación como argumento
    csv_updater = CsvUpdater(app.df)
    csv_updater.update_csvs()

# Verificar si este archivo es el punto de entrada principal del programa
if __name__ == "__main__":
    # Llamar a la función main() para iniciar la aplicación
    main()
