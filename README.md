# DataShooterApp 🔫
> Dispara filas de un CSV como si fueran tecleadas por un humano.

![Python](https://img.shields.io/badge/Python->=3.9-blue)
![Version](https://img.shields.io/badge/version-0.1.0-lightgrey)
![License](https://img.shields.io/badge/license-GPL--3.0-green)

---

## 🧩 Descripción general

**DataShooterApp** automatiza el copiado y pegado secuencial del contenido de un archivo CSV para simular la interacción de un usuario.  
Fue creada originalmente para **replicar el proceso de escaneo de códigos de barras**, pegando datos en cualquier campo activo del sistema operativo.

El flujo es simple: seleccionas el CSV, defines qué columnas usar, ajustas los tiempos… y el programa “teclea” cada fila.

---

## ⚙️ Estado del proyecto
**Etapa:** `production`  
**Versión:** `0.1.0`  
**Probado en:** macOS  
**Teóricamente compatible con:** Linux y Windows

---

## 🧠 Tecnologías utilizadas
- **Lenguaje:** Python ≥ 3.9  
- **UI Framework:** [Flet](https://flet.dev/) `0.28.3`  
- **Dependencias adicionales:**
  - `pyautogui >= 0.9.54`
  - `pyperclip >= 1.11.0`
- **Gestor de paquetes:** [UV](https://github.com/astral-sh/uv)

---

## 🧰 Requisitos
- Python 3.9 o superior  
- Tener instalado **UV**  
- macOS (probado) — requiere permisos de accesibilidad para simular teclado

---

## 🪜 Instalación y ejecución

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/alfnigredo/DataShooterApp.git
   cd DataShooterApp
   ```

2. **Instalar dependencias y ejecutar:**
   ```bash
   uv run flet run
   ```

   Esto crea el entorno automáticamente y lanza la aplicación.

---

## 🧱 Configuración de permisos (macOS)

Para que **pyautogui** pueda simular pulsaciones de teclado, debes **autorizar la app en el panel de accesibilidad:**

1. Abre **Preferencias del Sistema → Privacidad y Seguridad → Accesibilidad**.  
2. Haz clic en el candado para permitir cambios.  
3. Agrega tu terminal (o el IDE desde el que ejecutes la app) a la lista de aplicaciones permitidas.  
4. Reinicia la app.

⚠️ No necesita “Control total del disco”.  
En Linux puede requerir instalar `xclip` o `xsel` para que `pyperclip` funcione correctamente.

---

## 💡 Uso básico

1. Ejecuta la aplicación.  
2. Configura:
   - Tiempo de espera entre líneas (`Tiempo de espera (s)`).
   - Tiempo de cuenta regresiva (`Cuenta atrás (s)`).
   - Archivo CSV y columnas a usar (`Columnas a copiar`, ej. `0,1,2`).
   - Tecla posterior a cada pegado (`Enter`, `Tab`, etc.).  
3. Presiona **Iniciar**.  
4. Cambia a la aplicación destino (donde quieras pegar).  
5. El programa comenzará a pegar automáticamente.

---

## 📁 Estructura del repositorio

```
src/
 └── main.py     # Punto de entrada principal
```

Estructura estándar generada por UV.

---

## 🚫 Alcance y limitaciones

- **In-scope:** automatizar el pegado secuencial de valores desde un CSV.  
- **Out-of-scope:** no interactúa con elementos por selector, ni reconoce campos por ID o posición visual.  
- No realiza OCR ni lectura contextual de pantalla.

---

## 🛠️ Estándares y calidad

- Convenciones de commits: **Conventional Commits**
- Versionado: **SemVer**
- Licencia: **GPL-3.0**
- 100 % ejecución local (sin dependencias en la nube)

---

## 🧭 Roadmap

- [ ] Soporte para archivos **.xlsx**
- [ ] Hotkeys personalizables por columna

---

## 🤝 Contribuciones

Actualmente no se aceptan contribuciones externas.  
Si deseas sugerir mejoras o reportar bugs, puedes abrir un **issue** o enviar un **pull request** siguiendo el formato de commits convencional.

---

## 🪪 Licencia

Distribuido bajo los términos de la licencia **GNU General Public License v3.0**.  
Esto significa que puedes usar, modificar y redistribuir este software, siempre y cuando mantengas la atribución al autor original y distribuyas los cambios bajo la misma licencia.

Consulta el archivo [`LICENSE`](LICENSE) para más detalles.

---

## 👤 Autor

**Alf Nigredo**  
📧 3aico.circuss@gmail.com

---

© 2025 Alf Nigredo. Todos los derechos reservados.