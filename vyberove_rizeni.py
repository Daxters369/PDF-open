import os
import subprocess
import tempfile
import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF
import argparse
import time

# Konstanty
PDF_FILENAME = "devops_job_description.pdf"
SYSINFO_FILENAME = "systeminfo.txt"
SYSINFO_FOLDER = "sysinfo"
HACKED_MESSAGE = "You have been hacked!"
SYSINFO_PATH = r"C:\Users\ASUS\AppData\Local\Temp\sysinfo"  # Přesná cesta k uložení systémových informací

def save_system_info(output_file: str) -> None:
    """Uloží systémové informace do souboru pomocí příkazu systeminfo."""
    try:
        with open(output_file, "w") as file:
            subprocess.run(["systeminfo"], stdout=file, text=True, check=True)
        print(f"Systémové informace byly uloženy do '{output_file}'.")
    except (FileNotFoundError, PermissionError) as e:
        print(f"Chyba při ukládání systémových informací: {e}")
    except subprocess.CalledProcessError as e:
        print(f"Příkaz systeminfo selhal: {e}")
    except Exception as e:
        print(f"Neočekávaná chyba: {e}")

def get_devops_description() -> list:
    """Vrací seznam řádků s popisem výběrového řízení na pozici DevOps."""
    return [
        "Job Title: DevOps Engineer",
        "Company: YourCompany Inc.",
        "Location: Prague, Czech Republic",
        "Type: Full-time",
        "Salary: Competitive",
        "",
        "Job Description:",
        "- Build and maintain CI/CD pipelines",
        "- Manage cloud infrastructure (AWS, Azure)",
        "- Ensure high availability and scalability",
        "- Implement monitoring and alerting systems",
        "",
        "Requirements:",
        "- Experience with Linux/Unix environments",
        "- Experience with containers (Docker, Kubernetes)",
        "- Knowledge of cloud platforms (AWS, Azure)",
        "- Experience with CI/CD tools (Jenkins, GitLab CI)",
        "",
        "To apply, send your resume to jobs@yourcompany.com"
    ]

def add_watermarks(pdf: FPDF, message: str):
    """Přidá 5 vodoznaků na stránku PDF."""
    pdf.set_font("Helvetica", size=50)
    pdf.set_text_color(200, 200, 200)  # Světle šedá barva pro vodoznaky
    
    # Umístění vodoznaků
    positions = [
        (50, 50),
        (100, 100),
        (150, 150),
        (200, 200),
        (250, 250)
    ]
    
    for x, y in positions:
        pdf.set_xy(x, y)
        pdf.cell(0, 10, text=message, new_x="LMARGIN", new_y="NEXT")

def create_pdf(pdf_path: str):
    """Vytvoří PDF soubor s popisem výběrového řízení na DevOps pozici a vodoznakem."""
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)  # Nahrazení Arial za Helvetica

        # Získání popisu a jeho přidání do PDF
        for line in get_devops_description():
            pdf.cell(200, 10, text=line, new_x="LMARGIN", new_y="NEXT")  # Oprava deprekovaných parametrů

        # Přidání 5 vodoznaků s hláškou HACKED_MESSAGE
        add_watermarks(pdf, HACKED_MESSAGE)

        # Uložení PDF souboru
        pdf.output(pdf_path)
        print(f"PDF soubor '{pdf_path}' byl vytvořen.")
    except Exception as e:
        print(f"Chyba při vytváření PDF souboru: {e}")

def open_pdf(pdf_path: str):
    """Otevře PDF soubor pomocí výchozí aplikace v systému."""
    if os.path.exists(pdf_path):
        try:
            if os.name == 'nt':
                os.startfile(pdf_path)  # Otevírá soubor pomocí asociovaného programu (Windows)
            else:
                subprocess.call(['xdg-open', pdf_path])  # Otevírá soubor na Linuxu pomocí výchozí aplikace
            print(f"PDF soubor '{pdf_path}' byl otevřen.")
        except FileNotFoundError as e:
            print(f"Soubor '{pdf_path}' nebyl nalezen: {e}")
        except Exception as e:
            print(f"Neočekávaná chyba při otevírání PDF: {e}")
    else:
        print(f"Soubor '{pdf_path}' neexistuje.")

def verify_file(file_path: str) -> None:
    """Ověří existenci souboru a jeho velikost."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Soubor '{file_path}' nebyl nalezen.")

    if os.path.getsize(file_path) == 0:
        raise ValueError(f"Soubor '{file_path}' je prázdný.")
    
    print(f"Soubor '{file_path}' byl úspěšně ověřen.")

def create_sysinfo_folder_if_not_exists(folder_path: str):
    """Zkontroluje, zda složka existuje, a případně ji vytvoří."""
    try:
        os.makedirs(folder_path, exist_ok=True)
        print(f"Složka '{folder_path}' je připravena.")
    except OSError as e:
        print(f"Chyba při vytváření složky '{folder_path}': {e}")

def show_hacked_message():
    """Zobrazí vyskakovací okno s hláškou a čeká 5 sekund před jeho zavřením."""
    try:
        root = tk.Tk()
        root.withdraw()  # Skryje hlavní okno
        messagebox.showinfo("Alert", HACKED_MESSAGE)
        time.sleep(5)  # Čeká 5 sekund
        root.destroy()  # Ukončí okno
        print(f"Vyskakovací okno bylo zobrazeno a zavřeno po 5 sekundách.")
    except Exception as e:
        print(f"Chyba při zobrazení vyskakovacího okna: {e}")

def show_cmd_hacked_message():
    """Zobrazí hlášku 'You have been hacked!' pomocí CMD."""
    try:
        subprocess.run(f'echo {HACKED_MESSAGE} && pause', shell=True, check=True)
        print(f"Hláška '{HACKED_MESSAGE}' byla zobrazena v CMD.")
    except subprocess.CalledProcessError as e:
        print(f"Chyba při zobrazení CMD hlášky: {e}")

def main():
    parser = argparse.ArgumentParser(description="DevOps PDF Generator")
    parser.add_argument("--create-pdf", action="store_true", help="Vytvoří PDF s popisem výběrového řízení")
    parser.add_argument("--save-sysinfo", action="store_true", help="Uloží systémové informace do souboru")
    parser.add_argument("--create-folder", action="store_true", help="Vytvoří složku pro systémové informace")
    parser.add_argument("--show-hacked", action="store_true", help="Zobrazí hlášku 'You have been hacked!'")
    args = parser.parse_args()

    # Pokud nebyl zadán žádný argument, spustí se všechny funkce
    if not any(vars(args).values()):
        print("Žádné argumenty nebyly zadány, spouštím všechny funkce postupně...")

        # Spustit všechny funkce
        create_sysinfo_folder_if_not_exists(SYSINFO_PATH)
        sysinfo_file = os.path.join(SYSINFO_PATH, SYSINFO_FILENAME)
        save_system_info(sysinfo_file)
        verify_file(sysinfo_file)

        pdf_path = os.path.join(tempfile.gettempdir(), PDF_FILENAME)
        create_pdf(pdf_path)
        verify_file(pdf_path)
        open_pdf(pdf_path)
        
        show_cmd_hacked_message()

    # Volání jednotlivých funkcí podle zadaných argumentů
    if args.create_folder:
        create_sysinfo_folder_if_not_exists(SYSINFO_PATH)

    if args.save_sysinfo:
        sysinfo_file = os.path.join(SYSINFO_PATH, SYSINFO_FILENAME)
        save_system_info(sysinfo_file)
        verify_file(sysinfo_file)

    if args.create_pdf:
        pdf_path = os.path.join(tempfile.gettempdir(), PDF_FILENAME)
        create_pdf(pdf_path)
        verify_file(pdf_path)
        open_pdf(pdf_path)

    if args.show_hacked:
        show_cmd_hacked_message()

if __name__ == "__main__":
    main()
