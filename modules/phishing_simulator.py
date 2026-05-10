#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Social Toolkit - Simulador de Phishing Controlado
Uso exclusivo para pruebas autorizadas
"""

import smtplib
import argparse
import logging
import configparser
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path
import sys
import time

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/simulacro.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PhishingSimulator:
    def __init__(self, config_file='config/settings.ini'):
        """Inicializar simulador con configuración"""
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.cargar_plantillas()
        
    def cargar_plantillas(self):
        """Cargar plantillas de correo disponibles"""
        self.plantillas = {}
        templates_dir = Path('templates')
        if templates_dir.exists():
            for template_file in templates_dir.glob('*.html'):
                with open(template_file, 'r', encoding='utf-8') as f:
                    nombre = template_file.stem
                    self.plantillas[nombre] = f.read()
        
        # Plantilla por defecto si no hay archivos
        if not self.plantillas:
            self.plantillas['default'] = """
            <html>
            <body>
                <h2>Alerta de Seguridad</h2>
                <p>Estimado/a {nombre},</p>
                <p>Este es un <strong>SIMULACRO DE SEGURIDAD</strong> autorizado.</p>
                <p>Haz clic para aprender sobre seguridad: 
                <a href="https://{dominio}/training">Ir al entrenamiento</a></p>
                <hr>
                <small>Simulacro autorizado - No compartas este correo</small>
            </body>
            </html>
            """
    
    def cargar_whitelist(self):
        """Cargar lista de destinatarios autorizados"""
        whitelist_file = Path('config/whitelist.txt')
        if not whitelist_file.exists():
            logger.error("Archivo whitelist.txt no encontrado")
            return []
        
        with open(whitelist_file, 'r') as f:
            correos = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        return correos
    
    def validar_destinatario(self, email):
        """Validar que el destinatario está autorizado"""
        whitelist = self.cargar_whitelist()
        if email not in whitelist:
            logger.warning(f"Destinatario no autorizado: {email}")
            return False
        
        # Verificar dominio permitido
        dominio = email.split('@')[-1]
        allowed_domains = self.config['Security']['allowed_domains'].split(',')
        
        if dominio not in allowed_domains:
            logger.warning(f"Dominio no permitido: {dominio}")
            return False
        
        return True
    
    def enviar_correo(self, destinatario, asunto, cuerpo_html, remitente=None):
        """Enviar correo electrónico"""
        if not self.validar_destinatario(destinatario):
            return False
        
        if remitente is None:
            remitente = f"security@{self.config['Security']['allowed_domains'].split(',')[0]}"
        
        # Crear mensaje
        msg = MIMEMultipart('alternative')
        msg['Subject'] = asunto
        msg['From'] = remitente
        msg['To'] = destinatario
        
        # Versión texto plano
        texto_plano = re.sub(r'<[^>]+>', '', cuerpo_html)
        msg.attach(MIMEText(texto_plano, 'plain'))
        msg.attach(MIMEText(cuerpo_html, 'html'))
        
        try:
            # Configurar conexión SMTP
            smtp_config = self.config['SMTP']
            if smtp_config.getboolean('use_tls'):
                server = smtplib.SMTP(smtp_config['smtp_server'], int(smtp_config['smtp_port']))
                server.starttls()
            else:
                server = smtplib.SMTP(smtp_config['smtp_server'], int(smtp_config['smtp_port']))
            
            if smtp_config['smtp_user']:
                server.login(smtp_config['smtp_user'], smtp_config['smtp_password'])
            
            server.sendmail(remitente, destinatario, msg.as_string())
            server.quit()
            
            logger.info(f"Correo enviado a {destinatario}")
            return True
            
        except Exception as e:
            logger.error(f"Error enviando a {destinatario}: {e}")
            return False
    
    def simular(self, plantilla='default', limite=10):
        """Ejecutar simulación de phishing"""
        destinatarios = self.cargar_whitelist()
        
        if not destinatarios:
            logger.error("No hay destinatarios autorizados")
            return
        
        logger.info(f"Iniciando simulacro de phishing - Plantilla: {plantilla}")
        logger.info(f"Total destinatarios: {len(destinatarios)}")
        
        enviados = 0
        fallidos = 0
        limite_por_minuto = int(self.config['Security']['max_emails_per_minute'])
        
        for idx, destinatario in enumerate(destinatarios[:limite]):
            # Preparar asunto según plantilla
            asuntos = {
                'pwd': 'Alerta: Actualiza tu contraseña ahora',
                'factura': 'Factura pendiente - Acción requerida',
                'notificacion': 'Notificación importante de seguridad'
            }
            asunto = asuntos.get(plantilla, 'Simulacro de Seguridad')
            
            # Personalizar cuerpo
            nombre = destinatario.split('@')[0]
            dominio = self.config['Security']['allowed_domains'].split(',')[0]
            cuerpo = self.plantillas.get(plantilla, self.plantillas['default']).format(
                nombre=nombre,
                dominio=dominio
            )
            
            # Enviar
            if self.enviar_correo(destinatario, asunto, cuerpo):
                enviados += 1
            else:
                fallidos += 1
            
            # Rate limiting
            if (idx + 1) % limite_por_minuto == 0:
                logger.info(f"Esperando 60 segundos... enviados: {enviados}")
                time.sleep(60)
        
        logger.info(f"Simulacro completado - Enviados: {enviados}, Fallidos: {fallidos}")
        
        # Generar reporte automáticamente
        self.generar_reporte_simple(enviados, fallidos, plantilla)
    
    def generar_reporte_simple(self, enviados, fallidos, plantilla):
        """Generar reporte simple del simulacro"""
        reporte = f"""
        ========================================
        REPORTE DE SIMULACRO DE PHISHING
        ========================================
        Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        Plantilla: {plantilla}
        
        Estadísticas:
        - Total enviados: {enviados}
        - Fallidos: {fallidos}
        - Tasa de éxito: {(enviados/(enviados+fallidos))*100 if (enviados+fallidos)>0 else 0:.1f}%
        
        Advertencia: Este es un simulacro autorizado.
        """
        
        with open(f'logs/simulacro_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt', 'w') as f:
            f.write(reporte)
        
        logger.info("Reporte guardado en logs/")

def main():
    parser = argparse.ArgumentParser(description='Simulador de phishing controlado')
    parser.add_argument('--template', '-t', choices=['pwd', 'factura', 'notificacion', 'default'],
                        default='default', help='Plantilla de correo')
    parser.add_argument('--targets', '-f', help='Archivo con lista de destinatarios (opcional)')
    parser.add_argument('--limit', '-l', type=int, default=10, help='Límite de correos')
    
    args = parser.parse_args()
    
    # Verificar configuración
    if not Path('config/settings.ini').exists():
        print("❌ Configuración no encontrada. Ejecuta primero ./install.sh")
        sys.exit(1)
    
    simulator = PhishingSimulator()
    simulator.simular(args.template, args.limit)

if __name__ == "__main__":
    main()
