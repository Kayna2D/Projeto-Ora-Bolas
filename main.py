from math import *
from random import *
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
import os

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

def limpar_arquivos():
  posicao = open("posicao.txt", "w")
  posicao.close()

  velocidades = open("velocidades.txt", "w")
  velocidades.close()

  aceleracoes = open("aceleracoes.txt", "w")
  aceleracoes.close()

  distancia = open("distancia.txt", "w")
  distancia.close()

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
  'vel_max': 2.8,
  'vel': 0,
  'vel_x': 0,
  'vel_y': 0,
  'acc': 0,
  'acc_x': 0,
  'acc_y': 0,
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

  if robo['interceptado']  == True:
    break
  else:
    pass

grafico_trajetoria()
