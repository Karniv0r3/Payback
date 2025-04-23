
![Payback Logo](./payback-logo.png)


# Payback Anti-Phishing Script 🛡️

Este script automatiza el envío masivo de credenciales falsas a sitios de phishing que simulan formularios de acceso con el objetivo de **saturar sus bases de datos y sabotear a los delincuentes**.

### ⚙️ Requisitos

- Python 3.13+
- [Playwright](https://playwright.dev/python/)
- [Fake User Agent](https://pypi.org/project/fake-useragent/)
- (Opcional) Tor en segundo plano si se desea anonimato.

### 🚀 Instalación

```bash
pip install -r requirements.txt
python -m playwright install
```

### 🧠 Uso

```bash
python3 payback.py
```

El script te pedirá la URL donde se encuentra el formulario falso. Cuando se la des, Payback detectará los campos y comenzará a enviar credenciales aleatorias automáticamente. Se detiene con `Ctrl + C`.

### 🕵️ Características

- Rotación automática de User-Agent.
- Uso opcional de Tor para anonimato.
- Detección automática de campos de usuario/contraseña y botón de envío.
- Compatible con WordPress y otros formularios.
