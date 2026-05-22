# 📝 Historial de Cambios (Changelog)

Todos los cambios notables en este proyecto serán documentados en este archivo.
El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

## [1.3.0] - 2026-05-22

### ✨ Mejoras

- Añadido _endpoint_ `exp_juzgados`. Para entrega de los juzgados de los que se pueden pedir expedientes, en el servicio de "revisión de expedientes" preferentemente para la unidad de "Archivo".
- Mejora en el formato del archivo `README.md`.
- Mensaje de requisitos en plantilla para cita creada. "_Debes presentar tu credencial de identificación (INE) vigente_".
- Añadido campo `instrucciones` al modelo `cit_servicios` y añadirlo en la entrega de su _endpoint_.
- Descripción de la versión en la documentación _swagger_ hecha por defecto.


## [1.2.0] - 2026-05-20

### ✨ Mejoras

- Creación de plantillas para diferentes envíos de email, al crear y canelar citas.
- Uso de plantillas para envío de emails.
- Creación de servicio de envío de emails con plantillas.
- Documentación en 'README.md', 'CONTRIBUTING.md' y este 'CHANGELOG.md'.

### 🛠️ Cambiado

- Cambiar asunto de email de PJECZ a SAJI.


## [0.1.2] - 2026-05-07

### ✨ Mejoras

- Utilización de `uv` como manejador de paquetes de **Python**.
