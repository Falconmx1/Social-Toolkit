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
echo ""

# Pregunta 6
TOTAL=$((TOTAL+1))
echo -e "${BLUE}[Pregunta $TOTAL]${NC}"
echo -e "¿Qué hacer SI YA hiciste clic en un enlace sospechoso?"
echo -e "   a) Ignorarlo, probablemente no pasó nada"
echo -e "   b) Cambiar contraseñas inmediatamente y reportar a TI"
echo -e "   c) Borrar el historial del navegador"
echo -e "   d) Apagar la computadora"
read -p "Tu respuesta (a/b/c/d): " ans6

if [[ "$ans6" == "b" ]]; then
    echo -e "${GREEN}✅ Correcto! La acción rápida puede mitigar el daño.${NC}"
    SCORE=$((SCORE+1))
else
    echo -e "${RED}❌ Debes cambiar contraseñas y notificar a seguridad inmediatamente.${NC}"
fi
echo ""

# Pregunta 7
TOTAL=$((TOTAL+1))
echo -e "${BLUE}[Pregunta $TOTAL]${NC}"
echo -e "¿Qué extensión de archivo es la MÁS PELIGROSA para recibir adjunta?"
echo -e "   a) .pdf"
echo -e "   b) .jpg"
echo -e "   c) .exe"
echo -e "   d) .txt"
read -p "Tu respuesta (a/b/c/d): " ans7

if [[ "$ans7" == "c" ]]; then
    echo -e "${GREEN}✅ Correcto! Los .exe son ejecutables que pueden instalar malware.${NC}"
    SCORE=$((SCORE+1))
else
    echo -e "${RED}❌ Los archivos .exe ejecutan código y son muy peligrosos.${NC}"
fi
echo ""

# Pregunta 8
TOTAL=$((TOTAL+1))
echo -e "${BLUE}[Pregunta $TOTAL]${NC}"
echo -e "¿Qué es el 'spear phishing'?"
echo -e "   a) Un ataque masivo sin objetivo específico"
echo -e "   b) Un ataque dirigido a una persona u organización específica"
echo -e "   c) Un tipo de firewall"
echo -e "   d) Un antivirus gratuito"
read -p "Tu respuesta (a/b/c/d): " ans8

if [[ "$ans8" == "b" ]]; then
    echo -e "${GREEN}✅ Correcto! Spear phishing es altamente dirigido y peligroso.${NC}"
    SCORE=$((SCORE+1))
else
    echo -e "${RED}❌ El spear phishing personaliza el ataque para una víctima específica.${NC}"
fi
echo ""

# Pregunta 9
TOTAL=$((TOTAL+1))
echo -e "${BLUE}[Pregunta $TOTAL]${NC}"
echo -e "Característica SEGURA en un sitio web:"
echo -e "   a) Muestra candado verde (HTTPS válido)"
echo -e "   b) Pide credenciales después de un enlace de correo"
echo -e "   c) Tiene errores ortográficos"
echo -e "   d) El dominio tiene números extraños"
read -p "Tu respuesta (a/b/c/d): " ans9

if [[ "$ans9" == "a" ]]; then
    echo -e "${GREEN}✅ Correcto! HTTPS y candado verifican identidad y cifrado.${NC}"
    SCORE=$((SCORE+1))
else
    echo -e "${RED}❌ Siempre verifica el candado verde y que el certificado sea válido.${NC}"
fi
echo ""

# Pregunta 10
TOTAL=$((TOTAL+1))
echo -e "${BLUE}[Pregunta $TOTAL]${NC}"
echo -e "¿Cada cuánto deberías cambiar tus contraseñas corporativas?"
echo -e "   a) Nunca"
echo -e "   b) Cada 30-90 días según política de seguridad"
echo -e "   c) Solo si me la roban"
echo -e "   d) Cada año"
read -p "Tu respuesta (a/b/c/d): " ans10

if [[ "$ans10" == "b" ]]; then
    echo -e "${GREEN}✅ Correcto! Rotación periódica reduce riesgos.${NC}"
    SCORE=$((SCORE+1))
else
    echo -e "${RED}❌ Seguir la política de seguridad de tu empresa.${NC}"
fi
echo ""

# Resultados
PERCENTAGE=$((SCORE * 100 / TOTAL))

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                   RESULTADOS DEL TEST                     ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo -e "📊 Puntaje: ${YELLOW}$SCORE / $TOTAL${NC} (${PERCENTAGE}%)"

if [[ $PERCENTAGE -ge 90 ]]; then
    echo -e "${GREEN}🌟 Excelente! Tienes muy buena conciencia de seguridad.${NC}"
    echo -e "${GREEN}   Comparte este conocimiento con tus compañeros.${NC}"
elif [[ $PERCENTAGE -ge 70 ]]; then
    echo -e "${YELLOW}👍 Bien, pero hay áreas de mejora. Revisa las explicaciones.${NC}"
elif [[ $PERCENTAGE -ge 50 ]]; then
    echo -e "${RED}⚠️  Riesgo medio. Te recomendamos más entrenamiento.${NC}"
else
    echo -e "${RED}🚨 ALTO RIESGO. Necesitas capacitación urgente en seguridad.${NC}"
fi

echo ""
echo -e "${YELLOW}📝 Recomendaciones finales:${NC}"
echo "   • Siempre verifica remitentes y URLs antes de hacer clic"
echo "   • Activa autenticación de dos factores (2FA/MFA)"
echo "   • Reporta correos sospechosos a seguridad@tuempresa.com"
echo "   • Mantén actualizados tus sistemas y antivirus"
echo ""

# Guardar resultado
mkdir -p logs
echo "$(date) - Usuario: $USER - Score: $SCORE/$TOTAL ($PERCENTAGE%)" >> logs/training_history.log

echo -e "${GREEN}✅ Entrenamiento completado. Historial guardado en logs/${NC}"
