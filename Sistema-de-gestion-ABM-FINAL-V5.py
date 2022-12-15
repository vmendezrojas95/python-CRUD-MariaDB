import time
import mariadb
import sys
import os
from datetime import date
import pandas as pd # pip install pandas
from sqlalchemy import create_engine # Necesario para usar pandas con MaridaDB
# pip install pymysql , necesario para poder usar sqlalchemy y consecuentemente pandas

miConexion = mariadb.connect(host="localhost", user="root", passwd="4488", autocommit=True)
cursor = miConexion.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS Sistema_La_Criolla")
#miConexion.close()
#engine = create_engine("mariadb+pymysql:///?User=root&;Password=4488&Database=videoClub&Host=localhost&Port=3306")
#engine = create_engine("mysql+pymysql://user:pass@some_mariadb/dbname?charset=utf8mb4")
#def ocultar_contrasena():
 #   import getpass
  #  return getpass.getpass()
#engine = create_engine("mysql+pymysql://root:"+ocultar_contrasena()+"@localhost/Sistema_La_Criolla?charset=utf8mb4")

#print(engine)
#df = pd.read_sql("SELECT * FROM clientes", engine)
#print(df)

miConexion = mariadb.connect(host="localhost", user="root", passwd="4488", db="Sistema_La_Criolla")
cursor = miConexion.cursor()
#now = datetime.datetime.now()
#formatted_date = now.strftime()
cursor.execute("CREATE TABLE IF NOT EXISTS Proveedores(DNI VARCHAR(20) PRIMARY KEY, Nombre_Fantasia VARCHAR(50), Direccion VARCHAR(50), Telefono VARCHAR(20), Mail VARCHAR(50), Situacion_IVA VARCHAR(50))")
cursor.execute("CREATE TABLE IF NOT EXISTS Clientes(DNI VARCHAR(20) PRIMARY KEY, Apellido_Nombre VARCHAR(50), Direccion VARCHAR(50), Telefono VARCHAR(20), Mail VARCHAR(50), Situacion_IVA VARCHAR(50))")
cursor.execute("CREATE TABLE IF NOT EXISTS Articulos(Codigo_Barra VARCHAR(20) PRIMARY KEY, Nombre VARCHAR(50), Rubro VARCHAR(50), Precio FLOAT, Precio_Proveedor FLOAT, Stock INT, DNI_Proveedor VARCHAR(50), Estado VARCHAR(50))")
cursor.execute("CREATE TABLE IF NOT EXISTS Remitos(Codigo_Barra VARCHAR(20) PRIMARY KEY, Cantidad INT, DNI_Proveedor VARCHAR(20), Fecha DATE, Rubro VARCHAR(50), Precio FLOAT, Stock INT) ")
cursor.execute("CREATE TABLE IF NOT EXISTS Ventas(Codigo_Barra VARCHAR(20) PRIMARY KEY, Cantidad INT, DNI_Cliente VARCHAR(20), Productos VARCHAR(100), Fecha DATE, Cantitad INT, Monto FLOAT)")
#cursor.execute ("CREATE TABLE IF NOT EXISTS Pedidos_Reposicion (Codigo_Barra VARCHAR(20), Nombre VARCHAR(20), Rubro VARCHAR(20), Precio VARCHAR(20), Stock VARCHAR(20), DNI_Proveedor VARCHAR(20), Fecha_Pedido DATE)")
cursor.execute("CREATE TABLE IF NOT EXISTS Pedido_Reposicion(Codigo_Barra VARCHAR(20) PRIMARY KEY, DNI_Proveedor VARCHAR(20), Fecha DATE, Rubro VARCHAR(50), Precio FLOAT, Stock INT)")
"""

  ARMADO DE LA CLASE CLIENTE
"""
#############################################################################################################################
class Cliente():
    miConexion = mariadb.connect(host="localhost", user="root", passwd="4488", db="Sistema_La_Criolla")
    cursor = miConexion.cursor()

    def __init__(self, dni, apellido_Nombre, direccion, telefono, mail, situacionIVA):
        self.dni = dni
        self.apellido_Nombre = apellido_Nombre
        self.direccion = direccion
        self.telefono = telefono
        self.mail = mail
        self.situacionIVA = situacionIVA
        #opc = 0
    def menu(self):
        os.system("cls")
        opc = int(input("""Bienvenido al Menu Cliente, que Desea hacer?: 
         1- Alta
         2- Baja
         3- Modificacion 
         4- Listar
         5- Consumidor Final 
         6- Salir
        """))
        if opc == 1:
            print("Datos existentes en la tabla: ")
            engine = create_engine("mariadb+pymysql://root:4488@localhost/Sistema_La_Criolla?charset=utf8mb4")
            df = pd.read_sql_query("SELECT * FROM Clientes", engine)
            if df.empty:
                print("No hay datos en la tabla")
                print("Ingrese los datos del cliente: ")
            else:
                print(df)
            
            #cursor = miConexion.cursor()
            self.dni = input("Ingrese el DNI: ")
            # Comprobar que el DNI no exista
            cursor.execute("SELECT * FROM Clientes WHERE DNI = %s", (self.dni,))
            if cursor.fetchone() is not None:
                print("El DNI ya existe")
                return Cliente.menu(self)

            self.apellido_Nombre = input("Ingrese el Nombre y Apellido: ")
            self.direccion = input("Ingrese la Direccion: ")
            self.telefono = input("Ingrese el Telefono: ")
            self.mail = input("Ingrese el Mail: ")
            self.situacionIVA = input("Ingrese la Situacion IVA: 1-Responsable Inscripto 2-Responsable no Inscripto 3-Exento 4-No Responsable \n")
            if self.situacionIVA == "1":
                self.situacionIVA = "Responsable Inscripto"
            elif self.situacionIVA == "2":
                self.situacionIVA = "Responsable no Inscripto"
            elif self.situacionIVA == "3":
                self.situacionIVA = "Exento"
            elif self.situacionIVA == "4":
                self.situacionIVA = "No Responsable"
            else:
                print("Situacion IVA no valida")
                return Cliente.menu(self)
            cursor.execute ( "INSERT INTO Clientes (DNI, Apellido_Nombre, Direccion, Telefono, Mail, Situacion_IVA) VALUES (%s, %s, %s, %s, %s, %s)", (self.dni, self.apellido_Nombre, self.direccion, self.telefono, self.mail, self.situacionIVA))
            miConexion.commit()
            print("Cliente Agregado , Base de Datos actualizada")
            time.sleep(2)
            print("Nuevos Datos existentes en la tabla: ")
            #engine = create_engine("mariadb+pymysql://root:4488@localhost/Sistema_La_Criolla?charset=utf8mb4")
            df = pd.read_sql_query("SELECT * FROM Clientes", engine)
            print(df)
            os.system("pause")
            os.system("cls")
            Cliente.menu(self)
        elif opc == 2:
            print("Datos existentes en la tabla: ")
            engine = create_engine("mariadb+pymysql://root:4488@localhost/Sistema_La_Criolla?charset=utf8mb4")
            df = pd.read_sql_query("SELECT * FROM Clientes", engine)
            if df.empty:
                print("No hay datos en la tabla")
            else:
                print(df)
            self.dni = input("Ingrese el DNI del cliente a Eliminar: ")
            cursor.execute("DELETE FROM Clientes WHERE DNI = %s", (self.dni,))
            miConexion.commit()
            print("Cliente Eliminado, Base de Datos actualizada")
            time.sleep(2)
            print("#################")
            print("Nuevos Datos existentes en la tabla: ")
            df = pd.read_sql_query("SELECT * FROM Clientes", engine)
            print(df)
            os.system("pause")
            os.system("cls")
            Cliente.menu(self)
        elif opc == 3:
            print("Datos existentes en la tabla que puede modificar: ")
            engine = create_engine("mariadb+pymysql://root:4488@localhost/Sistema_La_Criolla?charset=utf8mb4")
            df = pd.read_sql_query("SELECT * FROM Clientes", engine)
            print(df)
            print(" ###############")
            self.dni = input("Ingrese el DNI del cliente a Modificar: ")
            self.apellido_Nombre = input("Ingrese el Apellido y Nombre: ")
            self.direccion = input("Ingrese la Direccion: ")
            self.telefono = input("Ingrese el Telefono: ")
            self.mail = input("Ingrese el Mail: ")
            self.situacionIVA = input("Ingrese la Situacion IVA: ")
            cursor.execute("UPDATE Clientes SET Apellido_Nombre = %s, Direccion = %s, Telefono = %s, Mail = %s, Situacion_IVA = %s WHERE DNI = %s", (self.apellido_Nombre, self.direccion, self.telefono, self.mail, self.situacionIVA, self.dni))
            miConexion.commit()
            print("Cliente Modificado, Base de Datos actualizada")
            time.sleep(2)
            print("Nuevos Datos existentes en la tabla: ")
            df = pd.read_sql_query("SELECT * FROM Clientes", engine)
            print(df)
            os.system("pause")
            os.system("cls")
            Cliente.menu(self)
        elif opc == 4:
            #cursor.execute("SELECT * FROM Clientes")
            #resultado = cursor.fetchall()
            # usar dataframe para mostrar los datos
            #engine = create_engine("mariadb+pymysql://root:"+ocultar_contrasena()+"@localhost/Sistema_La_Criolla?charset=utf8mb4")
            # crear engine con contraseña puesta en ocultar_contrasena()
            
            engine = create_engine("mariadb+pymysql://root:4488@localhost/Sistema_La_Criolla?charset=utf8mb4")
            df = pd.read_sql_query("SELECT * FROM Clientes", engine)
            print(df)
            #for i in resultado:
             #   print(i)
            
            os.system("pause")
            os.system("cls")
            MenuPrincipal()                    
        elif opc == 5:
            self.dni = int(input("Ingrese el DNI del cliente - Consumidor Final: "))
            self.apellido_Nombre = "Consumidor Final"
            self.direccion = " "
            self.telefono = " "
            self.mail = " "
            self.situacionIVA = "Consumidor Final"
            cursor.execute ( "INSERT INTO Clientes (DNI, Apellido_Nombre, Direccion, Telefono, Mail, Situacion_IVA) VALUES (%s, %s, %s, %s, %s, %s)", (self.dni, self.apellido_Nombre, self.direccion, self.telefono, self.mail, self.situacionIVA))
            miConexion.commit()
            print("Cliente Agregado")
            os.system("pause")
            os.system("cls")
            MenuPrincipal()
        elif opc == 6:
            print("Gracias por utilizar la Gestion de Clientes")
            os.system("pause")
            os.system("cls")
            MenuPrincipal()
            
        else:
            print("Opcion Incorrecta")
            os.system("pause")
            os.system("cls")
            Cliente.menu(self)
           
        """
        FIN CLASE CLIENTE
        """
#############################################################################################################################
#############################################################################################################################

"""
    ARMADO DE LA CLASE Articulo
"""
#############################################################################################################################
#############################################################################################################################
class Articulo:
    def __init__(self, codigoBarra, nombre, rubro, precio, stock, dniProveedor):
        self.codigoBarra = codigoBarra
        self.nombre = nombre
        self.rubro = rubro
        self.precio = precio
        self.stock = stock
        self.dniProveedor = dniProveedor
       # opc = 0
    def menu(self):
        os.system("cls")
        opc = int(input("""
        Bienvenido al Menu Articulo, que Desea hacer?: 
        1- Alta 
        2- Baja 
        3- Modificacion
        4- Listar 
        5- Listar articulos sin Stock 
        6- Ingreso de Remito 
        7- Salir 
        """
        ))
        if opc == 1:
            print("Datos existentes en la tabla: Articulos ")
            engine = create_engine("mariadb+pymysql://root:4488@localhost/Sistema_La_Criolla?charset=utf8mb4")
            df = pd.read_sql_query("SELECT * FROM Articulos", engine)
            print(df)
            print(" ###############")
            self.codigoBarra = input("Ingrese el Codigo de Barra: ")
            # Consulta para verificar si el Codigo de Barra ya existe
            cursor.execute("SELECT * FROM Articulos WHERE Codigo_Barra = %s", (self.codigoBarra,))
            resultado = cursor.fetchall()
            if resultado:
                print("El Codigo de Barra ya existe")
                os.system("pause")
                os.system("cls")
                Articulo.menu(self)
            self.nombre = input("Ingrese el Nombre: ")
            self.rubro = input("Ingrese el Rubro: ")
            self.precio = input("Ingrese el Precio: ")
            precio2 = input("Ingrese el Precio del Proveedor: ")
            self.stock = input("Ingrese el Stock: ")
            engine = create_engine("mariadb+pymysql://root:4488@localhost/Sistema_La_Criolla?charset=utf8mb4")
            df = pd.read_sql_query("SELECT * FROM Proveedores", engine)
            print(df)
            print(" ###############")
            print("Proveedores existentes en la tabla: ")
            self.dniProveedor = input("Ingrese el DNI del Proveedor: ")
            cursor.execute ("INSERT INTO Articulos (Codigo_Barra, Nombre, Rubro, Precio,Precio_Proveedor, Stock, DNI_Proveedor) VALUES (%s, %s, %s, %s, %s, %s, %s)", (self.codigoBarra, self.nombre, self.rubro, self.precio, precio2,self.stock, self.dniProveedor))
            miConexion.commit()
            print("Articulo Agregado, Base de Datos actualizada")
            time.sleep(2)
            print("Nuevos Datos existentes en la tabla: ")
            df = pd.read_sql_query("SELECT * FROM Articulos", engine)
            print(df)
            os.system("pause")
            os.system("cls")
            Articulo.menu(self)
        elif opc == 2:
            print("Datos existentes en la tabla: ")
            engine = create_engine("mariadb+pymysql://root:4488@localhost/Sistema_La_Criolla?charset=utf8mb4")
            df = pd.read_sql_query("SELECT * FROM Articulos", engine)
            print(df)
            print(" ###############")
            self.codigoBarra = input("Ingrese el Codigo de Barra del Articulo a Eliminar: ")
            # verificar si el Codigo de Barra existe
            cursor.execute("SELECT * FROM Articulos WHERE Codigo_Barra = %s", (self.codigoBarra,))
            resultado = cursor.fetchall()
            if resultado:
                cursor.execute("DELETE FROM Articulos WHERE Codigo_Barra = %s", (self.codigoBarra,))
                miConexion.commit()
                print("Articulo Eliminado, Base de Datos actualizada")
                time.sleep(2)
                print("Nuevos Datos existentes en la tabla: ")
                df = pd.read_sql_query("SELECT * FROM Articulos", engine)
                print(df)
                os.system("pause")
                os.system("cls")
                Articulo.menu(self)
            else:
                print("El Codigo de Barra no existe")
                os.system("pause")
                os.system("cls")
                Articulo.menu(self)
        elif opc == 3:
            print("Datos existentes en la tabla: ")
            engine = create_engine("mariadb+pymysql://root:4488@localhost/Sistema_La_Criolla?charset=utf8mb4")
            df = pd.read_sql_query("SELECT * FROM Articulos", engine)
            print(df)
            print(" ###############")
            self.codigoBarra = input("Ingrese el Codigo de Barra del Articulo a Modificar: ")
            # consultar si el Codigo de Barra existe
            cursor.execute("SELECT * FROM articulos WHERE Codigo_Barra = %s", (self.codigoBarra,))
            resultado = cursor.fetchall()
            if resultado:
                self.nombre = input("Ingrese el Nombre: ")
                self.rubro = input("Ingrese el Rubro: ")
                self.precio = input("Ingrese el Precio: ")
                self.stock = input("Ingrese el Stock: ")
                engine = create_engine("mariadb+pymysql://root:4488@localhost/Sistema_La_Criolla?charset=utf8mb4")
                df = pd.read_sql_query("SELECT * FROM Proveedores", engine)
                print(" ")
                print(" Proveedores Disponibles :")
                print(df)
                print("  ")
                self.dniProveedor = input("Ingrese el DNI del Proveedor: ")
                cursor.execute ("UPDATE articulos SET Nombre = %s, Rubro = %s, Precio = %s, Stock = %s, DNI_Proveedor = %s WHERE Codigo_Barra = %s", (self.nombre, self.rubro, self.precio, self.stock, self.dniProveedor, self.codigoBarra))
                miConexion.commit()
                print("Articulo Modificado, Base de Datos actualizada")
                time.sleep(2)
                print("Nuevos Datos existentes en la tabla: ")
                df = pd.read_sql_query("SELECT * FROM Articulos", engine)
                print(df)
                os.system("pause")
                os.system("cls")
                Articulo.menu(self)
            else:
                print("El Codigo de Barra no existe")
                os.system("pause")
                os.system("cls")
                Articulo.menu(self)
        elif opc == 4:
            print("Datos existentes en la tabla: ")
            engine = create_engine("mariadb+pymysql://root:4488@localhost/Sistema_La_Criolla?charset=utf8mb4")
            df = pd.read_sql_query("SELECT * FROM Articulos", engine)
            print(df)
            #cursor.execute("SELECT * FROM articulos")
            #resultado = cursor.fetchall()
            #for i in resultado:
             #   print(i)

            os.system("pause")
            os.system("cls")
            Articulo.menu(self)    
        elif opc == 5:
            cursor.execute("SELECT * FROM Articulos WHERE Stock = 0")
            resultado = cursor.fetchall()
            for i in resultado:
                print(i)
            os.system("pause")
            os.system("cls")
            Articulo.menu(self)
        elif opc == 6:
            os.system("cls")
            # Revisamos que no tenga ningun pedido pendiente en la tabla Pedido_reposicion
            print("Revisando que no tenga pendiente ninguna Orden de Reposicion: Cargando......")
            time.sleep(3)
            engine = create_engine("mariadb+pymysql://root:4488@localhost/Sistema_La_Criolla?charset=utf8mb4")
            df = pd.read_sql_query("SELECT * FROM Pedido_reposicion", engine)
            if df.empty:
                print("No hay Ordenes de Reposicion pendientes")
                opc2 = input("Desea Generar una Orden de Reposicion? 1-Si 2-No: ")
                if opc2 == 1:
                    print("Generando Orden de Reposicion")
                    time.sleep(2)
                    os.system("cls")
                    print("Sistema de Creacion de Remitos")
                    self.codigoBarra = input("Ingrese el Codigo de Barra del Articulo: ")
                    self.cantidad = int(input("Ingrese la Cantidad: "))
                    self.dniProveedor = input("Ingrese el DNI del Proveedor: ")
                    self.fecha = date.today()
                    self.rubro = input("Ingrese el Rubro: ")
                    self.precio = input("Ingrese el Precio: ")
                    self.stock = input("Ingrese el Stock: ")
                    os.system("cls")
                    os.system("pause")
                    print("Los datos del Remito son: ")
                    print("Codigo de Barra: ", self.codigoBarra)
                    print("Cantidad: ", self.cantidad)
                    print("DNI del Proveedor: ", self.dniProveedor)
                    print("Fecha: ", self.fecha)
                    print("Rubro: ", self.rubro)
                    print("Precio: ", self.precio)
                    print("Stock: ", self.stock)
                    opc3 = input("Desea Confirmar el Remito? 1-Si 2-No: ")
                    if opc3 == 1:
                        cursor.execute("INSERT INTO Remitos (Codigo_Barra, Cantidad, DNI_Proveedor, Fecha, Rubro, Precio, Stock) VALUES (%s, %s, %s, %s, %s, %s, %s)", (self.codigoBarra, self.cantidad, self.dniProveedor, self.fecha, self.rubro, self.precio, self.stock))
                        miConexion.commit()
                        # Actualizamos el Stock del Articulo
                        cursor.execute("UPDATE articulos SET Stock = Stock - %s WHERE Codigo_Barra = %s", (self.cantidad, self.codigoBarra))
                        miConexion.commit()
                        print("Remito Confirmado, Productos actualizados")
                        os.system("pause")
                        os.system("cls")
                        Articulo.menu(self)
                    else:
                        print("Remito no Confirmado")
                        os.system("pause")
                        os.system("cls")
                        Articulo.menu(self)
                    #print("Orden de Reposicion Generada")
                    #os.system("pause")
                    #os.system("cls")
                    #Articulo.menu(self)
                elif opc2 == 2:
                    os.system("cls")
                    Articulo.menu(self)
                os.system("pause")
                os.system("cls")
                Articulo.menu(self)
            else:
                print("Hay Ordenes de Reposicion pendientes")
                print(df)
                # Si los datos son correctos, se crea el remito para actualizar el stock
                opc2 = int(input("Los datos , son correctos? 1-Si 2-No: "))
                #opc2 = input("")
                if opc2 == 1:
                    print("Generando Orden de Reposicion")
                    time.sleep(2)
                    os.system("cls")
                    print("Sistema de Creacion de Remitos")
                    print("El Sitema cuenta con una version obsoleta, por favor pase los datos manualmente: ")
                    print(df)
                    self.codigoBarra = input("Ingrese el Codigo de Barra del Articulo: ")
                    self.cantidad = int(input("Ingrese la Cantidad: "))
                    self.dniProveedor = input("Ingrese el DNI del Proveedor: ")
                    self.fecha = date.today()
                    self.rubro = input("Ingrese el Rubro: ")
                    self.precio = input("Ingrese el Precio: ")
                    self.stock = input("Ingrese el Stock: ")
                    os.system("cls")
                    os.system("pause")
                    print("Los datos del Remito son: ")
                    print("Codigo de Barra: ", self.codigoBarra)
                    print("Cantidad: ", self.cantidad)
                    print("DNI del Proveedor: ", self.dniProveedor)
                    print("Fecha: ", self.fecha)
                    print("Rubro: ", self.rubro)
                    print("Precio: ", self.precio)
                    print("Stock: ", self.stock)
                    opc3 = int(input("Desea Confirmar el Remito? 1-Si 2-No: "))
                    if opc3 == 1:
                        cursor.execute("INSERT INTO Remitos (Codigo_Barra, Cantidad, DNI_Proveedor, Fecha, Rubro, Precio, Stock) VALUES (%s, %s, %s, %s, %s, %s, %s)", (self.codigoBarra, self.cantidad, self.dniProveedor, self.fecha, self.rubro, self.precio, self.stock))
                        miConexion.commit()
                        # Actualizamos el stock del articulo
                        cursor.execute("UPDATE Articulos SET Stock = Stock - %s WHERE Codigo_Barra = %s", (self.cantidad, self.codigoBarra))
                        miConexion.commit()
                        # Eliminamos la orden de reposicion
                        cursor.execute("DELETE FROM Pedido_reposicion WHERE Codigo_Barra = %s", (self.codigoBarra))
                        miConexion.commit()
                        print("Remito Confirmado, Productos actualizados")
                        #print("Remito Confirmado")
                        os.system("pause")
                        os.system("cls")
                        print("Remito cargado correctamente , los datos son: ")
                        engine = create_engine("mariadb+pymysql://root:4488@localhost/Sistema_La_Criolla?charset=utf8mb4")
                        df = pd.read_sql_query("SELECT * FROM Remitos", engine)
                        print(df)
                        os.system("pause")
                        os.system("cls")
                        Articulo.menu(self)
                    else:
                        print("Remito no Confirmado")
                        os.system("pause")
                        os.system("cls")
                        Articulo.menu(self)
                elif opc2 == 2:
                    opc4 = int(input("Desa crear un Remito manualmente? 1-Si 2-No: "))
                    if opc4 == 1:
                        print("Sistema de Creacion de Remitos")
                        self.codigoBarra = input("Ingrese el Codigo de Barra del Articulo: ")
                        self.cantidad = int(input("Ingrese la Cantidad: "))
                        self.dniProveedor = input("Ingrese el DNI del Proveedor: ")
                        self.fecha = date.today()
                        self.rubro = input("Ingrese el Rubro: ")
                        self.precio = input("Ingrese el Precio: ")
                        self.stock = input("Ingrese el Stock: ")
                        os.system("cls")
                        os.system("pause")
                        print("Los datos del Remito son: ")
                        print("Codigo de Barra: ", self.codigoBarra)
                        print("Cantidad: ", self.cantidad)
                        print("DNI del Proveedor: ", self.dniProveedor)
                        print("Fecha: ", self.fecha)
                        print("Rubro: ", self.rubro)
                        print("Precio: ", self.precio)
                        print("Stock: ", self.stock)
                        opc3 = int(input("Desea Confirmar el Remito? 1-Si 2-No: "))
                        if opc3 == 1:
                            cursor.execute("INSERT INTO Remitos (Codigo_Barra, Cantidad, DNI_Proveedor, Fecha, Rubro, Precio, Stock) VALUES (%s, %s, %s, %s, %s, %s, %s)", (self.codigoBarra, self.cantidad, self.dniProveedor, self.fecha, self.rubro, self.precio, self.stock))
                            miConexion.commit()
                            # Actualizamos el stock del articulo
                            cursor.execute("UPDATE Articulos SET Stock = Stock - %s WHERE Codigo_Barra = %s", (self.cantidad, self.codigoBarra))
                            miConexion.commit()
                            # Eliminamos la orden de reposicion
                            cursor.execute("DELETE FROM Pedido_reposicion WHERE Codigo_Barra = %s", (self.codigoBarra))
                            miConexion.commit()
                            print("Remito Confirmado, Productos actualizados")
                            engine = create_engine("mariadb+pymysql://root:4488@localhost/Sistema_La_Criolla?charset=utf8mb4")
                            df = pd.read_sql_query("SELECT * FROM Remitos", engine)
                            print(df)
                            os.system("pause") 
                            os.system("cls")
                            Articulo.menu(self)
                            # Actualizamos

                    
                

                
                #os.system("pause")
                #os.system("cls")
                #Articulo.menu(self)
            #print(df)
            #print("Sistema de Creacion de Remitos")
            #self.codigoBarra = input("Ingrese el Codigo de Barra del Articulo: ")
            #self.cantidad = int(input("Ingrese la Cantidad: "))
            #self.dniProveedor = input("Ingrese el DNI del Proveedor: ")
            #self.fecha = date.today()
            #self.rubro = input("Ingrese el Rubro: ")
            #self.precio = input("Ingrese el Precio: ")
            #self.stock = input("Ingrese el Stock: ")
            #os.system("pause")
            


        elif opc == 7:
            time.sleep(1)
            print("Gracias por utilizar Menu Articulo")
            time.sleep(1)
            os.system("cls")
            MenuPrincipal()
"""
Fin CLASE Articulo
"""
############################################################################################
############################################################################################


"""
CLASE Proveedor
"""
############################################################################################
############################################################################################

# Heredar de la clase Articulo
class Proveedor(Articulo):
    miConexion = mariadb.connect(host="localhost", user="root", passwd="4488", db="Sistema_La_Criolla")
    cursor = miConexion.cursor()
    def __init__(self, dni, nombreFantasia, direccion, telefono, mail, situacionIVA, codigoBarra, nombre, rubro, precio, stock, dniProveedor):
        super().__init__(self,codigoBarra, nombre, rubro, precio, stock, dniProveedor)
        self.dni = dni
        self.nombreFantasia = nombreFantasia
        self.direccion = direccion
        self.telefono = telefono
        self.mail = mail
        self.situacionIVA = situacionIVA
        self.codigoBarra = codigoBarra
        self.nombre = nombre
        self.rubro = rubro
        self.precio = precio
        self.stock = stock
        self.dniProveedor = dniProveedor
    
        #opc = 0
    def menu(self):
        os.system("cls")
        opc = int(input("""
        Bienvenido al Menu Proveedor, que Desea hacer?: 
        1- Alta
        2- Baja 
        3- Modificacion
        4- Listar 
        5- Pedido de reposicion
        6- Devolución a proveedor
        7- Salir 
        """))
        if opc == 1:
            print("Alta de Proveedor")
            print("Datos existentes en la tabla: ")
            engine = create_engine("mariadb+pymysql://root:4488@localhost/Sistema_La_Criolla?charset=utf8mb4")
            df = pd.read_sql_query("SELECT * FROM Proveedores", engine)
            if df.empty:
                print("No hay datos en la tabla")
            else:
              print(df)
            print("##############")
            self.dni = input("Ingrese el DNI: ")
            # Consulta para verificar si el DNI ya existe
            cursor.execute("SELECT * FROM Proveedores WHERE DNI = %s", (self.dni,))
            resultado = cursor.fetchall()
            if resultado:
                print("El DNI ya existe")
                os.system("pause")
                os.system("cls")
                Proveedor.menu(self)
            self.nombreFantasia = input("Ingrese el Nombre de Fantasia: ")
            self.direccion = input("Ingrese la Direccion: ")
            self.telefono = input("Ingrese el Telefono: ")
            self.mail = input("Ingrese el Mail: ")
            self.situacionIVA = input("Ingrese la Situacion IVA: 1- Responsable Inscripto, 2- Responsable no Inscripto, 3- Exento, 4- No Responsable: ")
            if self.situacionIVA == "1":
                self.situacionIVA = "Responsable Inscripto"
            elif self.situacionIVA == "2":
                self.situacionIVA = "Responsable no Inscripto"
            elif self.situacionIVA == "3":
                self.situacionIVA = "Exento"
            elif self.situacionIVA == "4":
                self.situacionIVA = "No Responsable"
            else:
                print("La situacion IVA ingresada no es valida")
                os.system("pause")
                os.system("cls")
                Proveedor.menu(self)

            cursor.execute ("INSERT INTO Proveedores (DNI, Nombre_Fantasia, Direccion, Telefono, Mail, Situacion_IVA) VALUES (%s, %s, %s, %s, %s, %s)", (self.dni, self.nombreFantasia, self.direccion, self.telefono, self.mail, self.situacionIVA))
            miConexion.commit()
            print("Proveedor Agregado, Base de Datos Actualizada")
            print("##############")
            print("Datos existentes en la tabla: ")
            #engine = create_engine("mariadb+pymysql://root:4488@localhost/Sistema_La_Criolla?charset=utf8mb4")
            df = pd.read_sql_query("SELECT * FROM Proveedores", engine)
            print(df)
            os.system("pause")
            os.system("cls")
            Proveedor.menu(self)
        elif opc == 2:
            print("Datos existentes en la tabla: ")
            engine = create_engine("mariadb+pymysql://root:4488@localhost/Sistema_La_Criolla?charset=utf8mb4")
            df = pd.read_sql_query("SELECT * FROM Proveedores", engine)
            print(df)
            print("##############")
            self.dni = input("Ingrese el DNI del proveedor a Eliminar: ")
            # verificar si el DNI existe
            cursor.execute("SELECT * FROM Proveedores WHERE DNI = %s", (self.dni,))
            resultado = cursor.fetchall()
            if resultado:
                cursor.execute("DELETE FROM Proveedores WHERE DNI = %s", (self.dni,))
                miConexion.commit()
                print("Proveedor Eliminado")
                os.system("pause")
                os.system("cls")
                Proveedor.menu(self)
            else:
                print("El DNI no existe")
                os.system("pause")
                os.system("cls")
                Proveedor.menu(self)
        elif opc == 3:
            print("Datos existentes en la tabla: ")
            engine = create_engine("mariadb+pymysql://root:4488@localhost/Sistema_La_Criolla?charset=utf8mb4")
            df = pd.read_sql_query("SELECT * FROM Proveedores", engine)
            print(df)
            print("************************")
            self.dni = input("Ingrese el DNI del proveedor a Modificar: ")
            # consultar si el DNI no existe
            cursor.execute("SELECT * FROM Proveedores WHERE DNI = %s", (self.dni,))
            resultado = cursor.fetchall()
            if resultado:
                self.nombreFantasia = input("Ingrese el Nombre de Fantasia: ")
                self.direccion = input("Ingrese la Direccion: ")
                self.telefono = input("Ingrese el Telefono: ")
                self.mail = input("Ingrese el Mail: ")
                self.situacionIVA = input("Ingrese la Situacion IVA: ")
                cursor.execute ("UPDATE Proveedores SET Nombre_Fantasia = %s, Direccion = %s, Telefono = %s, Mail = %s, Situacion_IVA = %s WHERE DNI = %s", (self.nombreFantasia, self.direccion, self.telefono, self.mail, self.situacionIVA, self.dni))
                miConexion.commit()
                print("Proveedor Modificado, Base de Datos Actualizada")
                print("##############")
                print("Nuevos Datos existentes en la tabla: ")
                df = pd.read_sql_query("SELECT * FROM Proveedores", engine)
                print(df)
                os.system("pause")
                os.system("cls")
                Proveedor.menu(self)
            else:
                print("El DNI no existe")
                os.system("pause")
                os.system("cls")
                Proveedor.menu(self)
            
           
        elif opc == 4:
            print("Datos existentes en la tabla: ")
            engine = create_engine("mariadb+pymysql://root:4488@localhost/Sistema_La_Criolla?charset=utf8mb4")
            df = pd.read_sql_query("SELECT * FROM Proveedores", engine)
            print(df)
            #cursor.execute("SELECT * FROM Proveedores")
            #resultado = cursor.fetchall()
            #for i in resultado:
             #   print(i)
            os.system("pause")
            os.system("cls")
            Proveedor.menu(self)
        elif opc == 5:
            #  extension para pedido de reposicion
            # Guardar en la tabla remitos para luego en remitos chequear si el producto esta en stock
            print("Pedido de Reposicion de Articulos")
            print("Ingrese Todos los datos para iniciar una reposicion")
            print("##############")
            print("Datos existentes en la tabla: Proveedores ")
            engine = create_engine("mariadb+pymysql://root:4488@localhost/Sistema_La_Criolla?charset=utf8mb4")
            df = pd.read_sql_query("SELECT * FROM Proveedores", engine)
            print(df)
            print("##############")
            print("##############")
            print("Datos existentes en la tabla: Articulos ")
            #engine = create_engine("mariadb+pymysql://root:4488@localhost/Sistema_La_Criolla?charset=utf8mb4")
            df = pd.read_sql_query("SELECT * FROM Articulos", engine)
            print(df)
            print("##############")
            self.dni = input("Ingrese el DNI del proveedor: ")
            # verificar si el DNI existe
            cursor.execute("SELECT * FROM Proveedores WHERE DNI = %s", (self.dni,))
            resultado = cursor.fetchall()
            if resultado:
                self.codigoBarra = input("Ingrese el Codigo de Barra: ")
                self.nombre = input("Ingrese el Nombre Del Producto : ")
                self.rubro = input("Ingrese el Rubro: ")
                self.precio = input("Ingrese el Precio: ")
                self.stock = input("Ingrese el Stock a Reponer: ")
               # print("##############")
                #print("Datos existentes en la tabla: Proveedores ")
                #engine = create_engine("mariadb+pymysql://root:4488@localhost/Sistema_La_Criolla?charset=utf8mb4")
                #df = pd.read_sql_query("SELECT * FROM Proveedores", engine)
                #print(df)
                #print("##############")
                #self.dniProveedor = input("Ingrese el DNI del proveedor: ")
                self.fecha = date.today()
                #cursor.execute ("INSERT INTO Articulos (Codigo_Barra, Nombre, Rubro, Precio, Stock, DNI_Proveedor) VALUES (%s, %s, %s, %s, %s, %s)", (self.codigoBarra, self.nombre, self.rubro, self.precio, self.stock, self.dniProveedor))
                #miConexion.commit()
                print("Pedido de Reposicion Realizado")
                # Guardar en tabla remitos para luego en remitos chequear si el producto esta en stock
                #cursor.execute("CREATE TABLE IF NOT EXISTS Pedido_Reposicion(Codigo_Barra VARCHAR(20) PRIMARY KEY, DNI_Proveedor VARCHAR(20), Fecha DATE, Rubro VARCHAR(50), Precio FLOAT, Stock INT)")

                cursor.execute ("INSERT INTO pedido_reposicion (Codigo_Barra, DNI_Proveedor, Fecha, Rubro, Precio, Stock) VALUES (%s, %s, %s, %s, %s, %s)", (self.codigoBarra, self.dni, self.fecha, self.rubro, self.precio, self.stock))
                miConexion.commit()
                # armar tabla reposicion
                os.system("pause")
                os.system("cls")
                Proveedor.menu(self)

        elif opc == 6:
           # Devolucion a proveedor de un producto sacando el stock
            print("Devolucion a proveedor")
            print("Ingrese los siguientes datos:")
            print("##############")
            print("Datos existentes en la tabla: Proveedores ")
            engine = create_engine("mariadb+pymysql://root:4488@localhost/Sistema_La_Criolla?charset=utf8mb4")
            df = pd.read_sql_query("SELECT * FROM Proveedores", engine)
            print(df)
            print("##############")
            print("Datos existentes en la tabla: Articulos ")
            #engine = create_engine("mariadb+pymysql://root:4488@localhost/Sistema_La_Criolla?charset=utf8mb4")
            df = pd.read_sql_query("SELECT * FROM Articulos", engine)
            print(df)
            print("##############")
            self.dni = input("Ingrese el DNI del proveedor: ")
            # verificar si el DNI existe
            cursor.execute("SELECT * FROM Proveedores WHERE DNI = %s", (self.dni,))
            resultado = cursor.fetchall()
            if resultado:
                self.codigoBarra = input("Ingrese el Codigo de Barra: ")
                print("Usted va a devolver el producto: ")
                cursor.execute("SELECT * FROM Articulos WHERE Codigo_Barra = %s", (self.codigoBarra,))
                resultado = cursor.fetchall()
                for i in resultado:
                    dataframe = pd.DataFrame(resultado,columns=['Codigo_Barra','Nombre','Rubro','Precio', 'Precio_Proveedor' ,'Stock','DNI_Proveedor','Estado'])
                    print(dataframe)
                    #print(i)
                self.stock = input("Ingrese el Stock a Devolver: ")

                #self.rubro = input("Ingrese el Rubro: ")
                #self.precio = input("Ingrese el Precio: ")
                #self.stock = input("Ingrese el Stock que quiere devolver : ")
                self.motivo = input("Ingrese el motivo de la devolucion: ")
               # Al stock le restamos el stock que quiere devolver
                cursor.execute ("UPDATE articulos SET Stock = Stock - %s, Estado = %s WHERE Codigo_Barra = %s", (self.stock, self.motivo, self.codigoBarra))
                #cursor.execute("UPDATE articulos SET Motivo = %s WHERE Codigo_Barra = %s", (motivo, self.codigoBarra))
                miConexion.commit()
                print("Stock devuelto, Base de Datos Actualizada")
                print("##############")
                print("Datos existentes en la tabla: ")
                df = pd.read_sql_query("SELECT * FROM Articulos", engine)
                print(df)
                os.system("pause")
                os.system("cls")
                Proveedor.menu(self)
            else:
                print("El DNI no existe")
                os.system("pause")
                os.system("cls")
                Proveedor.menu(self)
            

        elif opc == 7:
            time.sleep(1)
            print("Gracias por utilizar nuestro servicio")
            time.sleep(1)
            os.system("cls")
            MenuPrincipal()
            self.cursor.close()

##################################################################################################

##################################################################################################





"""
CLASS VENTAS
       
"""
##################################################################################################
##################################################################################################
# Heredar de la clase Cliente
class Ventas(Cliente):
    miConexion = mariadb.connect(host="localhost", user="root", passwd="4488", db="Sistema_La_Criolla")
    cursor = miConexion.cursor()
    def __init__(self, dniCliente, codigoBarra, cantidad, monto):
      #  super().__init__(self, dni, apellidoNombre, direccion, telefono, mail, situacionIVA)
        self.dniCliente = dniCliente
        self.codigoBarra = codigoBarra
        self.cantidad = cantidad
        self.monto = monto
        #self.dni = dni
        #self.apellidoNombre = apellidoNombre
        #self.direccion = direccion
        #self.telefono = telefono
        #self.mail = mail
        #self.situacionIVA = situacionIVA

        #opc = 0
    def menu(self):
        opc = int(input("""
        Bienvenido al Menu Ventas, que Desea hacer?: 
        1- Facturacion 
        2- Listado de Ventas del dia 
        3- Salir
        """))
        if opc == 1:
            os.system("cls")
            print("Bienvenido al Menu Facturacion")
            print("Ingrese los siguientes datos:")
            print("##############")
            print("Datos existentes en la tabla: Clientes ")
            engine = create_engine("mariadb+pymysql://root:4488@localhost/Sistema_La_Criolla?charset=utf8mb4")
            df = pd.read_sql_query("SELECT * FROM Clientes", engine)
            print(df)
            print("##############")
            print("Datos existentes en la tabla: Articulos ")
            engine = create_engine("mariadb+pymysql://root:4488@localhost/Sistema_La_Criolla?charset=utf8mb4")
            df = pd.read_sql_query("SELECT * FROM Articulos", engine)
            print(df)
            tipoCliente = int(input("Cliente es consumidor Final?: 1- Si, 2- No \n"))
            if tipoCliente == 1:
                self.dniCliente = 99999
                self.fecha = date.today()
                self.codigoBarra = input("Ingrese el Codigo de Barra: ")
                self.cantidad = int(input("Ingrese la cantidad de productos: "))
                # Traer el precio del producto de la tabla Articulos
                cursor.execute("SELECT Precio FROM Articulos WHERE Codigo_Barra = %s", (self.codigoBarra,))
                resultado = cursor.fetchall()
                for i in resultado:
                    self.monto = i[0] * self.cantidad
                    print("El monto a pagar es: ", self.monto)
                cursor.execute("SELECT Nombre FROM Articulos WHERE Codigo_Barra = %s", (self.codigoBarra,))
                resultado = cursor.fetchall()
                for i in resultado:
                    self.nombre = i[0]
                    print("El nombre del producto es: ", self.nombre)
                    #print(i)
                #self.precio = cursor.execute("SELECT Precio FROM Articulos WHERE Codigo_Barra = %s", (self.codigoBarra,))
                #print(self.precio)
                #self.monto = self.precio * self.cantidad
                #self.monto = int(input("Ingrese el monto total: "))
                cursor.execute ("INSERT INTO Ventas (DNI_Cliente, Codigo_Barra, Cantidad, Monto, Fecha, Productos) VALUES (%s, %s, %s, %s, %s, %s)", (self.dniCliente, self.codigoBarra, self.cantidad, self.monto, self.fecha, self.nombre))
                miConexion.commit()
                # Actualizar el stock del producto
                cursor.execute ("UPDATE articulos SET Stock = Stock - %s WHERE Codigo_Barra = %s", (self.cantidad, self.codigoBarra))
                miConexion.commit()
                print("Venta realizada, Base de Datos Actualizada")
                print("Factura Generada")
                print("##############")
                print("Datos existentes en la tabla: Ventas ")
                df = pd.read_sql_query("SELECT * FROM Ventas", engine)
                print(df)
                print("##############")
                print("Datos existentes en la tabla: Articulos ")
                df = pd.read_sql_query("SELECT * FROM Articulos", engine)
                print(df)
                print("##############")
                os.system("pause")
                os.system("cls")
                Ventas.menu(self)
            elif tipoCliente == 2:
                print("Datos existentes en la tabla: Clientes ")
                df = pd.read_sql_query("SELECT * FROM Clientes", engine)
                print(df)
                print("##############")
                self.dniCliente = input("Ingrese el DNI del cliente: ")
             # verificar si el DNI existe, si no existe crearlo
                cursor.execute("SELECT * FROM clientes WHERE DNI = %s", (self.dniCliente,))
                resultado = cursor.fetchall()
                if resultado:
                 self.codigoBarra = input("Ingrese el Codigo de Barra: ")
                 producto = input("Ingrese el producto: ")
                 self.cantidad = input("Ingrese la cantidad: ")
                 self.monto = input("Ingrese el monto: ")
                 Fecha = date.today()
                 cursor.execute ("INSERT INTO Ventas (DNI_Cliente, productos, Codigo_Barra, Cantidad, Monto, Fecha) VALUES (%s, %s, %s, %s, %s, %s)", (self.dniCliente, self.codigoBarra, producto, self.cantidad, self.monto, Fecha))
                 cursor.execute("UPDATE Proveedores SET Stock = Stock - %s WHERE Codigo_Barra = %s", (self.cantidad, self.codigoBarra))
                 miConexion.commit()
                 print("Factura Realizada")
                 os.system("pause")
                 os.system("cls")
                 Ventas.menu(self)
                else:
                 print("El DNI no existe")
                 print("Se creara un nuevo cliente")
                 self.apellido_Nombre = input("Ingrese el Nombre y Apellido: ")
                 self.direccion = input("Ingrese la direccion: ")
                 self.telefono = input("Ingrese el telefono: ")
                 self.mail = input("Ingrese el mail: ")
                 self.situacionIVA = input("Ingrese la situacion de IVA: 1- Responsable Inscripto, 2- No Responsable, 3- Exento, 4- Consumidor Final ")
                 if self.situacionIVA == 1:
                     self.situacionIVA = "Responsable Inscripto"
                 elif self.situacionIVA == 2:
                     self.situacionIVA = "No Responsable"
                 elif self.situacionIVA == 3:
                        self.situacionIVA = "Exento"
                 elif self.situacionIVA == 4:
                        self.situacionIVA = "Consumidor Final"
                 else:
                        print("Situacion de IVA no valida")
                 cursor.execute ("INSERT INTO Clientes (DNI, Apellido_Nombre, Direccion, Telefono, Mail, Situacion_IVA) VALUES (%s, %s, %s, %s, %s, %s)", (self.dniCliente, self.apellido_Nombre, self.direccion, self.telefono, self.mail, self.situacionIVA))
                 miConexion.commit()
                 print("Cliente Creado")
                 os.system("pause")
                 os.system("cls")
                 Ventas.menu(1) #  o probar con Ventas.menu(self)


        elif opc == 2:
            # Traer los datos de la tabla Ventas ordenados por fecha
            print("Datos existentes en la tabla: Ventas en el dia de hoy ")
            engine = create_engine("mariadb+pymysql://root:4488@localhost/Sistema_La_Criolla?charset=utf8mb4")
            df = pd.read_sql_query("SELECT * FROM Ventas WHERE Fecha = CURDATE()", engine)
            print(df)
            #cursor.execute("SELECT * FROM Ventas")
            #resultado = cursor.fetchall()
            #for i in resultado:
             #   print(i)
            os.system("pause")
            os.system("cls")
            Ventas.menu(self)

        elif opc == 3:
            time.sleep(1)
            print("Gracias por utilizar Menu Ventas")
            time.sleep(1)
            MenuPrincipal()
            

    
def ocultar_contrasena():
    import getpass
    return getpass.getpass()


class MenuLogIN:
    def __init__(self):
        print("Bienvenido al Sistema La Criolla")
        print("Que Tipo de Usuario desea ingresar?: \n")
        self.opc = int(input("1. Administrador \n2. Usuario \n3. Salir \n"))

        if self.opc == 1:
            print("Ingrese su Usuario y contraseña: ")
            self.usuario = input("Usuario: ")
            self.contrasena = ocultar_contrasena()
            if self.contrasena == "admin":
                os.system("cls")
                print("Bienvenido Administrador")
                MenuPrincipal()
                
            else:
                print("Contraseña incorrecta")
        elif self.opc == 2:
            print("Ingrese su Usuario y contraseña: ")
            self.usuario = input("Usuario: ")
            self.contrasena = ocultar_contrasena()
            if self.contrasena == "user":
                os.system("cls")
                print("Bienvenido Usuario")
                MenuPrincipal2()
            else:
                print("Contraseña incorrecta")
        elif self.opc == 3:
            print("Gracias por usar nuestro sistema")
            exit()
        else:
            print("Opcion no valida")
            time.sleep(1)
            os.system("cls")    



class MenuPrincipal:
    def __init__(self):
        print("Bienvenido al Sistema La Criolla")
       # print("Que Tipo de Usuario desea ingresar?: \n")
        #self.opc = print("1-Empleado")
        #self.opc =  print("2-Administrador")
        
        self.opciones = int(input("""
        1. Clientes
        2. Proveedores
        3. Articulos
        4. Ventas        
        5. Salir
        """))
        if self.opciones == 1:
            Cliente.menu(self)
        elif self.opciones == 2:
            Proveedor.menu(self)
        elif self.opciones == 3:
            Articulo.menu(self)
        elif self.opciones == 4:
            Ventas.menu(self)
        elif self.opciones == 5:
            print("Gracias por usar nuestro sistema")
            exit()
        else:
            print("Opcion no valida")
            time.sleep(1)
            os.system("cls")
            MenuPrincipal()
            #self.__init__()

class MenuPrincipal2():
    def __init__(self):
        self.msj = print("Bienvenido al Sistema La Criolla")
        self.opciones = int(input("""
        1. Clientes
        2. Proveedores - Disable
        3. Articulos - Disable
        4. Ventas        
        5. Salir
        """))
        if self.opciones == 1:
            Cliente.menu(self)
        elif self.opciones == 2:
            print("Opcion no disponible")
            time.sleep(1)
            os.system("cls")
            MenuPrincipal2()
        elif self.opciones == 3:
            print("Opcion no disponible")
            time.sleep(1)
            os.system("cls")
            MenuPrincipal2()
        elif self.opciones == 4:
            Ventas.menu(self)
        elif self.opciones == 5:
            print("Gracias por usar nuestro sistema")
            exit()
        else:
            print("Opcion no valida")
            time.sleep(1)
            os.system("cls")
            MenuPrincipal2()
            #self.__init__()
    

#time.sleep(1)
MenuLogIN()
MenuPrincipal()
MenuPrincipal2()
cliente = Cliente("", "", "", "", "", "")
provedor = Proveedor("", "", "", "", "", "")
articulos = Articulo("", "", "", "", "", "")
ventas = Ventas("", "", "", "")




   