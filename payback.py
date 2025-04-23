
from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent
import random, string, time, sys

def generar_credenciales():
    usuario = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    dominio = random.choice(["@jmail.com", "@yajoo.net", "@hotmaill.net"])
    correo = usuario + dominio
    contraseña = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return correo, contraseña

def detectar_selectores(page):
    print("\nDetectando selectores del formulario...")
    print("DOM cargado correctamente.\n")

    def buscar_selectores(selector_list):
        for sel in selector_list:
            loc = page.locator(sel)
            if loc.count() > 0:
                return sel
        return None

    posibles_usuarios = [
        "input[name*='user']", "input[name*='email']", "input[name*='login']",
        "input[placeholder*='email']", "input[placeholder*='correo']", "input[placeholder*='usuario']",
        "input[aria-label*='usuario']", "input[aria-label*='email']",
        "input[id*='user']", "input[class*='user']", "input[class*='login']",
        "input[type='text']", "input[type='email']", "input[type='tel']", "input"
    ]

    posibles_passwords = [
        "input[type='password']", "input[name*='pass']", "input[id*='pass']",
        "input[placeholder*='contraseña']", "input[aria-label*='contraseña']",
        "input[class*='pass']"
    ]

    posibles_botones = [
        "button[type='submit']", "input[type='submit']", "input[type='button']",
        "button", "div[role='button']", "span[role='button']",
        "*[onclick*='login']", "*[onclick*='submit']",
        "*[name*='login']", "*[id*='login']", "*[class*='login']"
    ]

    usuario_selector = buscar_selectores(posibles_usuarios)
    contraseña_selector = buscar_selectores(posibles_passwords)
    boton_enviar_selector = buscar_selectores(posibles_botones)

    if not usuario_selector or not contraseña_selector or not boton_enviar_selector:
        print("⚠️ No se pudieron detectar todos los selectores. Mostrando diagnóstico...")
        time.sleep(3)
        print("\n🔍 Campos detectados en el DOM principal:")
        for i, inp in enumerate(page.query_selector_all("input"), 1):
            print(f"  [INPUT {i}] {inp.get_attribute('outerHTML')}")
        for i, btn in enumerate(page.query_selector_all("button, input[type='submit'], div[role='button'], span[role='button']"), 1):
            print(f"  [BOTÓN {i}] {btn.get_attribute('outerHTML')}")
        raise ValueError("Detección automática fallida.")

    print(f"Detectado usuario: {usuario_selector}")
    print(f"Detectado contraseña: {contraseña_selector}")
    print(f"Detectado botón enviar: {boton_enviar_selector}")
    return usuario_selector, contraseña_selector, boton_enviar_selector

def main():
    print("=== Script Anónimo con Playwright + Emulación Realista ===")
    url = input("Introduce la URL del formulario (real o de pruebas): ").strip()
    usar_tor = input("¿Deseás usar Tor? (s/n): ").strip().lower() == 's'
    navegador = input("¿Navegador a usar? (chromium/firefox/webkit): ").strip().lower() or "chromium"
    ua = UserAgent()
    contador = 0

    try:
        with sync_playwright() as p:
            while True:
                user_agent = ua.random
                print(f"\n🕵️ Usando User-Agent: {user_agent}")
                print(f"🔌 Usando Tor: {'Sí' if usar_tor else 'No'}")

                proxy_settings = {"server": "socks5://127.0.0.1:9050"} if usar_tor else None
                browser_type = getattr(p, navegador if navegador in ["chromium", "firefox", "webkit"] else "chromium")
                browser = browser_type.launch(headless=True, proxy=proxy_settings)

                context = browser.new_context(
                    user_agent=user_agent,
                    locale="es-ES",
                    timezone_id="America/Bogota",
                    viewport={"width": 1280, "height": 720},
                    screen={"width": 1280, "height": 720},
                    device_scale_factor=1.0,
                    is_mobile=False,
                    has_touch=False,
                    permissions=["geolocation"],
                    extra_http_headers={
                        "Accept-Language": "es-ES,es;q=0.9",
                        "Upgrade-Insecure-Requests": "1"
                    }
                )

                page = context.new_page()
                page.set_default_timeout(120000)

                try:
                    page.goto(url, timeout=120000)
                    usuario_selector, contraseña_selector, boton_enviar_selector = detectar_selectores(page)

                    while True:
                        page.wait_for_selector(usuario_selector, timeout=10000)
                        page.wait_for_selector(contraseña_selector, timeout=10000)

                        correo, contraseña = generar_credenciales()
                        page.fill(usuario_selector, correo)
                        page.fill(contraseña_selector, contraseña)
                        page.click(boton_enviar_selector)

                        contador += 1
                        print(f"[{contador}] Enviado usuario: {correo}, contraseña: {contraseña}")
                        time.sleep(2)

                        page.goto(url)
                        if page.locator(usuario_selector).count() == 0:
                            print("⚠️ El formulario ya no está disponible. Probablemente fue bloqueado.")
                            return

                except KeyboardInterrupt:
                    print(f"\n🛑 Script detenido por el usuario. Se enviaron {contador} pares de credenciales.")
                    return
                except Exception as e:
                    print(f"⚠️ Error en ejecución: {e}")
                finally:
                    try:
                        browser.close()
                    except:
                        pass

    except KeyboardInterrupt:
        print(f"\n🛑 Script detenido por el usuario. Se enviaron {contador} pares de credenciales.")
        sys.exit(0)

if __name__ == "__main__":
    main()
