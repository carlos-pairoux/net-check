#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket

# --- Diagnóstico local ---

def get_hostname() -> dict:
    """Retorna el nombre del host local. 
    Clave: 'hostname' o 'error'."""
    try:
        return {"hostname": socket.gethostname()}
    except Exception as e:
        return {"error": f"Hostname error: {str(e)}"}

def get_local_ip() -> dict:
    """Retorna la IP local activa usando un socket UDP 
    sin enviar tráfico real. Clave: 'local_ip' o 'error'."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Se crea un socket UDP. No establece conexión real,
        # pero obliga al sistema operativo a elegir la interfaz
        # de red que usaría para llegar a esa dirección.
        s.connect(("8.8.8.8", 80))
        # 8.8.8.8 es el DNS público de Google. No se envía nada,
        # solo se usa como destino para que el SO resuelva la ruta.
        ip = s.getsockname()[0]
        # getsockname() devuelve la dirección local asignada al socket.
        # El índice [0] extrae únicamente la IP, descartando el puerto.
        s.close()
        return {"local_ip": ip}
    except Exception as e:
        return {"error": f"Local IP error: {str(e)}"}
