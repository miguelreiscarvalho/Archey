# Controle de Mouse por Expressões Faciais

Este projeto utiliza a biblioteca Mediapipe para rastrear expressões faciais em tempo real e controlar o mouse do computador com base nos movimentos detectados. O programa foi desenvolvido em Python e faz uso das seguintes bibliotecas:

- OpenCV (cv2): Para captura de vídeo, processamento de imagem e exibição.
- Mediapipe: Para detecção de pontos-chave no rosto, especialmente nos olhos, sobrancelhas e boca.
- Pynput: Para controle do mouse e do teclado.
- Tkinter: Para obter informações sobre as dimensões do monitor.
- SpeechRecognition: Para reconhecimento de voz.
- PyAutoGUI: Para realizar ações como clicar, pressionar e soltar teclas.

## Configuração

Antes de executar o programa, certifique-se de instalar as bibliotecas necessárias. Você pode fazer isso executando o seguinte comando:

```bash
pip install opencv-python mediapipe pynput pillow SpeechRecognition pyautogui
```

Além disso, este projeto utiliza um modelo de expressão facial da biblioteca Mediapipe, e a precisão pode variar. Certifique-se de estar em um ambiente bem iluminado para melhor detecção.

## Uso

1. Execute o programa.
2. A câmera será ativada, e as expressões faciais serão rastreadas.
3. Movimentos específicos, como piscar de olhos, movimentos de sobrancelhas ou movimentos da boca, podem ser configurados para realizar ações, como clicar, pressionar teclas ou movimentar o mouse.
4. Além disso, o controle por voz está habilitado. Algumas palavras-chave ativam ações específicas, como clicar, pressionar e soltar teclas.


## Controle Manual

- Ajuste a sensibilidade (`sensi_x` e `sensi_y`) para personalizar a velocidade do mouse.
- Use os pontos-chave do rosto, como os olhos e a boca, para controlar o mouse conforme desejado.

Lembre-se de encerrar o programa pressionando a tecla Esc.

**Nota:** A precisão do reconhecimento facial pode variar, e ajustes podem ser necessários para atender às suas preferências e ambiente de iluminação.
