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

    usuario_selector = contraseña_selector = boton_enviar_selector = None

    for selector in [
        "input[name*='user']", "input[name*='email']", "input[name*='login']",
        "input#username", "input#email", "input[type='text']", "input"
    ]:
        if page.locator(selector).count() > 0:
            usuario_selector = selector
            break

    for selector in ["input[name*='pass']", "input#password", "input[type='password']"]:
        if page.locator(selector).count() > 0:
            contraseña_selector = selector
            break

    for selector in [
        "button[type='submit']", "input[type='submit']", "button[name*='login']",
        "button#login", "button", "input[type='button']"
    ]:
        if page.locator(selector).count() > 0:
            boton_enviar_selector = selector
            break

    if not usuario_selector or not contraseña_selector or not boton_enviar_selector:
        raise ValueError("No se pudieron detectar todos los selectores necesarios automáticamente.")

    print(f"Detectado usuario: {usuario_selector}")
    print(f"Detectado contraseña: {contraseña_selector}")
    print(f"Detectado botón enviar: {boton_enviar_selector}")
    return usuario_selector, contraseña_selector, boton_enviar_selector

def determinar_uso_de_tor(url):
    dominios_excluidos = ["genescol.com", ".web", "localhost", "127.", "192.168."]
    return not any(d in url for d in dominios_excluidos)

def main():
    print("=== Script Anónimo con Playwright + Tor + User-Agent Rotativo ===")
    url = input("Introduce la URL del formulario (real o de pruebas): ").strip()

    usar_tor = determinar_uso_de_tor(url)
    ua = UserAgent()
    contador = 0

    try:
        with sync_playwright() as p:
            while True:
                user_agent = ua.random
                print(f"\n🕵️ Usando User-Agent: {user_agent}")
                print(f"🔌 Usando Tor: {'Sí' if usar_tor else 'No'}")

                proxy_settings = {"server": "socks5://127.0.0.1:9050"} if usar_tor else None

                browser = p.chromium.launch(
                    headless=True,
                    proxy=proxy_settings
                )

                context = browser.new_context(user_agent=user_agent)
                page = context.new_page()
                page.set_default_timeout(120000)

                try:
                    page.goto(url, timeout=120000)
                    usuario_selector, contraseña_selector, boton_enviar_selector = detectar_selectores(page)

                    while True:
                        page.goto(url)
                        page.wait_for_selector(usuario_selector)
                        page.wait_for_selector(contraseña_selector)

                        correo, contraseña = generar_credenciales()
                        page.fill(usuario_selector, correo)
                        page.fill(contraseña_selector, contraseña)
                        page.click(boton_enviar_selector)

                        contador += 1
                        print(f"[{contador}] Enviado usuario: {correo}, contraseña: {contraseña}")
                        time.sleep(2)

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
