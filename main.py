import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import json
from datetime import datetime
import csv

class ContadorMicroalgas:
    def __init__(self, root):
        self.root = root
        self.root.title("Contador de Microalgas")
        self.root.geometry("1300x800")
        
        # Configurar cores
        self.cores = {
            'primary': '#2196F3',    # Azul
            'success': '#4CAF50',    # Verde
            'warning': '#FFC107',    # Amarelo
            'danger': '#F44336',     # Vermelho
            'background': '#F5F5F5', # Cinza claro
            'text': '#212121'        # Texto escuro
        }
        
        # Configurar estilos
        self.configure_styles()
        
        # Variáveis de controle
        self.setup_variables()
        
        # Criar interface
        self.create_interface()
        
        # Carregar configurações
        self.load_settings()
        
    def configure_styles(self):
        """Configurar estilos personalizados"""
        # Estilo para frames
        self.style = ttk.Style()
        self.style.configure(
            "Card.TFrame",
            background=self.cores['background'],
            relief="raised",
            borderwidth=1
        )
        
        # Estilo para labels
        self.style.configure(
            "Title.TLabel",
            font=('Helvetica', 16, 'bold'),
            foreground=self.cores['primary'],
            background=self.cores['background']
        )
        
        self.style.configure(
            "Subtitle.TLabel",
            font=('Helvetica', 12),
            foreground=self.cores['text'],
            background=self.cores['background']
        )
        
        # Estilo para botões
        self.style.configure(
            "Primary.TButton",
            font=('Helvetica', 10, 'bold'),
            background=self.cores['primary']
        )
        
        self.style.configure(
            "Success.TButton",
            font=('Helvetica', 10, 'bold'),
            background=self.cores['success']
        )
        
    def setup_variables(self):
        """Inicializar variáveis"""
        self.current_image = None
        self.processed_image = None
        self.analysis_results = []
        
        # Parâmetros de detecção
        self.detection_params = {
            'min_dist': tk.IntVar(value=20),
            'sensibilidade': tk.IntVar(value=50),
            'acuracia': tk.IntVar(value=30),
            'min_radius': tk.IntVar(value=5),
            'max_radius': tk.IntVar(value=50)
        }
        
        # Estatísticas
        self.stats = {
            'total_count': tk.StringVar(value="0"),
            'avg_size': tk.StringVar(value="0.0"),
            'density': tk.StringVar(value="0.0")
        }
        
    def create_interface(self):
        """Criar interface principal"""
        # Container principal
        main_container = ttk.Frame(self.root, style="Card.TFrame")
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Cabeçalho
        self.create_header(main_container)
        
        # Área principal
        content = ttk.Frame(main_container)
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Painel de controle (esquerda)
        control_panel = self.create_control_panel(content)
        control_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Área de visualização (direita)
        view_panel = self.create_view_panel(content)
        view_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Painel de estatísticas (inferior)
        stats_panel = self.create_stats_panel(main_container)
        stats_panel.pack(fill=tk.X, padx=10, pady=5)
        
    def create_header(self, parent):
        """Criar cabeçalho"""
        header = ttk.Frame(parent, style="Card.TFrame")
        header.pack(fill=tk.X, padx=5, pady=5)
        
        # Título
        ttk.Label(
            header,
            text="Contador de Microalgas",
            style="Title.TLabel"
        ).pack(side=tk.LEFT, padx=10, pady=5)
        
        # Botões principais
        buttons_frame = ttk.Frame(header)
        buttons_frame.pack(side=tk.RIGHT, padx=10)
        
        ttk.Button(
            buttons_frame,
            text="Carregar Imagem",
            command=self.load_image,
            style="Primary.TButton"
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            buttons_frame,
            text="Contar Microalgas",
            command=self.process_image,
            style="Success.TButton"
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            buttons_frame,
            text="Exportar Resultados",
            command=self.export_results,
            style="Primary.TButton"
        ).pack(side=tk.LEFT, padx=5)
        
    def create_control_panel(self, parent):
        """Criar painel de controle"""
        control_frame = ttk.LabelFrame(
            parent,
            text="Parâmetros de Detecção",
            style="Card.TFrame"
        )
        
        # Parâmetros com descrições
        params = [
            ("Distância Mínima", self.detection_params['min_dist'],
             "Distância mínima entre microalgas (pixels)"),
            ("Sensibilidade", self.detection_params['sensibilidade'],
             "Sensibilidade na detecção de bordas"),
            ("Acurácia", self.detection_params['acuracia'],
             "Precisão na detecção de círculos"),
            ("Raio Mínimo", self.detection_params['min_radius'],
             "Tamanho mínimo das microalgas"),
            ("Raio Máximo", self.detection_params['max_radius'],
             "Tamanho máximo das microalgas")
        ]
        
        for param, var, desc in params:
            frame = ttk.Frame(control_frame)
            frame.pack(fill=tk.X, padx=10, pady=5)
            
            ttk.Label(
                frame,
                text=param,
                style="Subtitle.TLabel"
            ).pack(anchor=tk.W)
            
            ttk.Label(
                frame,
                text=desc,
                wraplength=200,
                style="Subtitle.TLabel"
            ).pack(anchor=tk.W)
            
            scale = ttk.Scale(
                frame,
                from_=1,
                to=100,
                variable=var,
                orient=tk.HORIZONTAL
            )
            scale.pack(fill=tk.X, pady=5)
        
        return control_frame
        
    def create_view_panel(self, parent):
        """Criar painel de visualização"""
        view_frame = ttk.Frame(parent, style="Card.TFrame")
        
        # Área de imagem original
        original_frame = ttk.LabelFrame(
            view_frame,
            text="Imagem Original",
            style="Card.TFrame"
        )
        original_frame.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.original_image_label = ttk.Label(original_frame)
        self.original_image_label.pack(padx=5, pady=5)
        
        # Área de imagem processada
        processed_frame = ttk.LabelFrame(
            view_frame,
            text="Contagem de Microalgas",
            style="Card.TFrame"
        )
        processed_frame.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.processed_image_label = ttk.Label(processed_frame)
        self.processed_image_label.pack(padx=5, pady=5)
        
        return view_frame
        
    def create_stats_panel(self, parent):
        """Criar painel de estatísticas"""
        stats_frame = ttk.LabelFrame(
            parent,
            text="Resultados da Análise",
            style="Card.TFrame"
        )
        
        # Grid de estatísticas
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack(fill=tk.X, padx=10, pady=5)
        
        # Total de microalgas
        total_frame = ttk.Frame(stats_grid)
        total_frame.pack(side=tk.LEFT, expand=True, padx=20)
        
        ttk.Label(
            total_frame,
            text="Total de Microalgas",
            style="Subtitle.TLabel"
        ).pack()
        
        ttk.Label(
            total_frame,
            textvariable=self.stats['total_count'],
            font=('Helvetica', 24, 'bold'),
            foreground=self.cores['primary']
        ).pack()
        
        # Tamanho médio
        size_frame = ttk.Frame(stats_grid)
        size_frame.pack(side=tk.LEFT, expand=True, padx=20)
        
        ttk.Label(
            size_frame,
            text="Tamanho Médio (pixels)",
            style="Subtitle.TLabel"
        ).pack()
        
        ttk.Label(
            size_frame,
            textvariable=self.stats['avg_size'],
            font=('Helvetica', 24, 'bold'),
            foreground=self.cores['success']
        ).pack()
        
        # Densidade
        density_frame = ttk.Frame(stats_grid)
        density_frame.pack(side=tk.LEFT, expand=True, padx=20)
        
        ttk.Label(
            density_frame,
            text="Densidade (microalgas/pixel²)",
            style="Subtitle.TLabel"
        ).pack()
        
        ttk.Label(
            density_frame,
            textvariable=self.stats['density'],
            font=('Helvetica', 24, 'bold'),
            foreground=self.cores['warning']
        ).pack()
        
        return stats_frame
        
    def load_image(self):
        """Carregar imagem"""
        file_path = filedialog.askopenfilename(
            title="Selecionar Imagem",
            filetypes=[
                ("Imagens", "*.png *.jpg *.jpeg *.tif *.tiff *.bmp"),
                ("Todos os arquivos", "*.*")
            ]
        )
        
        if file_path:
            self.current_image = cv2.imread(file_path)
            if self.current_image is None:
                messagebox.showerror(
                    "Erro",
                    "Não foi possível carregar a imagem"
                )
                return
            
            self.show_image(self.current_image, self.original_image_label)
            self.processed_image_label.configure(image='')
            self.reset_stats()
            
    def process_image(self):
        """Processar imagem e contar microalgas"""
        if self.current_image is None:
            messagebox.showerror(
                "Erro",
                "Por favor, carregue uma imagem primeiro"
            )
            return
        
        # Criar cópia da imagem
        img = self.current_image.copy()
        
        # Pré-processamento
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (9, 9), 2)
        
        # Detectar círculos
        circles = cv2.HoughCircles(
            blurred,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=self.detection_params['min_dist'].get(),
            param1=self.detection_params['sensibilidade'].get(),
            param2=self.detection_params['acuracia'].get(),
            minRadius=self.detection_params['min_radius'].get(),
            maxRadius=self.detection_params['max_radius'].get()
        )
        
        # Processar resultados
        result_image = img.copy()
        self.analysis_results = []
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            
            # Calcular estatísticas
            total_count = len(circles[0])
            avg_radius = np.mean([c[2] for c in circles[0]])
            image_area = img.shape[0] * img.shape[1]
            density = total_count / image_area
            
            # Atualizar estatísticas
            self.stats['total_count'].set(str(total_count))
            self.stats['avg_size'].set(f"{avg_radius:.1f}")
            self.stats['density'].set(f"{density*1e6:.2f}")
            
            # Marcar microalgas
            for i in circles[0, :]:
                # Converter cores de hex para BGR
                success_color = tuple(int(self.cores['success'].lstrip('#')[i:i+2], 16) for i in (4, 2, 0))
                danger_color = tuple(int(self.cores['danger'].lstrip('#')[i:i+2], 16) for i in (4, 2, 0))
                primary_color = tuple(int(self.cores['primary'].lstrip('#')[i:i+2], 16) for i in (4, 2, 0))
                
                # Desenhar círculo e centro
                cv2.circle(
                    result_image,
                    center=(int(i[0]), int(i[1])),
                    radius=int(i[2]),
                    color=success_color,
                    thickness=2
                )
                cv2.circle(
                    result_image,
                    center=(int(i[0]), int(i[1])),
                    radius=2,
                    color=danger_color,
                    thickness=3
                )
                
                # Adicionar número
                cv2.putText(
                    result_image,
                    str(len(self.analysis_results) + 1),
                    (int(i[0] - 10), int(i[1] - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    primary_color,
                    2
                )
                
                # Guardar resultados
                self.analysis_results.append({
                    'id': len(self.analysis_results) + 1,
                    'x': int(i[0]),
                    'y': int(i[1]),
                    'radius': int(i[2])
                })
        else:
            self.reset_stats()
            messagebox.showinfo(
                "Resultado",
                "Nenhuma microalga detectada com os parâmetros atuais"
            )
        
        self.processed_image = result_image
        self.show_image(result_image, self.processed_image_label)
        
    def export_results(self):
        """Exportar resultados da análise"""
        if not self.analysis_results:
            messagebox.showerror(
                "Erro",
                "Não há resultados para exportar"
            )
            return
        
        # Criar diretório para resultados
        output_dir = "resultados_analise"
        os.makedirs(output_dir, exist_ok=True)
        
        # Nome do arquivo baseado na data/hora
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Salvar imagem processada
        if self.processed_image is not None:
            image_path = os.path.join(
                output_dir,
                f"analise_microalgas_{timestamp}.jpg"
            )
            cv2.imwrite(image_path, self.processed_image)
        
        # Exportar dados para CSV
        csv_path = os.path.join(
            output_dir,
            f"dados_microalgas_{timestamp}.csv"
        )
        
        with open(csv_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=['id', 'x', 'y', 'radius']
            )
            writer.writeheader()
            writer.writerows(self.analysis_results)
        
        # Exportar relatório em texto
        report_path = os.path.join(
            output_dir,
            f"relatorio_microalgas_{timestamp}.txt"
        )
        
        with open(report_path, 'w') as f:
            f.write("Relatório de Análise de Microalgas\n")
            f.write("=================================\n\n")
            f.write(f"Data da análise: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"Total de microalgas: {self.stats['total_count'].get()}\n")
            f.write(f"Tamanho médio: {self.stats['avg_size'].get()} pixels\n")
            f.write(f"Densidade: {self.stats['density'].get()} microalgas/pixel²\n")
        
        messagebox.showinfo(
            "Sucesso",
            f"Resultados exportados para:\n{output_dir}"
        )
        
    def show_image(self, cv_image, label_widget):
        """Mostrar imagem no widget"""
        # Redimensionar imagem mantendo proporção
        height, width = cv_image.shape[:2]
        max_size = 400
        if height > max_size or width > max_size:
            scale = max_size / max(height, width)
            cv_image = cv2.resize(cv_image, None, fx=scale, fy=scale)
        
        # Converter para formato Tkinter
        image_rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_tk = ImageTk.PhotoImage(image_pil)
        
        label_widget.configure(image=image_tk)
        label_widget.image = image_tk
        
    def reset_stats(self):
        """Resetar estatísticas"""
        self.stats['total_count'].set("0")
        self.stats['avg_size'].set("0.0")
        self.stats['density'].set("0.0")
        
    def load_settings(self):
        """Carregar configurações salvas"""
        try:
            with open('config.json', 'r') as f:
                settings = json.load(f)
            
            for key, value in settings.items():
                if key in self.detection_params:
                    self.detection_params[key].set(value)
        except FileNotFoundError:
            pass
        
    def save_settings(self):
        """Salvar configurações atuais"""
        settings = {
            key: var.get()
            for key, var in self.detection_params.items()
        }
        
        with open('config.json', 'w') as f:
            json.dump(settings, f)

def main():
    root = tk.Tk()
    app = ContadorMicroalgas(root)
    root.mainloop()

if __name__ == "__main__":
    main() 