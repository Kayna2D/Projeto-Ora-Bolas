from math import *
from random import *
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
import json

def interceptar(robo, bola, tempo):

  if (bola['y'] - robo['y']) == 0:
    tend = 0.00000000000000001
    mod_tan = sqrt(((bola['x'] - robo['x'])/(tend))**2)
  else:
    mod_tan = sqrt(((bola['x'] - robo['x'])/(bola['y'] - robo['y']))**2)

  angulo = atan(mod_tan)

  bola['distancia'] = sqrt((bola['x'] - robo['x'])**2 + (bola['y'] - robo['y'])**2)

  if bola['distancia'] >= 2.8:
    robo['vel_max'] = 2.8
    robo['acc'] = 2.8
  elif (bola['distancia'] >= 2.5) and (bola['distancia'] < 2.8):
    robo['vel_max'] = 2.5
    robo['acc'] = 1.25
  elif (bola['distancia'] >= 2.2) and (bola['distancia'] < 2.5):
    robo['vel_max'] = 2.2
    robo['acc'] = 1.1
  elif (bola['distancia'] >= 1.9) and (bola['distancia'] < 2.2):
    robo['vel_max'] = 1.9
    robo['acc'] = 0.95
  elif (bola['distancia'] >= 1.6) and (bola['distancia'] < 1.9):
    robo['vel_max'] = 1.6
    robo['acc'] = 0.8
  elif (bola['distancia'] >= 1.3) and (bola['distancia'] < 1.6):
    robo['vel_max'] = 1.3
    robo['acc'] = 0.65
  elif (bola['distancia'] >= 1.0) and (bola['distancia'] < 1.3):
    robo['vel_max'] = 1.0
    robo['acc'] = 0.5
  elif (bola['distancia'] >= 0.7) and (bola['distancia'] < 1.0):
    robo['vel_max'] = 0.7
    robo['acc'] = 0.35
  elif (bola['distancia'] >= 0.4) and (bola['distancia'] < 0.7):
    robo['vel_max'] = 0.4
    robo['acc'] = 0.2
  elif (bola['distancia'] >= 0.1) and (bola['distancia'] < 0.4):
    robo['vel_max'] = 0.1
    robo['acc'] = 0.05

  if robo['vel'] < robo['vel_max']:
    robo['vel'] += robo['acc'] * 0.2
  elif robo['vel'] > robo['vel_max']:
    robo['vel'] -= robo['acc'] * 0.2

  robo['ecin'] = robo['peso']*(robo['vel']**2) / 2
  

  robo['vel_x'] = robo['vel'] * sin(angulo)
  robo['vel_y'] = robo['vel'] * cos(angulo)

  robo['acc_x'] = robo['acc'] * sin(angulo)
  robo['acc_y'] = robo['acc'] * cos(angulo)

  # sentido da velocidade
  if (robo['x'] < bola['x']):
    robo['vel_x'] = sqrt(robo['vel_x']**2)
  else:
    robo['vel_x'] = -sqrt(robo['vel_x']**2)

  if (robo['y'] < bola['y']):
    robo['vel_y'] = sqrt(robo['vel_y']**2)
  else:
    robo['vel_y'] = -sqrt(robo['vel_y']**2)

  robo['x'] += robo['vel_x']
  robo['y'] += robo['vel_y']

  criar_arquivos(robo, bola, tempo)

  if (bola['distancia'] <= robo['raio']):
    print("Bola interceptada")
    print("Em: %.2fs" %tempo)
    print("Distancia: %.2f" %bola['distancia'])
    robo['interceptado'] = True
    return robo
  else:
    return robo
    
def criar_arquivos(robo, bola, tempo):
  posicao = open("posicao.txt", "a")
  posicao.write("%.2f//%.2f//%.2f//%.2f//%.2f\n" %(tempo, robo['x'], robo['y'], bola['x'], bola['y']))
  posicao.close()

  velocidades = open("velocidades.txt", "a")
  velocidades.write("%.2f//%.2f//%.2f\n" %(tempo, robo['vel_x'], robo['vel_y']))
  velocidades.close()

  aceleracoes = open("aceleracoes.txt", "a")
  aceleracoes.write("%.2f//%.2f//%.2f\n" %(tempo, robo['acc_x'], robo['acc_y']))
  aceleracoes.close()

  distancia = open("distancia.txt", "a")
  distancia.write("%.2f//%.2f\n" %(tempo, bola['distancia']))
  distancia.close()

  energia_cinetica = open("energia_cinetica.txt", "a")
  energia_cinetica.write("%.2f//%.2f\n" %(tempo, robo['ecin']))
  energia_cinetica.close()


def velocidade_bola(tempo_total):
  dados_bola = []

  dados_a = []

  trajetoria_bola = open("trajetoria_bola.txt", "r")

  for linha in trajetoria_bola.readlines():
    dados_a.append(linha.strip().split('//'))
    dados_bola.append({
      't': linha.strip().split('//')[0],
      'x': linha.strip().split('//')[1],
      'y': linha.strip().split('//')[2],
    })
  trajetoria_bola.close()

  velocidade_bola = open("velocidade_bola.txt", "w")
  for linha in range(len(dados_bola)): 
    tempo = float(dados_bola[linha]['t'])
    xi = float(dados_bola[linha]['x'])
    yi = float(dados_bola[linha]['y'])

    xf = float(dados_bola[linha + 1]['x'])
    yf = float(dados_bola[linha + 1]['y'])

    delta_x = float(xf - xi)
    delta_y = float(yf - yi)

    velocidade_bola_x = delta_x / 0.2
    velocidade_bola_y = delta_y / 0.2

    velocidade_bola.write("%.2f//%.2f//%.2f\n" %(tempo, velocidade_bola_x, velocidade_bola_y))

    if (tempo == tempo_total):
      break


  velocidade_bola.close()

def aceleracao_bola(tempo_total):
  dados_bola = []

  dados_a = []

  velocidade_bola = open("velocidade_bola.txt", "r")

  for linha in velocidade_bola.readlines():
    dados_a.append(linha.strip().split('//'))
    dados_bola.append({
      't': linha.strip().split('//')[0],
      'x': linha.strip().split('//')[1],
      'y': linha.strip().split('//')[2],
    })
  velocidade_bola.close()

  aceleracao_bola = open("aceleracao_bola.txt", "w")
  for linha in range(len(dados_bola) -1): 
    tempo = float(dados_bola[linha]['t'])
    xi = float(dados_bola[linha]['x'])
    yi = float(dados_bola[linha]['y'])

    xf = float(dados_bola[linha + 1]['x'])
    yf = float(dados_bola[linha + 1]['y'])

    delta_x = xf - xi
    delta_y = yf - yi

    aceleracao_bola_x = delta_x / 0.2
    aceleracao_bola_y = delta_y / 0.2

    aceleracao_bola.write("%.2f//%.2f//%.2f\n" %(tempo, aceleracao_bola_x, aceleracao_bola_y))

    if (tempo == tempo_total):
      break
  
  aceleracao_bola.close()

def energia_cinetica_bola(tempo_total):
  dados_bola = []

  dados_a = []

  velocidade_bola = open("velocidade_bola.txt", "r")

  for linha in velocidade_bola.readlines():
    dados_a.append(linha.strip().split('//'))
    dados_bola.append({
      't': linha.strip().split('//')[0],
      'x': linha.strip().split('//')[1],
      'y': linha.strip().split('//')[2],
    })
  velocidade_bola.close()

  energia_cinetica_bola = open("energia_cinetica_bola.txt", "w")
  for linha in range(len(dados_bola)):
    tempo = float(dados_bola[linha]['t'])
    vx = float(dados_bola[linha]['x'])
    vy = float(dados_bola[linha]['y'])

    velocidade_bola = sqrt(vx**2 + vy**2)
    ecin = 0.05 * (velocidade_bola**2) / 2

    energia_cinetica_bola.write("%.2f//%.2f\n" %(tempo, ecin))

    if (tempo == tempo_total):
      break  

  energia_cinetica_bola.close()

    

def limpar_arquivos():
  posicao = open("posicao.txt", "w")
  posicao.close()

  velocidades = open("velocidades.txt", "w")
  velocidades.close()

  aceleracoes = open("aceleracoes.txt", "w")
  aceleracoes.close()

  distancia = open("distancia.txt", "w")
  distancia.close()

  energia_cinetica = open("energia_cinetica.txt", "w")
  energia_cinetica.close()

# Gráficos
def grafico_trajetoria():
  posicao = open("posicao.txt", "r")
  x_robo = []
  y_robo = []
  x_bola = []
  y_bola = []
  for linha in posicao:
    valores = linha.split("//")
    x_robo.append(float(valores[1]))
    y_robo.append(float(valores[2]))
    x_bola.append(float(valores[3]))
    y_bola.append(float(valores[4]))
  plt.plot(x_robo, y_robo)
  plt.plot(x_bola, y_bola)
  
  plt.title("Gráfico das trajetórias da bola e do robo até a interceptação")
  plt.xlabel("X (m)")
  plt.ylabel("Y (m)")
  plt.legend(["Robô", "Bola"])

  plt.savefig("grafico_trajetoria.png", bbox_inches='tight', pad_inches=0, dpi=300)
  plt.close()

def grafico_posicao_x():
  posicao = open("posicao.txt", "r")
  tempo = []
  x_robo = []
  x_bola = []

  for linha in posicao:
    valores = linha.split("//")
    tempo.append(float(valores[0]))
    x_robo.append(float(valores[1]))
    x_bola.append(float(valores[3]))

  plt.plot(tempo, x_robo)
  plt.plot(tempo, x_bola)

  plt.title("Gráfico da posição x do robô e da bola em função do tempo")
  plt.xlabel("Tempo (s)")
  plt.ylabel("X (m)")
  plt.legend(["Robô", "Bola"])

  plt.savefig("grafico_posicao_x.png", bbox_inches='tight', pad_inches=0, dpi=300)
  plt.close()

def grafico_posicao_y():
  posicao = open("posicao.txt", "r")
  tempo = []
  y_robo = []
  y_bola = []

  for linha in posicao:
    valores = linha.split("//")
    tempo.append(float(valores[0]))
    y_robo.append(float(valores[2]))
    y_bola.append(float(valores[4]))

  plt.plot(tempo, y_robo)
  plt.plot(tempo, y_bola)

  plt.title("Gráfico da posição y do robô e da bola em função do tempo")
  plt.xlabel("Tempo (s)")
  plt.ylabel("Y (m)")
  plt.legend(["Robô", "Bola"])

  plt.savefig("grafico_posicao_y.png", bbox_inches='tight', pad_inches=0, dpi=300)
  plt.close()

def grafico_velocidade():
  velocidades = open("velocidades.txt", "r")
  tempo = []
  vx_robo = []
  vy_robo = []

  for linha in velocidades:
    valores = linha.split("//")
    tempo.append(float(valores[0]))
    vx_robo.append(float(valores[1]))
    vy_robo.append(float(valores[2]))

  plt.plot(tempo, vx_robo)
  plt.plot(tempo, vy_robo)

  plt.title("Gráfico das velocidades do robô em função do tempo")
  plt.xlabel("Tempo (s)")
  plt.ylabel("Velocidade (m/s)")
  plt.legend(["Vx", "Vy"])

  plt.savefig("grafico_velocidade.png", bbox_inches='tight', pad_inches=0, dpi=300)
  plt.close()

  velocidades.close()

def grafico_velocidade_bola():
  velocidade_bola = open("velocidade_bola.txt", "r")
  tempo = []
  vx_bola = []
  vy_bola = []

  for linha in velocidade_bola:
    valores = linha.split("//")
    tempo.append(float(valores[0]))
    vx_bola.append(float(valores[1]))
    vy_bola.append(float(valores[2]))

  plt.plot(tempo, vx_bola)
  plt.plot(tempo, vy_bola)

  plt.title("Gráfico das velocidades da bola em função do tempo")
  plt.xlabel("Tempo (s)")
  plt.ylabel("Velocidade (m/s)")
  plt.legend(["Vx", "Vy"])

  plt.savefig("grafico_velocidade_bola.png", bbox_inches='tight', pad_inches=0, dpi=300)

  velocidade_bola.close()

  plt.close()

def grafico_aceleracao():
  aceleracoes = open("aceleracoes.txt", "r")

  tempo = []
  ax_robo = []
  ay_robo = []

  for linha in aceleracoes:
    valores = linha.split("//")
    tempo.append(float(valores[0]))
    ax_robo.append(float(valores[1]))
    ay_robo.append(float(valores[2]))

  plt.plot(tempo, ax_robo)
  plt.plot(tempo, ay_robo)

  plt.title("Gráfico das acelerações do robô em função do tempo")
  plt.xlabel("Tempo (s)")
  plt.ylabel("Aceleração (m/s²)")
  plt.legend(["Ax", "Ay"])

  plt.savefig("grafico_aceleracao.png", bbox_inches='tight', pad_inches=0, dpi=300)
  plt.close()

  aceleracoes.close()

def grafico_aceleracao_bola():
  aceleracao_bola = open("aceleracao_bola.txt", "r")

  tempo = []
  ax_bola = []
  ay_bola = []

  for linha in aceleracao_bola:
    valores = linha.split("//")
    tempo.append(float(valores[0]))
    ax_bola.append(float(valores[1]))
    ay_bola.append(float(valores[2]))

  plt.plot(tempo, ax_bola)
  plt.plot(tempo, ay_bola)

  plt.title("Gráfico das acelerações da bola em função do tempo")
  plt.xlabel("Tempo (s)")
  plt.ylabel("Aceleração (m/s²)")
  plt.legend(["Ax", "Ay"])

  plt.savefig("grafico_aceleracao_bola.png", bbox_inches='tight', pad_inches=0, dpi=300)
  
  aceleracao_bola.close()

  plt.close()

def grafico_distancia():
  distancia = open("distancia.txt", "r")
  tempo = []
  dist = []

  for linha in distancia:
    valores = linha.split("//")
    tempo.append(float(valores[0]))
    dist.append(float(valores[1]))

  plt.plot(tempo, dist)

  plt.title("Gráfico da distância relativa entre o robô e a bola em função do tempo")
  plt.xlabel("Tempo (s)")
  plt.ylabel("Distância (m)")


  plt.savefig("grafico_distancia.png", bbox_inches='tight', pad_inches=0, dpi=300)
  plt.close()

def grafico_energia_cinetica():
  energia_cinetica = open("energia_cinetica.txt", "r")
  tempo = []
  ec = []

  for linha in energia_cinetica:
    valores = linha.split("//")
    tempo.append(float(valores[0]))
    ec.append(float(valores[1]))

  plt.plot(tempo, ec)

  plt.title("Gráfico da energia cinética do robô em função do tempo")
  plt.xlabel("Tempo (s)")
  plt.ylabel("Energia cinética (J)")

  plt.savefig("grafico_energia_cinetica.png", bbox_inches='tight', pad_inches=0, dpi=300)
  plt.close()

  energia_cinetica.close()

limpar_arquivos()

robo_xi_max = int(2 * 100)
robo_xi_min = 0

robo_yi_max = int(1.5 * 100)
robo_yi_min = int(-0.5 * 100)

while(True):
  robo_xi = randint(robo_xi_min, robo_xi_max) / 100
  robo_yi = randint(robo_yi_min, robo_yi_max) / 100
  dist_i = sqrt((robo_xi - 1)**2 + (robo_yi - 0.5)**2)
  if dist_i <= 1:
    break
  else:
    continue



robo = {
  'x': robo_xi,
  'y': robo_yi,
  'raio': 0.09, #m
  'peso': 2.8,
  'vel_max': 2.8,
  'vel': 0,
  'vel_x': 0,
  'vel_y': 0,
  'acc': 0,
  'acc_x': 0,
  'acc_y': 0,
  'ecin': 0,
  'interceptado': False
}

bola = {
  'x': 1,
  'y': 0.5,
  'distancia': dist_i
}



dados_bola = []

dados_a = []

trajetoria_bola = open("trajetoria_bola.txt", "r")

for linha in trajetoria_bola.readlines():
  dados_a.append(linha.strip().split('//'))
  dados_bola.append({
    't': linha.strip().split('//')[0],
    'x': linha.strip().split('//')[1],
    'y': linha.strip().split('//')[2],
  })

trajetoria_bola.close()
""" for i in range(len(dados_a)):
  dados_a[i][0] = float(dados_a[i][0])
  dados_a[i][1] = float(dados_a[i][1])
  dados_a[i][2] = float(dados_a[i][2])
  dados_bola[dados_a[i][0]] = {
    't': dados_a[i][0],
    'x': dados_a[i][1],
    'y': dados_a[i][2],
  } """


for i in range(len(dados_bola)):
  tempo = float(dados_bola[i]['t'])
  bola['x'] = float(dados_bola[i]['x'])
  bola['y'] = float(dados_bola[i]['y'])
  robo = interceptar(robo, bola, tempo)

  if robo['interceptado'] == True:
    velocidade_bola(tempo)
    aceleracao_bola(tempo)
    energia_cinetica_bola(tempo)
    break
  else:
    pass




grafico_trajetoria()
grafico_posicao_x()
grafico_posicao_y()
grafico_velocidade()
grafico_velocidade_bola()
grafico_aceleracao()
grafico_aceleracao_bola()
grafico_distancia()
grafico_energia_cinetica()