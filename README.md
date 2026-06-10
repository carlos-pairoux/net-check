# NetCheck

NetCheck es un script Python para diagnosticar conectividad básica de red que responde a cuatro preguntas concretas:

- ¿Quién soy en la red?
- ¿Puedo resolver nombres de dominio?
- ¿Puedo llegar al exterior?
- ¿Con qué latencia?

Eso es suficiente para determinar si una máquina tiene conectividad funcional o dónde empieza el problema.

---

## Por qué estas cuatro preguntas y en este orden

La secuencia refleja cómo se diagnostica una red en la práctica: de lo local hacia lo externo.

Primero hostname e IP: si esto falla, el problema es de configuración del sistema, no de red.

Después DNS: punto de falla externo más común. Separarlo del ping permite distinguir entre "no hay red" y "hay red pero DNS está caído".

Finalmente conectividad y latencia con un único paquete. No se promedian múltiples porque el objetivo es diagnóstico rápido, no medir calidad del enlace.

---

## Modo de uso

```bash
python net_check.py
```

Sin dependencias externas. Requiere Python 3.x.

---

## Output (ejemplo)

<pre>
--- LOCAL ---
  hostname: DESKTOP-123
  local_ip: 192.168.1.10

--- DNS ---
  domain: google.com
  resolved_ip: 142.250.80.46

--- CONNECTIVITY ---
  True

--- LATENCY ---
  193.0

--- STATUS_SUMMARY ---
  ok
</pre>

---

## Interpretación del output

`LOCAL` confirma que el equipo tiene identidad en la red.  
`DNS` confirma que puede resolver nombres de dominio.  
`CONNECTIVITY` indica si el host respondió al ping.  
`LATENCY` muestra el tiempo de respuesta en milisegundos.  
`STATUS_SUMMARY` resume el estado general:

- `ok` si DNS resolvió y el host respondió.
- `degraded` ante cualquier fallo parcial.

---

## Por qué está diseñado así

La IP local se obtiene con un socket UDP conectado a 8.8.8.8 sin enviar tráfico real. Esto fuerza al sistema operativo a elegir la interfaz de salida correcta, resolviendo el problema clásico de `gethostbyname()` que devuelve `127.0.0.1` en sistemas con múltiples interfaces.

El dominio objetivo está fijo en `google.com`. Mantener el script sin argumentos de entrada simplifica su uso en soporte básico donde configurar parámetros no agrega valor. Si el proyecto crece, parametrizarlo desde terminal es la extensión natural.

`status_summary` distingue solo entre `ok` y `degraded` sin detallar qué componente falló. Para diagnóstico de primer nivel es suficiente; extender esa lógica es el siguiente paso natural si se necesita más granularidad.

La latencia se parsea de la salida de texto del ping del sistema operativo. Es funcional pero frágil ante cambios de formato entre versiones o idiomas. Una mejora posible sería usar ICMP directamente con una librería dedicada.

NetCheck es una herramienta de diagnóstico básico de red. No reemplaza soluciones de monitoreo en producción.

---

## Autor

[Carlos Pairoux](https://github.com/carlos-pairoux)
