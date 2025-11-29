# manual_control.py
import json
import sys
import time

import config  # Importa as configurações do seu projeto
import pygame
import websocket

# --- CONFIGURAÇÃO DE VELOCIDADE MANUAL ---
VEL_FRENTE = 50
VEL_ESQ = 100
VEL_DIR = 90


def connect_robot():
    uri = f"ws://{config.IP_ROBOT}:{config.PORT_ROBOT}"
    print(f"Conectando ao Robô em {uri}...")
    try:
        ws = websocket.create_connection(uri, timeout=1)
        print("CONECTADO! Use WASD ou Setas para mover.")
        return ws
    except Exception as e:
        print(f"Erro ao conectar: {e}")
        return None


def send_cmd(ws, m1, m2):
    if not ws:
        return
    try:
        msg = json.dumps({"motor1_vel": int(m1), "motor2_vel": int(m2)})
        ws.send(msg)
    except Exception as e:
        print(f"Erro no envio: {e}")


def main():
    pygame.init()
    # Cria uma janela pequena (necessária para capturar o teclado)
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Controle Manual - Mecathron")
    font = pygame.font.Font(None, 30)
    clock = pygame.time.Clock()

    ws = connect_robot()
    if not ws:
        print("Não foi possível conectar ao robô. Verifique o IP no config.py")
        sys.exit()

    running = True
    last_cmd = (0, 0)

    try:
        while running:
            # 1. Processa Eventos (Fechar janela)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # 2. Captura Teclado
            keys = pygame.key.get_pressed()

            m1, m2 = 0, 0
            status = "PARADO"

            # Lógica de Movimento (Estilo Tanque)
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                m1 = VEL_ESQ
                m2 = VEL_DIR
                status = "FRENTE"
                # Permite curvas enquanto anda
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    m1 -= 50  # Reduz motor esquerdo
                    status = "CURVA ESQ"
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    m2 -= 50  # Reduz motor direito
                    status = "CURVA DIR"

            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                m1 = -VEL_ESQ
                m2 = -VEL_DIR
                status = "RÉ"
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    m1 += 50
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    m2 += 50

            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                # Giro no próprio eixo
                m1 = -VEL_ESQ / 2
                m2 = VEL_DIR / 2
                status = "GIRANDO ESQ"

            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                # Giro no próprio eixo
                m1 = VEL_ESQ / 2
                m2 = -VEL_DIR / 2
                status = "GIRANDO DIR"

            # Tecla de Emergência (Espaço)
            if keys[pygame.K_SPACE]:
                m1, m2 = 0, 0
                status = "FREIO DE MÃO"

            # 3. Envia comando apenas se mudou (para não saturar a rede) ou a cada X frames
            # Aqui envia sempre para garantir responsividade, mas pode filtrar
            send_cmd(ws, m1, m2)

            # 4. Atualiza Interface
            screen.fill((50, 50, 50))

            text_status = font.render(f"Status: {status}", True, (0, 255, 0))
            text_motores = font.render(f"M1: {m1} | M2: {m2}", True, (255, 255, 255))
            text_info = font.render("Use WASD para mover", True, (200, 200, 200))

            screen.blit(text_status, (20, 20))
            screen.blit(text_motores, (20, 60))
            screen.blit(text_info, (20, 100))

            pygame.display.flip()
            clock.tick(20)  # 20 Hz (Comandos por segundo)

    except KeyboardInterrupt:
        pass
    finally:
        send_cmd(ws, 0, 0)
        ws.close()
        pygame.quit()
        print("Controle encerrado.")


if __name__ == "__main__":
    main()
