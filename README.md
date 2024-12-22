# Proyecto de Análisis Web 🌐

Herramienta de web scraping y análisis de vulnerabilidades construida con Python. Este proyecto incluye capacidades para recopilar noticias de Hacker News y escanear vulnerabilidades CVE para servicios específicos.

## Características ⚡

- Escaneo de vulnerabilidades CVE usando la API NIST NVD
- Funcionalidad de web scraping para Hacker News 
- Exportación de datos a formatos estructurados
- Interfaz de línea de comandos amigable

## Requisitos 📋

```bash
beautifulsoup4==4.12.2
requests==2.31.0
pandas==2.1.1
```

Instalación 🛠️

Clonar el repositorio

bashCopygit clone https://github.com/tunombre/Analysis-Web-Project.git
cd Analysis-Web-Project

Crear y activar entorno virtual (opcional pero recomendado)

bashCopypython -m venv venv
source venv/bin/activate  # En Windows usar: venv\Scripts\activate

Instalar dependencias

bashCopypip install -r requirements.txt
Uso 💻
Escáner de Vulnerabilidades
pythonCopyfrom src.controller.vulnerability_scanner import VulnerabilityScanner

scanner = VulnerabilityScanner()
resultados = scanner.search_cves("ProFTPD 1.3.5")
print(resultados)
Web Scraper
pythonCopyfrom src.scraper import main as scraper_main

scraper_main()
Estructura del Proyecto 📁
CopyAnalysis-Web-Project/
├── src/
│   ├── __init__.py
│   ├── controller/
│   │   ├── __init__.py
│   │   └── vulnerability_scanner.py
│   └── scraper.py
├── requirements.txt
├── README.md
└── main.py
Cómo Contribuir 🤝

Haz un Fork del proyecto
Crea tu rama de características (git checkout -b feature/NuevaCaracteristica)
Haz commit de tus cambios (git commit -m 'Añadir nueva característica')
Haz Push a la rama (git push origin feature/NuevaCaracteristica)
Abre un Pull Request

Licencia 📄
Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE.md para más detalles
