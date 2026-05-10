#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Social Toolkit - Detector de Phishing
Analiza correos en busca de indicadores maliciosos
"""

import re
import sys
import argparse
from urllib.parse import urlparse
import dns.resolver
from datetime import datetime
import json
from pathlib import Path

# Colores para output (opcional)
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

class PhishingDetector:
    def __init__(self):
        self.indicadores = []
        self.puntaje_total = 0
        self.max_puntaje = 100
        self.sospechoso = False
        
    def analizar_remitente(self, remitente):
        """Analizar dirección de remitente"""
        puntos = 0
        razones = []
        
        # Patrones sospechosos comunes
        patrones = [
            (r'(paypal|amazon|banco|seguridad|soporte)@\w+\.\w+', "Remitente genérico de soporte"),
            (r'\d+@', "Remitente con números aleatorios"),
            (r'(verify|update|secure|account)@', "Palabra clave en remitente"),
            (r'@\w+\.(tk|ml|ga|cf|gq|xyz)', "Dominio gratis/raros"),
        ]
        
        for patron, razon in patrones:
            if re.search(patron, remitente, re.IGNORECASE):
                puntos += 10
                razones.append(razon)
        
        # Verificar si el dominio tiene registros SPF/DKIM/DMARC
        dominio = remitente.split('@')[-1] if '@' in remitente else ''
        if dominio:
            try:
                # Intentar resolver MX
                mx_records = dns.resolver.resolve(dominio, 'MX')
                if not mx_records:
                    puntos += 15
                    razones.append("Dominio sin servidor MX válido")
            except:
                puntos += 20
                razones.append("Dominio no resuelve correctamente")
        
        return puntos, razones
    
    def analizar_asunto(self, asunto):
        """Analizar asunto del correo"""
        puntos = 0
        razones = []
        
        # Palabras de urgencia/emergencia
        palabras_urgencia = [
            'urgente', 'inmediato', 'verificar', 'actualizar', 'confirmar',
            'emergencia', 'alerta', 'suspend', 'bloqueado', 'seguridad',
            'cuenta', 'password', 'contraseña', 'factura', 'pago'
        ]
        
        for palabra in palabras_urgencia:
            if re.search(rf'\b{palabra}\b', asunto, re.IGNORECASE):
                puntos += 5
                razones.append(f"Palabra de urgencia: '{palabra}'")
        
        # Características sospechosas
        if re.search(r'!!+|!!!+', asunto):
            puntos += 10
            razones.append("Múltiples signos de exclamación")
        
        if re.search(r'[A-Z]{5,}', asunto):
            puntos += 8
            razones.append("Bloque de mayúsculas sospechoso")
        
        return puntos, razones
    
    def analizar_urls(self, cuerpo):
        """Analizar URLs en el cuerpo del correo"""
        puntos = 0
        razones = []
        
        # Encontrar todas las URLs
        urls = re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', cuerpo)
        
        for url in urls:
            url_puntos = 0
            url_razones = []
            
            # URL acortada
            acortadores = ['bit.ly', 'tinyurl.com', 'goo.gl', 'ow.ly', 'is.gd', 'buff.ly']
            for acortador in acortadores:
                if acortador in url.lower():
                    url_puntos += 15
                    url_razones.append(f"URL acortada con {acortador}")
                    break
            
            # Verificar si la URL tiene IP en lugar de dominio
            if re.match(r'https?://\d+\.\d+\.\d+\.\d+', url):
                url_puntos += 20
                url_razones.append("URL usa IP en lugar de dominio")
            
            # Dominios sospechosos
            try:
                parsed = urlparse(url)
                dominio = parsed.netloc.lower()
                
                # Verificar si intenta suplantar marca conocida
                marcas = ['paypal', 'amazon', 'microsoft', 'google', 'apple', 'facebook']
                for marca in marcas:
                    if marca in dominio and not dominio.endswith(f'.{marca}.com'):
                        url_puntos += 15
                        url_razones.append(f"Posible suplantación de {marca}")
                
                # Caracteres raros
                if '--' in dominio or re.search(r'[^a-z0-9\.\-]', dominio):
                    url_puntos += 10
                    url_razones.append("Caracteres inusuales en dominio")
                    
            except:
                url_puntos += 5
            
            if url_puntos > 0:
                puntos += min(url_puntos, 25)  # Máximo 25 puntos por URL
                razones.extend(url_razones)
        
        # Limitar puntos máximos de URLs
        puntos = min(puntos, 40)
        
        return puntos, razones
    
    def analizar_adjuntos(self, adjuntos):
        """Analizar nombres de archivos adjuntos"""
        puntos = 0
        razones = []
        
        extensiones_peligrosas = [
            '.exe', '.scr', '.bat', '.cmd', '.vbs', '.ps1', '.js',
            '.jar', '.app', '.msi', '.pif', '.reg'
        ]
        
        if adjuntos:
            for adjunto in adjuntos:
                extension = Path(adjunto).suffix.lower()
                if extension in extensiones_peligrosas:
                    puntos += 25
                    razones.append(f"Extensión peligrosa: {extension}")
                elif extension in ['.zip', '.rar', '.7z']:
                    puntos += 10
                    razones.append(f"Archivo comprimido: {extension} (puede contener malware)")
        
        return puntos, razones
    
    def analizar_html(self, cuerpo):
        """Analizar características HTML sospechosas"""
        puntos = 0
        razones = []
        
        # Formularios ocultos
        if 'display:none' in cuerpo or 'visibility:hidden' in cuerpo:
            puntos += 15
            razones.append("Formulario oculto detectado")
        
        # JavaScript inline
        if '<script' in cuerpo.lower():
            puntos += 20
            razones.append("Contiene JavaScript (posible redirección)")
        
        # DOM manipulation
        if 'document.' in cuerpo.lower() or 'window.' in cuerpo.lower():
            puntos += 15
            razones.append("Manipulación de DOM detectada")
        
        return puntos, razones
    
    def analizar_correo(self, remitente, asunto, cuerpo, adjuntos=None):
        """Análisis completo de un correo"""
        self.indicadores = []
        self.puntaje_total = 0
        
        if adjuntos is None:
            adjuntos = []
        
        # Ejecutar todos los análisis
        tipos_analisis = [
            ('Remitente', self.analizar_remitente(remitente)),
            ('Asunto', self.analizar_asunto(asunto)),
            ('URLs', self.analizar_urls(cuerpo)),
            ('HTML', self.analizar_html(cuerpo)),
            ('Adjuntos', self.analizar_adjuntos(adjuntos))
        ]
        
        for nombre, (puntos, razones) in tipos_analisis:
            self.puntaje_total += puntos
            if razones:
                self.indicadores.append({
                    'categoria': nombre,
                    'puntos': puntos,
                    'razones': razones
                })
        
        # Determinar nivel de riesgo
        self.puntaje_total = min(self.puntaje_total, self.max_puntaje)
        
        if self.puntaje_total >= 50:
            self.sospechoso = True
            nivel = "ALTO 🚨"
        elif self.puntaje_total >= 25:
            self.sospechoso = True
            nivel = "MEDIO ⚠️"
        else:
            nivel = "BAJO ✅"
        
        return {
            'puntaje': self.puntaje_total,
            'nivel': nivel,
            'sospechoso': self.sospechoso,
            'indicadores': self.indicadores
        }
    
    def generar_reporte_detallado(self, resultado):
        """Generar reporte visual del análisis"""
        print(f"\n{'='*60}")
        print(f"{Colors.BLUE}🔍 ANÁLISIS DE PHISHING - REPORTE{Colors.RESET}")
        print(f"{'='*60}")
        
        print(f"\n📊 Puntaje de riesgo: {resultado['puntaje']}/100")
        
        if resultado['nivel'] == "ALTO 🚨":
            print(f"{Colors.RED}⚠️  NIVEL: {resultado['nivel']}{Colors.RESET}")
        elif resultado['nivel'] == "MEDIO ⚠️":
            print(f"{Colors.YELLOW}⚠️  NIVEL: {resultado['nivel']}{Colors.RESET}")
        else:
            print(f"{Colors.GREEN}✅ NIVEL: {resultado['nivel']}{Colors.RESET}")
        
        if resultado['sospechoso']:
            print(f"\n{Colors.RED}🚨 ¡POSIBLE INTENTO DE PHISHING DETECTADO!{Colors.RESET}")
            print(f"\nIndicadores encontrados:")
            
            for indicador in resultado['indicadores']:
                print(f"\n  📌 {Colors.YELLOW}{indicador['categoria']}{Colors.RESET} (+{indicador['puntos']} pts)")
                for razon in indicador['razones']:
                    print(f"     • {razon}")
            
            print(f"\n{Colors.RED}🔒 RECOMENDACIONES:{Colors.RESET}")
            print("   1. NO hagas clic en enlaces ni descargues archivos")
            print("   2. Reporta este correo a seguridad@tuempresa.com")
            print("   3. Elimina el correo de tu bandeja")
            print("   4. Si hiciste clic, cambia tus contraseñas inmediatamente")
        else:
            print(f"\n{Colors.GREEN}✅ El correo parece legítimo según los análisis.{Colors.RESET}")
        
        print(f"\n{'='*60}")
        
        # Guardar reporte JSON
        reporte_json = {
            'fecha': datetime.now().isoformat(),
            'resultado': resultado
        }
        
        with open(f'logs/deteccion_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json', 'w') as f:
            json.dump(reporte_json, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Reporte guardado en logs/")

def main():
    parser = argparse.ArgumentParser(description='Detector de phishing')
    parser.add_argument('--email', '-e', help='Archivo .eml con el correo a analizar')
    parser.add_argument('--remitente', '-r', help='Dirección del remitente')
    parser.add_argument('--asunto', '-s', help='Asunto del correo')
    parser.add_argument('--cuerpo', '-c', help='Contenido del correo')
    
    args = parser.parse_args()
    
    detector = PhishingDetector()
    
    if args.email:
        try:
            with open(args.email, 'r', encoding='utf-8', errors='ignore') as f:
                contenido = f.read()
            
            # Extraer partes del email (simplificado)
            remitente_match = re.search(r'From:.*?[<]([^>]+)[>]', contenido, re.IGNORECASE)
            asunto_match = re.search(r'Subject:\s*(.+?)(?:\n|$)', contenido, re.IGNORECASE)
            
            remitente = remitente_match.group(1) if remitente_match else ""
            asunto = asunto_match.group(1) if asunto_match else ""
            cuerpo = contenido
            
            result = detector.analizar_correo(remitente, asunto, cuerpo)
            detector.generar_reporte_detallado(result)
            
        except Exception as e:
            print(f"❌ Error al leer archivo: {e}")
            sys.exit(1)
    
    elif args.remitente and args.asunto and args.cuerpo:
        result = detector.analizar_correo(args.remitente, args.asunto, args.cuerpo)
        detector.generar_reporte_detallado(result)
    
    else:
        print("Uso:")
        print("  python3 phishing_detector.py --email correo.eml")
        print("  python3 phishing_detector.py --remitente 'x@y.com' --asunto 'Alerta' --cuerpo 'Haz clic aquí'")
        sys.exit(1)

if __name__ == "__main__":
    main()
