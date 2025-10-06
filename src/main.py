import csv
import time
import sys

import pyautogui
import pyperclip

import flet as ft

# Estado global simple para cancelación
cancelar_proceso = False


def app_main(page: ft.Page):
    global cancelar_proceso
    app_name = "DataShooterApp"
    version = "0.1.0"

    page.title = f"{app_name} - v{version}"
    page.theme = ft.Theme(color_scheme=ft.ColorScheme(primary=ft.Colors.CYAN_ACCENT_700))
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.frameless = True
    page.window.width = 680
    page.window.height = 680
    page.window.center()
    page.padding = 16
    page.scroll = ft.ScrollMode.AUTO

    page.appbar = ft.AppBar(
        leading=ft.Container(
            ft.Image(
                src="icon.png",
                width=40,
                height=40,
                fit=ft.ImageFit.CONTAIN,
            ),
            margin=ft.Margin(left=10, top=0, right=0, bottom=0),
        ),
        leading_width=40,
        title=ft.Text(app_name),
        center_title=False,
        bgcolor=ft.Colors.PRIMARY,
        actions=[
            ft.IconButton(
                icon=ft.Icons.CLOSE,
                tooltip="Cerrar",
                on_click=lambda _: page.window.close(),
            )
        ],
    )

    # --- Helpers UI ---
    def log(msg: str):
        log_list.controls.append(
            ft.Text(msg, selectable=False, style=ft.TextStyle(font_family="monospace"))
        )
        log_list.update()

    def set_progress(p: float):
        progress_bar.value = max(0.0, min(1.0, p))
        progress_bar.update()

    def set_running(running: bool):
        btn_iniciar.disabled = running
        btn_cancelar.disabled = not running
        inputs_container.disabled = running
        btn_iniciar.update()
        btn_cancelar.update()
        inputs_container.update()

    # --- File picker ---
    def on_file_result(e: ft.FilePickerResultEvent):
        if e.files and len(e.files) > 0:
            ruta_csv.value = e.files[0].path or ""
            ruta_csv.update()

    file_picker = ft.FilePicker(on_result=on_file_result)
    page.overlay.append(file_picker)

    # --- Inputs ---
    tiempo_espera = ft.TextField(label="Tiempo de espera (s)", value="0.3", expand=True)
    cuenta_atras = ft.TextField(label="Cuenta atrás (s)", value="3", expand=True)
    ruta_csv = ft.TextField(label="Ruta del CSV", expand=True)
    btn_csv = ft.ElevatedButton(
        "Seleccionar CSV",
        on_click=lambda _: file_picker.pick_files(
            allow_multiple=False,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["csv"],
        ),
    )

    omitir_lineas = ft.TextField(
        label="Omitir líneas (encabezados)", value="0", width=200
    )
    columnas = ft.TextField(
        label="Columnas a copiar (separadas por comas)",
        value="0,1",
        expand=True,
        hint_text="Ej. 0,2,3",
    )

    tecla = ft.Dropdown(
        label="Tecla luego de pegar",
        options=[
            ft.dropdown.Option("enter"),
            ft.dropdown.Option("tab"),
            ft.dropdown.Option("space"),
            ft.dropdown.Option(","),
        ],
        value="enter",
        width=200,
    )

    inputs_container = ft.Column(
        controls=[
            ft.Row([tiempo_espera, cuenta_atras]),
            ft.Row([ruta_csv, btn_csv]),
            ft.Row([omitir_lineas, columnas]),
            ft.Row([tecla]),
        ]
    )

    # --- Log y progreso ---
    log_list = ft.ListView(
        height=220,
        auto_scroll=True,
        spacing=4,
        padding=10,
    )
    progress_bar = ft.ProgressBar(value=0.0)

    # --- Lógica principal ---
    def copiar_y_pegar(texto: str):
        # Manejo de portapapeles y pegado (Cmd+V en macOS, Ctrl+V en otros)
        pyperclip.copy(texto)
        time.sleep(0.1)
        if sys.platform == "darwin":
            pyautogui.hotkey("command", "v")
        else:
            pyautogui.hotkey("ctrl", "v")

    def worker(
        _tiempo_espera: float,
        _cuenta_atras: int,
        _archivo_csv: str,
        _omitir_lineas: int,
        _columnas: list[int],
        _tecla: str,
    ):
        global cancelar_proceso
        cancelar_proceso = False
        set_running(True)
        set_progress(0.0)
        log("Preparando ejecución…")

        # Cuenta atrás
        for i in range(_cuenta_atras, 0, -1):
            if cancelar_proceso:
                log("Proceso cancelado.")
                set_running(False)
                return
            log(f"Iniciando en {i}")
            time.sleep(1)

        # Mover el cursor a una posición segura
        try:
            pyautogui.moveTo(10, 10)
            log(
                "El cursor se ha movido a una posición segura. No muevas el ratón durante la ejecución."
            )
        except Exception as ex:
            log(f"Advertencia al mover cursor: {ex}")

        # Preparar portapapeles
        log("Preparando el portapapeles…")
        pyperclip.copy("Preparación")
        time.sleep(0.3)

        try:
            with open(_archivo_csv, newline="", encoding="utf-8-sig") as csvfile:
                reader = csv.reader(csvfile)
                filas = list(reader)
                if _omitir_lineas > 0:
                    filas = filas[_omitir_lineas:]
                total_filas = len(filas)

                if total_filas == 0:
                    log("No hay filas para procesar tras omitir encabezados.")
                    set_running(False)
                    return

                for idx, fila in enumerate(filas, start=1):
                    if cancelar_proceso:
                        log("Proceso cancelado durante la ejecución.")
                        set_running(False)
                        return

                    # Progreso
                    set_progress(idx / total_filas)
                    log(f"Procesando fila {idx} de {total_filas}")

                    for col in _columnas:
                        # Corrección: permitir columna 0
                        if col < 0:
                            continue
                        try:
                            texto = fila[col]
                        except Exception:
                            log(f"Columna {col} fuera de rango en fila {idx}: {fila}")
                            continue
                        copiar_y_pegar(texto)
                        try:
                            pyautogui.press(_tecla)
                        except Exception as ex:
                            log(f"No se pudo presionar '{_tecla}': {ex}")
                        time.sleep(_tiempo_espera)
        except FileNotFoundError:
            log("Error: archivo CSV no encontrado.")
        except Exception as ex:
            log(f"Error procesando CSV: {ex}")
        finally:
            # try:
            #     # Volver el cursor al centro
            #     size = pyautogui.size()
            #     pyautogui.moveTo(size.width / 2, size.height / 2)
            # except Exception:
            #     pass
            log("El script ha terminado.")
            set_progress(1.0)
            set_running(False)

    # --- Acciones botones ---
    def on_iniciar(_):
        global cancelar_proceso
        cancelar_proceso = False
        log_list.controls.clear()
        log_list.update()
        try:
            t_espera = float(tiempo_espera.value.strip())
            c_atras = int(cuenta_atras.value.strip())
            archivo = ruta_csv.value.strip()
            if not archivo:
                page.snack_bar = ft.SnackBar(ft.Text("Selecciona un archivo CSV"))
                page.snack_bar.open = True
                page.update()
                return
            omitir = int(omitir_lineas.value.strip() or 0)
            cols_raw = [
                c.strip() for c in (columnas.value or "").split(",") if c.strip() != ""
            ]
            if not cols_raw:
                page.snack_bar = ft.SnackBar(ft.Text("Ingresa las columnas a copiar"))
                page.snack_bar.open = True
                page.update()
                return
            cols = []
            for c in cols_raw:
                try:
                    cols.append(int(c))
                except ValueError:
                    log(f"Columna inválida: '{c}' (se omite)")

            key = tecla.value or "enter"
            set_running(True)

            page.run_thread(worker, t_espera, c_atras, archivo, omitir, cols, key)
        except ValueError:
            page.snack_bar = ft.SnackBar(
                ft.Text("Ingresa valores válidos en los campos numéricos")
            )
            page.snack_bar.open = True
            page.update()

    def on_cancelar(_):
        global cancelar_proceso
        cancelar_proceso = True
        log("Solicitud de cancelación recibida…")

    btn_iniciar = ft.FilledButton(
        "Iniciar", icon=ft.Icons.PLAY_ARROW, on_click=on_iniciar, expand=True
    )
    btn_cancelar = ft.OutlinedButton(
        "Cancelar", icon=ft.Icons.STOP, on_click=on_cancelar, disabled=True, expand=True
    )

    page.add(
        ft.Text("Convierte un CSV a una secuencia de teclas para pegar en un sitio web.", style=ft.TextThemeStyle.BODY_SMALL),
        ft.Divider(height=1),
        inputs_container,
        ft.Row([btn_iniciar, btn_cancelar], spacing=10),
        progress_bar,
        log_list,
    )


if __name__ == "__main__":
    ft.app(target=app_main)
