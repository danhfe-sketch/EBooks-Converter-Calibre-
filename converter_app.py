import os
import subprocess
import threading
import shlex
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
        self.geometry("600x580")
        self.resizable(False, False)

        # Variáveis de estado
        self.pdf_path = ctk.StringVar()
        self.input_files = []
        self.output_dir = ctk.StringVar()
        self.output_format = ctk.StringVar(value="EPUB")
        self.lang = ctk.StringVar(value="PT")
        
        # Controle do Dropdown de Parâmetros
        self.param_ids = ["none", "heavy_clean", "heuristics", "unwrap", "no_spacing", "tables", "font"]
        self.selected_param_id = "none"
        self.display_param = ctk.StringVar()

        # Dicionário de Traduções
        self.translations = {
            "PT": {
                "title": "Conversor de Arquivos para eBooks",
                "file_lbl": "Arquivo(s):",
                "btn_browse": "Procurar",
                "dest_lbl": "Salvar em:",
                "format_lbl": "Formato de Saída:",
                "extra_lbl": "Perfil de Correção:",
                "btn_convert": "Converter Lote Completo",
                "btn_test": "Testar Amostra (1º Arq)",
                "status_waiting": "Aguardando ação...",
                "status_converting": "Convertendo...",
                "status_batch": "Iniciando processamento...",
                "warn_no_file": "Por favor, selecione pelo menos um arquivo.",
                "warn_no_dest": "Por favor, selecione uma pasta de destino válida.",
                "warn_title": "Aviso",
                "dialog_files_title": "Selecione os arquivos",
                "dialog_dest_title": "Selecione a pasta de destino",
                "file_types": "eBooks e Documentos",
                "all_files": "Todos os Arquivos",
                "files_selected": "arquivos selecionados",
                "converting_x_of_y": "Convertendo {i} de {total}...\n{filename}",
                "batch_done": "Concluído! {success}/{total} arquivos convertidos.",
                "batch_partial": "Atenção: Apenas {success} de {total} foram convertidos com sucesso.",
                "batch_error": "Erro: Nenhum arquivo foi convertido. Verifique os formatos.",
                "error_engine": "Erro crítico: Motor de conversão não encontrado.",
                "error_unexpected": "Ocorreu um erro inesperado: {error}",
                "param_names": {
                    "none": "Nenhum (Padrão do Calibre)",
                    "heavy_clean": "Limpeza Pesada (Combo Recomendado)",
                    "heuristics": "Ativar Heurística Básica",
                    "unwrap": "Forçar Junção de Linhas",
                    "no_spacing": "Remover Espaçamento de Parágrafos",
                    "tables": "Desmontar Tabelas (Linearizar)",
                    "font": "Normalizar Tamanho da Fonte (12pt)"
                },
                "param_cmds": {
                    "none": "",
                    "heavy_clean": "--enable-heuristics --unwrap-lines --remove-paragraph-spacing",
                    "heuristics": "--enable-heuristics",
                    "unwrap": "--unwrap-lines",
                    "no_spacing": "--remove-paragraph-spacing",
                    "tables": "--linearize-tables",
                    "font": "--base-font-size 12"
                },
                "param_descs": {
                    "none": "Nenhuma alteração extra. O motor tentará converter da forma mais fiel ao arquivo original.",
                    "heavy_clean": "Ativa a IA, junta frases quebradas no meio e remove buracos em branco. Ideal para PDFs que ficam desformatados.",
                    "heuristics": "Usa cálculos matemáticos para tentar consertar parágrafos cortados e emendar palavras com hífen.",
                    "unwrap": "Força a junção de frases que o PDF quebrou fisicamente no meio da linha, melhorando a fluidez.",
                    "no_spacing": "Elimina grandes espaços em branco indesejados entre os parágrafos do texto.",
                    "tables": "Transforma tabelas complexas do PDF em texto corrido para não estourar a tela do leitor de eBook.",
                    "font": "Força o tamanho base do texto para 12pt, evitando que o EPUB fique com letras minúsculas ou gigantes."
                }
            },
            "EN": {
                "title": "File to eBook Converter",
                "file_lbl": "File(s):",
                "btn_browse": "Browse",
                "dest_lbl": "Save to:",
                "format_lbl": "Output Format:",
                "extra_lbl": "Fix Profile:",
                "btn_convert": "Convert Full Batch",
                "btn_test": "Test Sample (1st File)",
                "status_waiting": "Waiting for action...",
                "status_converting": "Converting...",
                "status_batch": "Starting processing...",
                "warn_no_file": "Please select at least one file.",
                "warn_no_dest": "Please select a valid destination folder.",
                "warn_title": "Warning",
                "dialog_files_title": "Select files",
                "dialog_dest_title": "Select destination folder",
                "file_types": "eBooks and Documents",
                "all_files": "All Files",
                "files_selected": "files selected",
                "converting_x_of_y": "Converting {i} of {total}...\n{filename}",
                "batch_done": "Complete! {success}/{total} files converted.",
                "batch_partial": "Attention: Only {success} of {total} converted successfully.",
                "batch_error": "Error: No files were converted. Check the formats.",
                "error_engine": "Critical Error: Conversion engine not found.",
                "error_unexpected": "An unexpected error occurred: {error}",
                "param_names": {
                    "none": "None (Calibre Default)",
                    "heavy_clean": "Heavy Clean (Recommended Combo)",
                    "heuristics": "Enable Basic Heuristics",
                    "unwrap": "Force Line Unwrapping",
                    "no_spacing": "Remove Paragraph Spacing",
                    "tables": "Linearize Tables",
                    "font": "Normalize Font Size (12pt)"
                },
                "param_cmds": {
                    "none": "",
                    "heavy_clean": "--enable-heuristics --unwrap-lines --remove-paragraph-spacing",
                    "heuristics": "--enable-heuristics",
                    "unwrap": "--unwrap-lines",
                    "no_spacing": "--remove-paragraph-spacing",
                    "tables": "--linearize-tables",
                    "font": "--base-font-size 12"
                },
                "param_descs": {
                    "none": "No extra changes. The engine will convert using its default structural analysis.",
                    "heavy_clean": "Enables AI, unwraps broken lines, and removes blank gaps. Best for messy or badly formatted PDFs.",
                    "heuristics": "Uses mathematical logic to fix cut-off paragraphs and mend hyphenated words.",
                    "unwrap": "Forces sentences physically broken by the PDF format to join together, improving text flow.",
                    "no_spacing": "Removes large, unwanted blank spaces between text paragraphs.",
                    "tables": "Converts complex PDF tables into continuous text so they don't break the eBook reader screen.",
                    "font": "Forces the base text size to 12pt, preventing the EPUB from having tiny or huge letters."
                }
            }
        }

        # Inicializa o valor de exibição do parâmetro
        t_init = self.translations[self.lang.get()]
        self.display_param.set(t_init["param_names"][self.selected_param_id])

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

        # Frame de Parâmetros Extras (Dropdown com Explicação)
        frame_extra = ctk.CTkFrame(self)
        frame_extra.pack(fill="x", padx=20, pady=(0, 10))

        self.lbl_extra = ctk.CTkLabel(frame_extra, text=t["extra_lbl"])
        self.lbl_extra.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nw")

        self.param_dropdown = ctk.CTkOptionMenu(
            frame_extra, 
            variable=self.display_param, 
            values=list(t["param_names"].values()), 
            command=self.on_param_select, 
            width=320
        )
        self.param_dropdown.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="w")

        self.lbl_param_desc = ctk.CTkLabel(
            frame_extra, 
            text=t["param_descs"][self.selected_param_id], 
            text_color="gray", 
            wraplength=350, 
            justify="left"
        )
        self.lbl_param_desc.grid(row=1, column=1, padx=10, pady=(5, 10), sticky="w")

        # Frame dos Botões (Teste e Conversão Lote)
        frame_buttons = ctk.CTkFrame(self, fg_color="transparent")
        frame_buttons.pack(pady=(10, 10))

        self.btn_test = ctk.CTkButton(frame_buttons, text=t["btn_test"], font=ctk.CTkFont(size=14, weight="bold"), height=40, fg_color="#5A5A5A", hover_color="#404040", command=lambda: self.start_conversion_thread(is_test=True))
        self.btn_test.pack(side="left", padx=10)

        self.btn_convert = ctk.CTkButton(frame_buttons, text=t["btn_convert"], font=ctk.CTkFont(size=15, weight="bold"), height=40, command=lambda: self.start_conversion_thread(is_test=False))
        self.btn_convert.pack(side="left", padx=10)

        # Barra de Progresso
        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.pack(pady=(0, 10))
        self.progress_bar.set(0)

        # Label de Status (Feedback para o usuário)
        self.lbl_status = ctk.CTkLabel(self, text=t["status_waiting"], text_color="gray")
        self.lbl_status.pack(pady=(0, 10))

    def on_param_select(self, choice):
        t = self.translations[self.lang.get()]
        # Encontra o ID do parâmetro selecionado com base no texto exibido
        for p_id, p_name in t["param_names"].items():
            if p_name == choice:
                self.selected_param_id = p_id
                break
        
        # Atualiza a label de descrição abaixo do dropdown
        self.lbl_param_desc.configure(text=t["param_descs"][self.selected_param_id])

    def change_language(self, choice):
        t = self.translations[choice]
        
        # Atualiza o dropdown de parâmetros
        new_values = list(t["param_names"].values())
        self.param_dropdown.configure(values=new_values)
        self.display_param.set(t["param_names"][self.selected_param_id])
        self.lbl_param_desc.configure(text=t["param_descs"][self.selected_param_id])

        # Atualiza os textos estáticos da interface
        self.title_label.configure(text=t["title"])
        self.lbl_file.configure(text=t["file_lbl"])
        self.btn_file.configure(text=t["btn_browse"])
        self.lbl_dest.configure(text=t["dest_lbl"])
        self.btn_dest.configure(text=t["btn_browse"])
        self.lbl_format.configure(text=t["format_lbl"])
        self.lbl_extra.configure(text=t["extra_lbl"])
        self.btn_test.configure(text=t["btn_test"])
        
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
            
            self.output_dir.set(os.path.dirname(self.input_files[0]))

    def select_output_dir(self):
        t = self.translations[self.lang.get()]
        dir_path = filedialog.askdirectory(title=t["dialog_dest_title"])
        if dir_path:
            self.output_dir.set(dir_path)

    def start_conversion_thread(self, is_test=False):
        t = self.translations[self.lang.get()]

        if not self.input_files:
            messagebox.showwarning(t["warn_title"], t["warn_no_file"])
            return
        if not self.output_dir.get() or not os.path.isdir(self.output_dir.get()):
            messagebox.showwarning(t["warn_title"], t["warn_no_dest"])
            return

        self.btn_convert.configure(state="disabled", text=t["status_converting"])
        self.btn_test.configure(state="disabled")
        self.lbl_status.configure(text=t["status_batch"], text_color="yellow")
        self.progress_bar.set(0)

        thread = threading.Thread(target=self.run_conversion, args=(is_test,))
        thread.daemon = True
        thread.start()

    def run_conversion(self, is_test):
        t = self.translations[self.lang.get()]
        target_format = self.output_format.get().lower()
        
        files_to_process = [self.input_files[0]] if is_test else self.input_files
        total_files = len(files_to_process)
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        calibre_exe = os.path.join(base_dir, "Calibre Portable", "Calibre", "ebook-convert.exe")

        if os.path.exists(calibre_exe):
            converter_cmd = calibre_exe
        else:
            converter_cmd = "ebook-convert"

        last_output_file = ""

        try:
            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            success_count = 0
            
            for i, input_file in enumerate(files_to_process):
                status_msg = t["converting_x_of_y"].format(i=i+1, total=total_files, filename=os.path.basename(input_file))
                self.lbl_status.configure(text=status_msg, text_color="yellow")
                self.progress_bar.set(i / total_files)

                base_name = os.path.splitext(os.path.basename(input_file))[0]
                output_file = os.path.join(self.output_dir.get(), f"{base_name}.{target_format}")

                # Proteção contra colisão de arquivos
                if os.path.abspath(input_file) == os.path.abspath(output_file):
                    output_file = os.path.join(self.output_dir.get(), f"{base_name}_corrigido.{target_format}")

                command = [converter_cmd, input_file, output_file]
                
                # Desativa a capa genérica para EPUBs
                if target_format == "epub":
                    command.append("--no-default-epub-cover")

                # Injeta os comandos mapeados do Dropdown
                extra_cmd = t["param_cmds"][self.selected_param_id]
                if extra_cmd:
                    command.extend(shlex.split(extra_cmd))

                process = subprocess.run(
                    command,
                    startupinfo=startupinfo,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding='utf-8',           
                    errors='replace'            
                )

                if process.returncode == 0 and os.path.exists(output_file):
                    success_count += 1
                    last_output_file = output_file

            self.progress_bar.set(1.0)
            
            if success_count == total_files:
                final_msg = t["batch_done"].format(success=success_count, total=total_files)
                self.update_status(final_msg, "green", reset_btn=True)
                
                if is_test and last_output_file and os.name == 'nt':
                    os.startfile(last_output_file)

            elif success_count > 0:
                final_msg = t["batch_partial"].format(success=success_count, total=total_files)
                self.update_status(final_msg, "yellow", reset_btn=True)
            else:
                self.update_status(t["batch_error"], "red", reset_btn=True)

        except FileNotFoundError:
            self.update_status(t["error_engine"], "red", reset_btn=True)
            self.progress_bar.set(0)
        except Exception as e:
            error_msg = t["error_unexpected"].format(error=str(e))
            self.update_status(error_msg, "red", reset_btn=True)
            self.progress_bar.set(0)

    def update_status(self, message, color, reset_btn=False):
        t = self.translations[self.lang.get()]
        self.lbl_status.configure(text=message, text_color=color)
        if reset_btn:
            self.btn_convert.configure(state="normal", text=t["btn_convert"])
            self.btn_test.configure(state="normal")

if __name__ == "__main__":
    app = PDFConverterApp()
    app.mainloop()
