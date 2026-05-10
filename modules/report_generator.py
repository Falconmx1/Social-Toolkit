#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Social Toolkit - Generador de Reportes
Crea reportes PDF y HTML de simulacros y detecciones
"""

import json
import argparse
from datetime import datetime
from pathlib import Path
import sys
try:
    from fpdf import FPDF
    HAS_FPDF = True
except ImportError:
    HAS_FPDF = False
    print("⚠️ FPDF no instalado. Los PDFs no estarán disponibles.")
    print("   Instala: pip install fpdf")

class ReportGenerator:
    def __init__(self):
        self.reportes_dir = Path("logs")
        self.reportes_dir.mkdir(exist_ok=True)
    
    def generar_html(self, datos, nombre_archivo="reporte.html"):
        """Generar reporte HTML"""
        html_content = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reporte Social Toolkit</title>
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: auto; background: white; padding: 20px; border-radius: 8px; }}
                h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
                h2 {{ color: #34495e; margin-top: 20px; }}
                .score {{ font-size: 24px; font-weight: bold; padding: 10px; border-radius: 5px; }}
                .score-high {{ background: #e74c3c; color: white; }}
                .score-medium {{ background: #f39c12; color: white; }}
                .score-low {{ background: #27ae60; color: white; }}
                table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #3498db; color: white; }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
                .warning {{ background: #ffeeee; border-left: 4px solid #e74c3c; padding: 10px; margin: 10px 0; }}
                .info {{ background: #eef9ff; border-left: 4px solid #3498db; padding: 10px; margin: 10px 0; }}
                footer {{ margin-top: 30px; text-align: center; font-size: 12px; color: #7f8c8d; }}
                .badge {{ display: inline-block; padding: 3px 8px; border-radius: 3px; font-size: 12px; }}
                .badge-high {{ background: #e74c3c; color: white; }}
                .badge-medium {{ background: #f39c12; color: white; }}
                .badge-low {{ background: #27ae60; color: white; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🛡️ Social Toolkit - Reporte de Seguridad</h1>
                <p><strong>Fecha:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Generado por:</strong> {datos.get('usuario', 'Sistema')}</p>
        """
        
        # Sección de resumen
        html_content += f"""
                <h2>📊 Resumen General</h2>
                <div class="info">
                    <strong>Tipo de reporte:</strong> {datos.get('tipo', 'General')}<br>
                    <strong>Total eventos analizados:</strong> {len(datos.get('eventos', []))}<br>
                    <strong>Riesgo detectado:</strong> 
                    <span class="badge badge-{datos.get('riesgo', 'low')}">{datos.get('riesgo', 'BAJO')}</span>
                </div>
        """
        
        # Tabla de eventos
        if datos.get('eventos'):
            html_content += """
                <h2>📋 Detalle de Eventos</h2>
                <table>
                    <thead>
                        <tr><th>ID</th><th>Timestamp</th><th>Nivel</th><th>Descripción</th></tr>
                    </thead>
                    <tbody>
            """
            
            for idx, evento in enumerate(datos.get('eventos', []), 1):
                nivel_color = {
                    'ALTO': 'badge-high',
                    'MEDIO': 'badge-medium',
                    'BAJO': 'badge-low'
                }.get(evento.get('nivel', 'BAJO'), 'badge-low')
                
                html_content += f"""
                    <tr>
                        <td>{idx}</td>
                        <td>{evento.get('timestamp', 'N/A')}</td>
                        <td><span class="badge {nivel_color}">{evento.get('nivel', 'BAJO')}</span></td>
                        <td>{evento.get('descripcion', 'Sin descripción')}</td>
                    </tr>
                """
            
            html_content += """
                    </tbody>
                </table>
            """
        
        # Recomendaciones
        html_content += """
                <h2>🔒 Recomendaciones de Seguridad</h2>
                <ul>
                    <li>Activar autenticación de dos factores (2FA) en todas las cuentas críticas</li>
                    <li>Realizar entrenamientos de phishing al menos cada 90 días</li>
                    <li>Configurar SPF, DKIM y DMARC para evitar suplantación de dominio</li>
                    <li>Implementar políticas de contraseñas robustas (mínimo 12 caracteres)</li>
                    <li>Establecer un canal de reporte de incidentes fácil y anónimo</li>
                </ul>
                
                <h2>📈 Estadísticas de la Industria</h2>
                <ul>
                    <li>El 90% de los breaches de datos involucran phishing (Informe DBIR 2023)</li>
                    <li>Los correos con urgencia tienen 40% más probabilidad de ser abiertos</li>
                    <li>Empresas con entrenamiento regular reducen riesgo de phishing en 70%</li>
                </ul>
                
                <footer>
                    <hr>
                    <p>Reporte generado por Social Toolkit - Uso educativo autorizado</p>
                    <p>Para más información: <a href="https://github.com/Falconmx1/Social-Toolkit">GitHub Repository</a></p>
                </footer>
            </div>
        </body>
        </html>
        """
        
        archivo_html = self.reportes_dir / nombre_archivo
        with open(archivo_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Reporte HTML generado: {archivo_html}")
        return archivo_html
    
    def generar_pdf(self, datos, nombre_archivo="reporte.pdf"):
        """Generar reporte PDF (requiere fpdf)"""
        if not HAS_FPDF:
            print("❌ FPDF no instalado. No se puede generar PDF.")
            return None
        
        class PDF(FPDF):
            def header(self):
                self.set_font('Arial', 'B', 12)
                self.cell(0, 10, 'Social Toolkit - Reporte de Seguridad', 0, 1, 'C')
                self.ln(10)
            
            def footer(self):
                self.set_y(-15)
                self.set_font('Arial', 'I', 8)
                self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')
        
        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)
        
        # Fecha
        pdf.cell(0, 10, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1)
        pdf.ln(5)
        
        # Resumen
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(0, 10, "Resumen General", 0, 1)
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 8, f"Tipo: {datos.get('tipo', 'General')}")
        pdf.multi_cell(0, 8, f"Eventos: {len(datos.get('eventos', []))}")
        pdf.multi_cell(0, 8, f"Riesgo: {datos.get('riesgo', 'BAJO')}")
        pdf.ln(5)
        
        # Eventos
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(0, 10, "Detalle de Eventos", 0, 1)
        
        for idx, evento in enumerate(datos.get('eventos', []), 1):
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(0, 8, f"Evento {idx}: {evento.get('nivel', 'N/A')}", 0, 1)
            pdf.set_font("Arial", size=9)
            pdf.multi_cell(0, 6, f"  • {evento.get('descripcion', 'Sin descripción')}")
            pdf.ln(2)
        
        archivo_pdf = self.reportes_dir / nombre_archivo
        pdf.output(str(archivo_pdf))
        print(f"✅ Reporte PDF generado: {archivo_pdf}")
        return archivo_pdf
    
    def cargar_logs_simulacro(self):
        """Cargar logs de simulacro y crear reporte"""
        eventos = []
        
        # Buscar archivos de log
        log_files = list(self.reportes_dir.glob("simulacro_*.txt"))
        
        for log_file in log_files:
            with open(log_file, 'r') as f:
                contenido = f.read()
                eventos.append({
                    'timestamp': log_file.stem.replace('simulacro_', ''),
                    'nivel': 'MEDIO',
                    'descripcion': f"Simulacro ejecutado: {contenido[:200]}..."
                })
        
        datos = {
            'tipo': 'Simulacro de Phishing',
            'usuario': 'Equipo de Seguridad',
            'riesgo': 'MEDIO',
            'eventos': eventos
        }
        
        return datos
    
    def cargar_logs_deteccion(self):
        """Cargar logs de detección y crear reporte"""
        eventos = []
        
        # Buscar archivos JSON de detección
        json_files = list(self.reportes_dir.glob("deteccion_*.json"))
        
        for json_file in json_files:
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                
                resultado = data.get('resultado', {})
                eventos.append({
                    'timestamp': data.get('fecha', 'N/A')[:19],
                    'nivel': resultado.get('nivel', 'BAJO'),
                    'descripcion': f"Correo analizado - Puntaje: {resultado.get('puntaje', 0)}/100"
                })
            except Exception as e:
                print(f"Error leyendo {json_file}: {e}")
        
        # Determinar nivel de riesgo general
        niveles = [e['nivel'] for e in eventos]
        if 'ALTO 🚨' in niveles:
            riesgo_general = 'ALTO'
        elif 'MEDIO ⚠️' in niveles:
            riesgo_general = 'MEDIO'
        else:
            riesgo_general = 'BAJO'
        
        datos = {
            'tipo': 'Detección de Phishing',
            'usuario': 'Sistema Automático',
            'riesgo': riesgo_general,
            'eventos': eventos
        }
        
        return datos

def main():
    parser = argparse.ArgumentParser(description='Generador de reportes')
    parser.add_argument('--log', '-l', help='Archivo de log específico')
    parser.add_argument('--type', '-t', choices=['simulacro', 'deteccion', 'all'], 
                        default='all', help='Tipo de reporte')
    parser.add_argument('--format', '-f', choices=['html', 'pdf', 'both'], 
                        default='html', help='Formato del reporte')
    
    args = parser.parse_args()
    
    generator = ReportGenerator()
    
    if args.type == 'simulacro':
        datos = generator.cargar_logs_simulacro()
    elif args.type == 'deteccion':
        datos = generator.cargar_logs_deteccion()
    else:
        # Combinar ambos
        datos_sim = generator.cargar_logs_simulacro()
        datos_det = generator.cargar_logs_deteccion()
        
        datos = {
            'tipo': 'Reporte Completo',
            'usuario': 'Equipo de Seguridad',
            'riesgo': 'MEDIO',  # Podría calcularse mejor
            'eventos': datos_sim.get('eventos', []) + datos_det.get('eventos', [])
        }
    
    nombre_base = f"reporte_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    if args.format in ['html', 'both']:
        generator.generar_html(datos, f"{nombre_base}.html")
    
    if args.format in ['pdf', 'both']:
        generator.generar_pdf(datos, f"{nombre_base}.pdf")
    
    print("\n✅ Reportes generados exitosamente")

if __name__ == "__main__":
    main()
