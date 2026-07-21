import os
import subprocess
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Configuração visual padrão do CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class PDFConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações da Janela Principal
        self.title("Conversor de PDF Avançado / Advanced PDF Converter")
        self.geometry("600x480")
        self.resizable(False, False)

        # Variáveis de estado
        self.pdf_path = ctk.StringVar()
        self.input_files = []
        self.output_dir = ctk.StringVar()
        self.output_format = ctk.StringVar(value="EPUB")
        self.lang = ctk.StringVar(value="PT")

        # Dicionário de Traduções
        self.translations = {
            "PT": {
                "title": "Conversor de Arquivos para eBooks",
                "file_lbl": "Arquivo(s):",
                "btn_browse": "Procurar",
                "dest_lbl": "Salvar em:",
                "format_lbl": "Formato de Saída:",
                "btn_convert": "Converter Agora",
                "status_waiting": "Aguardando ação...",
                "status_converting": "Convertendo...",
                "status_batch": "Iniciando processamento em lote...",
                "warn_no_file": "Por favor, selecione pelo menos um arquivo.",
                "warn_no_dest": "Por favor, selecione uma pasta de destino válida.",
                "warn_title": "Aviso",
                "dialog_files_title": "Selecione os arquivos",
                "dialog_dest_title": "Selecione a pasta de destino",
                "file_types": "eBooks e Documentos",
                "all_files": "Todos os Arquivos",
                "files_selected": "arquivos selecionados",
                "converting_x_of_y": "Convertendo {i} de {total}...\n{filename}",
                "batch_done": "Lote Concluído! {success}/{total} arquivos convertidos.",
                "batch_partial": "Atenção: Apenas {success} de {total} foram convertidos com sucesso.",
                "batch_error": "Erro: Nenhum arquivo foi convertido. Verifique os formatos.",
                "error_engine": "Erro crítico: Motor de conversão (ebook-convert) não encontrado.",
                "error_unexpected": "Ocorreu um erro inesperado: {error}"
            },
            "EN": {
                "title": "File to eBook Converter",
                "file_lbl": "File(s):",
                "btn_browse": "Browse",
                "dest_lbl": "Save to:",
                "format_lbl": "Output Format:",
                "btn_convert": "Convert Now",
                "status_waiting": "Waiting for action...",
                "status_converting": "Converting...",
                "status_batch": "Starting batch processing...",
                "warn_no_file": "Please select at least one file.",
                "warn_no_dest": "Please select a valid destination folder.",
                "warn_title": "Warning",
                "dialog_files_title": "Select files",
                "dialog_dest_title": "Select destination folder",
                "file_types": "eBooks and Documents",
                "all_files": "All Files",
                "files_selected": "files selected",
                "converting_x_of_y": "Converting {i} of {total}...\n{filename}",
                "batch_done": "Batch Complete! {success}/{total} files converted.",
                "batch_partial": "Attention: Only {success} of {total} converted successfully.",
                "batch_error": "Error: No files were converted. Check the formats.",
                "error_engine": "Critical Error: Conversion engine (ebook-convert) not found.",
                "error_unexpected": "An unexpected error occurred: {error}"
            }
        }

        # Construção da Interface
        self.build_ui()

    def build_ui(self):
        t = self.translations[self.lang.get()]

        # Frame superior para o Menu de Idiomas
        frame_top = ctk.CTkFrame(self, fg_color="transparent")
        frame_top.pack(fill="x", padx=20, pady=(10, 0))
        
        self.lang_menu = ctk.CTkOptionMenu(frame_top, variable=self.lang, values=["PT", "EN"], command=self.change_language, width=70)
        self.lang_menu.pack(side="right")

        # Título
        self.title_label = ctk.CTkLabel(self, text=t["title"], font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=(0, 10))

        # Frame de Seleção de Arquivo(s)
        frame_file = ctk.CTkFrame(self)
        frame_file.pack(fill="x", padx=20, pady=10)
        
        self.lbl_file = ctk.CTkLabel(frame_file, text=t["file_lbl"])
        self.lbl_file.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        entry_file = ctk.CTkEntry(frame_file, textvariable=self.pdf_path, width=320, state="readonly")
        entry_file.grid(row=0, column=1, padx=10, pady=10)
        
        self.btn_file = ctk.CTkButton(frame_file, text=t["btn_browse"], width=80, command=self.select_pdf)
        self.btn_file.grid(row=0, column=2, padx=10, pady=10)

        # Frame de Seleção da Pasta de Destino
        frame_dest = ctk.CTkFrame(self)
        frame_dest.pack(fill="x", padx=20, pady=10)
        
        self.lbl_dest = ctk.CTkLabel(frame_dest, text=t["dest_lbl"])
        self.lbl_dest.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        entry_dest = ctk.CTkEntry(frame_dest, textvariable=self.output_dir, width=320, state="readonly")
        entry_dest.grid(row=0, column=1, padx=10, pady=10)
        
        self.btn_dest = ctk.CTkButton(frame_dest, text=t["btn_browse"], width=80, command=self.select_output_dir)
        self.btn_dest.grid(row=0, column=2, padx=10, pady=10)

        # Frame de Opções de Conversão
        frame_options = ctk.CTkFrame(self)
        frame_options.pack(fill="x", padx=20, pady=10)

        self.lbl_format = ctk.CTkLabel(frame_options, text=t["format_lbl"])
        self.lbl_format.pack(side="left", padx=10, pady=10)

        opt_format = ctk.CTkOptionMenu(frame_options, variable=self.output_format, values=["EPUB", "MOBI", "AZW3", "PDF", "DOCX", "TXT"])
        opt_format.pack(side="left", padx=10, pady=10)

        # Botão de Converter
        self.btn_convert = ctk.CTkButton(self, text=t["btn_convert"], font=ctk.CTkFont(size=15, weight="bold"), height=40, command=self.start_conversion_thread)
        self.btn_convert.pack(pady=(20, 10))

        # Barra de Progresso
        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.pack(pady=(0, 10))
        self.progress_bar.set(0)

        # Label de Status (Feedback para o usuário)
        self.lbl_status = ctk.CTkLabel(self, text=t["status_waiting"], text_color="gray")
        self.lbl_status.pack(pady=(0, 10))

    def change_language(self, choice):
        t = self.translations[choice]
        
        # Atualiza os textos estáticos da interface
        self.title_label.configure(text=t["title"])
        self.lbl_file.configure(text=t["file_lbl"])
        self.btn_file.configure(text=t["btn_browse"])
        self.lbl_dest.configure(text=t["dest_lbl"])
        self.btn_dest.configure(text=t["btn_browse"])
        self.lbl_format.configure(text=t["format_lbl"])
        
        # Atualiza os textos dinâmicos de acordo com o estado atual do programa
        if self.btn_convert.cget("state") == "normal":
            self.btn_convert.configure(text=t["btn_convert"])
            if not self.input_files:
                self.lbl_status.configure(text=t["status_waiting"])
        else:
            self.btn_convert.configure(text=t["status_converting"])

        if len(self.input_files) > 1:
            self.pdf_path.set(f"{len(self.input_files)} {t['files_selected']}")

    def select_pdf(self):
        t = self.translations[self.lang.get()]
        file_paths = filedialog.askopenfilenames(
            title=t["dialog_files_title"],
            filetypes=[(t["file_types"], "*.pdf *.epub *.mobi *.azw3 *.docx *.txt"), (t["all_files"], "*.*")]
        )
        if file_paths:
            self.input_files = list(file_paths)
            if len(self.input_files) == 1:
                self.pdf_path.set(self.input_files[0])
            else:
                self.pdf_path.set(f"{len(self.input_files)} {t['files_selected']}")
            
            # Atualiza a pasta de destino automaticamente SEMPRE para a mesma pasta do primeiro arquivo
            self.output_dir.set(os.path.dirname(self.input_files[0]))

    def select_output_dir(self):
        t = self.translations[self.lang.get()]
        dir_path = filedialog.askdirectory(title=t["dialog_dest_title"])
        if dir_path:
            self.output_dir.set(dir_path)

    def start_conversion_thread(self):
        t = self.translations[self.lang.get()]

        # Validações antes de iniciar
        if not self.input_files:
            messagebox.showwarning(t["warn_title"], t["warn_no_file"])
            return
        if not self.output_dir.get() or not os.path.isdir(self.output_dir.get()):
            messagebox.showwarning(t["warn_title"], t["warn_no_dest"])
            return

        # Desabilita o botão para evitar cliques duplos e atualiza o status
        self.btn_convert.configure(state="disabled", text=t["status_converting"])
        self.lbl_status.configure(text=t["status_batch"], text_color="yellow")
        self.progress_bar.set(0)

        # Roda a conversão em uma thread separada para não travar a interface gráfica (GUI)
        thread = threading.Thread(target=self.run_conversion)
        thread.daemon = True
        thread.start()

    def run_conversion(self):
        t = self.translations[self.lang.get()]
        target_format = self.output_format.get().lower()
        total_files = len(self.input_files)
        
        # Identifica o diretório onde o script está rodando para buscar o Calibre Portable
        base_dir = os.path.dirname(os.path.abspath(__file__))
        calibre_exe = os.path.join(base_dir, "Calibre Portable", "Calibre", "ebook-convert.exe")

        # Verifica se a pasta do Calibre Portable existe localmente. Se não, tenta usar o PATH do sistema
        if os.path.exists(calibre_exe):
            converter_cmd = calibre_exe
        else:
            converter_cmd = "ebook-convert"

        try:
            # Configuração para rodar invisível no Windows (sem abrir o CMD)
            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            success_count = 0
            
            # Loop que percorre os arquivos selecionados
            for i, input_file in enumerate(self.input_files):
                # Mensagem de progresso formatada com o idioma atual
                status_msg = t["converting_x_of_y"].format(i=i+1, total=total_files, filename=os.path.basename(input_file))
                self.lbl_status.configure(text=status_msg, text_color="yellow")
                self.progress_bar.set(i / total_files)

                # Cria o caminho do arquivo de saída
                base_name = os.path.splitext(os.path.basename(input_file))[0]
                output_file = os.path.join(self.output_dir.get(), f"{base_name}.{target_format}")

                # O comando que será executado invisivelmente
                command = [converter_cmd, input_file, output_file]
                
                # Desativa a capa genérica se o formato de saída for EPUB
                if target_format == "epub":
                    command.append("--no-default-epub-cover")

                # Executa o processo de conversão
                process = subprocess.run(
                    command,
                    startupinfo=startupinfo,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding='utf-8',           
                    errors='replace'            
                )

                # Verifica se a conversão do arquivo atual foi bem sucedida
                if process.returncode == 0 and os.path.exists(output_file):
                    success_count += 1

            # Finalização do loop do lote
            self.progress_bar.set(1.0)
            
            if success_count == total_files:
                final_msg = t["batch_done"].format(success=success_count, total=total_files)
                self.update_status(final_msg, "green", reset_btn=True)
            elif success_count > 0:
                final_msg = t["batch_partial"].format(success=success_count, total=total_files)
                self.update_status(final_msg, "yellow", reset_btn=True)
            else:
                self.update_status(t["batch_error"], "red", reset_btn=True)

        except FileNotFoundError:
            # Captura erro caso o motor de conversão não seja encontrado
            self.update_status(t["error_engine"], "red", reset_btn=True)
            self.progress_bar.set(0)
        except Exception as e:
            error_msg = t["error_unexpected"].format(error=str(e))
            self.update_status(error_msg, "red", reset_btn=True)
            self.progress_bar.set(0)

    def update_status(self, message, color, reset_btn=False):
        t = self.translations[self.lang.get()]
        # Atualiza a interface a partir da Thread de conversão
        self.lbl_status.configure(text=message, text_color=color)
        if reset_btn:
            self.btn_convert.configure(state="normal", text=t["btn_convert"])

if __name__ == "__main__":
    app = PDFConverterApp()
    app.mainloop()
