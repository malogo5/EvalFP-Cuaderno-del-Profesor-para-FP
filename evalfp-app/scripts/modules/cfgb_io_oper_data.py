"""EvalFP — Operaciones Auxiliares para la Configuración y Explotación · 3030 · FPB Informática de Oficina
RD 356/2014, de 16 de mayo (BOE) · Decreto CLM 80/2014, de 1 de agosto (DOCM [2014/10283])
"""
MODULO = {
    "nombre":"Operaciones Auxiliares para la Configuración y la Explotación","codigo":"3030","abrev":"OPER",
    "ciclo":"","ciclo_clave":"CFGB","ciclo_nivel":"CFGB",
    "curso":"2º IO","horas_sem":7,"total_horas":210,"anno":"2026-2027","eval_count":3,
    "decreto":"RD 356/2014, de 16 de mayo · Decreto CLM 80/2014, de 1 de agosto (DOCM [2014/10283])",
}
UTS = [
    {"id":"UT1","nombre":"Configuración en entorno monousuario","horas":53,"eval":1,"tags":"Sistema operativo · Usuarios · Archivos · Permisos · Periféricos · Ergonomía"},
    {"id":"UT2","nombre":"Configuración en entorno de red","horas":52,"eval":2,"tags":"Red local · TCP/IP · Recursos compartidos · Impresoras · VPN · Seguridad"},
    {"id":"UT3","nombre":"Paquete ofimático básico","horas":53,"eval":2,"tags":"Procesador de texto · Hoja de cálculo · Presentaciones · PDF · Macros"},
    {"id":"UT4","nombre":"Utilidades de Internet","horas":52,"eval":3,"tags":"Navegador · Correo · Mensajería · Almacenamiento nube · Seguridad web"},
]
RAS = [
    {"id":"RA1","pond":25,"nombre":"Configura equipos informáticos para su funcionamiento en un entorno monousuario, interpretando la documentación técnica y aplicando las instrucciones recibidas."},
    {"id":"RA2","pond":25,"nombre":"Configura equipos informáticos para su funcionamiento en un entorno de red, describiendo sus características e interpretando la documentación técnica."},
    {"id":"RA3","pond":25,"nombre":"Utiliza aplicaciones de un paquete ofimático, relacionándolas con sus aplicaciones en un entorno laboral."},
    {"id":"RA4","pond":25,"nombre":"Emplea utilidades proporcionadas por Internet, configurándolas e identificando su funcionalidad en el entorno personal y laboral."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
]
EVAL_RAS = {1:["RA1"], 2:["RA2","RA3"], 3:["RA4"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["practica"] for ra in ["RA1","RA2","RA3","RA4"]}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado y configurado los parámetros básicos del sistema operativo.",
        "Se han creado y administrado cuentas de usuario con distintos niveles de privilegio.",
        "Se ha gestionado el sistema de archivos, organizando la información en directorios y aplicando los permisos oportunos.",
        "Se han instalado y desinstalado aplicaciones, verificando su correcta ejecución.",
        "Se han configurado los periféricos de entrada/salida —ratón, teclado, pantalla, impresora— en función del trabajo a realizar.",
        "Se han aplicado las medidas de seguridad básicas del sistema operativo —contraseñas, bloqueo de pantalla, cifrado—.",
        "Se han aplicado las reglas de ergonomía y salud en el uso del puesto de trabajo.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los elementos básicos de una red de área local —switch, router, cable, tarjeta de red—.",
        "Se han configurado los parámetros TCP/IP del equipo para su conexión a una red local.",
        "Se han compartido carpetas e impresoras en la red, asignando los permisos adecuados.",
        "Se ha comprobado la conectividad del equipo con otros dispositivos de la red utilizando herramientas de diagnóstico.",
        "Se han configurado conexiones de acceso remoto y VPN básicas siguiendo las instrucciones facilitadas.",
        "Se han aplicado las medidas de seguridad básicas en la conexión a redes —contraseña Wi-Fi, firewall—.",
        "Se han identificado y resuelto incidencias básicas de conectividad de red.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las aplicaciones del paquete ofimático y sus principales funciones.",
        "Se han creado, editado y guardado documentos de texto aplicando formatos básicos.",
        "Se han elaborado hojas de cálculo con datos, fórmulas y gráficos sencillos.",
        "Se han creado presentaciones con diapositivas incorporando texto, imágenes y elementos multimedia.",
        "Se han exportado e importado documentos en distintos formatos, incluido PDF.",
        "Se han utilizado las funciones básicas de la agenda y el calendario del paquete ofimático.",
        "Se han aplicado técnicas de gestión de archivos y copias de seguridad de los documentos creados.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado y configurado los parámetros básicos del navegador web.",
        "Se han utilizado buscadores para localizar información, valorando la fiabilidad de las fuentes.",
        "Se ha configurado y utilizado el correo electrónico para comunicaciones personales y profesionales.",
        "Se han utilizado herramientas de mensajería instantánea y videoconferencia básicas.",
        "Se han utilizado servicios de almacenamiento en la nube para compartir y sincronizar archivos.",
        "Se han identificado los riesgos de seguridad en el uso de Internet —phishing, malware, privacidad—.",
        "Se han aplicado medidas básicas de seguridad en la navegación web y el correo electrónico.",
        "Se han descargado y actualizado aplicaciones desde fuentes seguras y repositorios oficiales.",
    ], start=1)],
}
