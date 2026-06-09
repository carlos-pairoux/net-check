#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import subprocess
import platform

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

# --- Diagnóstico remoto ---

def resolve_dns(domain: str) -> dict:
    """Resuelve un dominio a su dirección IP.
    Clave: 'domain', 'resolved_ip' o 'error'."""
    try:
        ip = socket.gethostbyname(domain)
        return {"domain": domain, "resolved_ip": ip}
    except socket.gaierror as e:
        return {"error": f"DNS resolution error: {str(e)}"}

def ping(host: str) -> dict:
    """Verifica conectividad y mide latencia hacia un host.
    Clave: 'host', 'reachable', 'latency_ms' o 'error'."""
    try:
        param = "-n" if platform.system() == "Windows" else "-c"
        result = subprocess.run(
            ["ping", param, "1", host],
            capture_output=True,
            text=True
        )
        # param cambia según el SO: "-n" en Windows, "-c" en Linux/macOS.
        # Ambos indican que se envía un único paquete para minimizar el tiempo
        # de espera y mantener el diagnóstico liviano.
        reachable = result.returncode == 0
        # returncode 0 indica que el host respondió al paquete ICMP.
        # Cualquier otro valor significa que no hubo respuesta o hubo error.
        latency = "parse error"
        if reachable:
            for line in result.stdout.splitlines():
                if "time=" in line or "tiempo=" in line:
                    part = line.split("time=")[-1] if "time=" in line else line.split("tiempo=")[-1]
                    latency = float(part.split()[0].replace("ms", "").strip())
                    break
        # Se parsea la salida del ping para extraer la latencia en ms.
        # Se contemplan dos formatos porque Windows y Linux difieren en el texto de salida.
        return {"host": host, "reachable": reachable, "latency_ms": latency}
    except Exception as e:
        return {"error": f"Ping error: {str(e)}"}

