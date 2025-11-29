# --- REDE ---
# IP do servidor do jogo (Visão)
# Pac-Man: "192.168.1.101"
# Rocket League: "192.168.1.106"

IP_GAME_SERVER = "192.168.1.106"
PORT_GAME_SERVER = "8765"

# IP do seu Robô (ESP32)
# "car_rosa": "121",
# "car_azul": "122",
# "pac_man": "116",
# "fant_azul": "119",
# "fant_rosa": "117",
# "fant_verm": "118",
# "fant_verd": "120",

IP_ROBOT = "192.168.1.122"
PORT_ROBOT = "81"

# --- IDENTIDADE ---
# O nome deve ser EXATAMENTE igual ao enviado pelo JSON da visão
MEU_NOME = "carro_1"
NOME_BOLA = "bola"

# --- PARAMETROS DE MOVIMENTO (0 a 255) ---
VEL_CRUZEIRO = 180
VEL_ATAQUE = 255
VEL_GIRAR = 130
VEL_RE = -150
FATOR_AJUSTE = 1.3

# --- ESTRATÉGIA ---
# Defina o X do gol adversário.
# Se o campo tem 160cm de largura:
# Gol Esquerda = 0, Gol Direita = 160 (Verifique no servidor da arena!)
GOL_ALVO_X = 160
GOL_ALVO_Y = 65  # Metade da altura Y (se o campo tiver 130cm de altura)

# Distância em cm para ficar atrás da bola antes de chutar
OFFSET_CHUTE = 15

# Distância para considerar que já pode atacar (chutar)
DISTANCIA_CHUTE = 150  # Pixels
LIMITE_TRAVAMENTO = 10
