#!/bin/bash
# Social Toolkit - Módulo de entrenamiento interactivo
# Concienciación sobre phishing y seguridad

#!/bin/bash

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCORE=0
TOTAL=0

clear
echo -e "${BLUE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     🛡️  MÓDULO DE ENTRENAMIENTO - PHISHING AWARENESS      ║
║                                                           ║
║      Aprende a identificar ataques de ingeniería social   ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${YELLOW}📋 Este entrenamiento te ayudará a reconocer intentos de phishing.${NC}"
echo -e "${YELLOW}Responde las siguientes preguntas:\n${NC}"
sleep 2

# Pregunta 1
TOTAL=$((TOTAL+1))
echo -e "${BLUE}[Pregunta $TOTAL]${NC}"
echo -e "¿Qué es el phishing?"
echo -e "   a) Un tipo de malware"
echo -e "   b) Una técnica para engañar y obtener información confidencial"
echo -e "   c) Un antivirus"
echo -e "   d) Un firewall"
read -p "Tu respuesta (a/b/c/d): " ans1

if [[ "$ans1" == "b" ]]; then
    echo -e "${GREEN}✅ Correcto!${NC}"
    SCORE=$((SCORE+1))
else
    echo -e "${RED}❌ Incorrecto. El phishing es una técnica de engaño para obtener información.${NC}"
fi
echo ""

# Pregunta 2
TOTAL=$((TOTAL+1))
echo -e "${BLUE}[Pregunta $TOTAL]${NC}"
echo -e "¿Qué indicador es sospechoso en un correo?"
echo -e "   a) Tiene mi nombre correcto"
echo -e "   b) Solicita hacer clic en un enlace para 'verificar cuenta' urgentemente"
echo -e "   c) Viene de mi jefe directo"
echo -e "   d) El dominio del remitente coincide con mi empresa"
read -p "Tu respuesta (a/b/c/d): " ans2

if [[ "$ans2" == "b" ]]; then
    echo -e "${GREEN}✅ Correcto!${NC}"
    SCORE=$((SCORE+1))
    echo -e "${YELLOW}💡 Las peticiones urgentes de acción son una táctica común.${NC}"
else
    echo -e "${RED}❌ Las peticiones urgentes para verificar datos son muy sospechosas.${NC}"
fi
echo ""

# Pregunta 3
TOTAL=$((TOTAL+1))
echo -e "${BLUE}[Pregunta $TOTAL]${NC}"
echo -e "Recibes un correo de 'soporte@paypal-seguro.com' pidiendo actualizar tu cuenta. ¿Qué haces?"
echo -e "   a) Hago clic en el enlace inmediatamente"
echo -e "   b) Verifico manualmente en el sitio oficial de PayPal sin usar el enlace"
echo -e "   c) Reenvió el correo a todos mis compañeros"
echo -e "   d) Respondo con mi contraseña para 'verificar'"
read -p "Tu respuesta (a/b/c/d): " ans3

if [[ "$ans3" == "b" ]]; then
    echo -e "${GREEN}✅ Correcto! Siempre verifica manualmente en el sitio oficial.${NC}"
    SCORE=$((SCORE+1))
else
    echo -e "${RED}❌ Nunca uses enlaces de correos sospechosos. Ve directamente al sitio oficial.${NC}"
fi
echo ""

# Pregunta 4
TOTAL=$((TOTAL+1))
echo -e "${BLUE}[Pregunta $TOTAL]${NC}"
echo -e "¿Qué hace un atacante con tu información obtenida mediante phishing?"
echo -e "   a) La borra"
echo -e "   b) Roba identidad, dinero o acceso a sistemas"
echo -e "   c) Te envía regalos"
echo -e "   d) La pública en redes sociales"
read -p "Tu respuesta (a/b/c/d): " ans4

if [[ "$ans4" == "b" ]]; then
    echo -e "${GREEN}✅ Correcto!${NC}"
    SCORE=$((SCORE+1))
else
    echo -e "${RED}❌ El phishing busca robar información para cometer fraudes.${NC}"
fi
echo ""

# Pregunta 5
TOTAL=$((TOTAL+1))
echo -e "${BLUE}[Pregunta $TOTAL]${NC}"
echo -e "¿Cuál es un indicador claro de phishing en una URL?"
echo -e "   a) https://www.google.com"
echo -e "   b) http://paypal.verificacion-segura.com/login"
echo -e "   c) https://github.com/Falconmx1"
echo -e "   d) http://192.168.1.1"
read -p "Tu respuesta (a/b/c/d): " ans5

if [[ "$ans5" == "b" ]]; then
    echo -e "${GREEN}✅ Correcto! Dominios con nombres sospechosos que simulan marcas.${NC}"
    SCORE=$((SCORE+1))
else
    echo -e "${RED}❌ Dominios extraños que no coinciden exactamente con la marca real.${NC}"
fi
