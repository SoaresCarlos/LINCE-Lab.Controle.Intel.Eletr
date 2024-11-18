"""
Bancada Motor-Gerador
UFPA - Campus Tucuruí
Monitoria de Sistemas de Controle para Engenharia - PGRAD - MONITORIA 03/2020
Coodenador: Cleison Daniel Silva
Bolsista: Felipe Silveira Piano
Data: 27/09/2020
"""

import serial #Biblioteca que permite a comunicação com microcontroladores
import numpy as np # Biblioteca para operações matematicas e manipulação de arrays
import matplotlib.pyplot as plt #Biblioteca para a criação de graficos
import time as t #Para a manipulação do tempo, como pausas
from scipy.signal import square,sawtooth #Biblioteca usada para gerar formas de onda (Quadrada, triangular)


##########################################

tensao_alimentacao = 13 #Defina a tensão da bancada com a qual esta trabalhando

numAmostras = 500  #Numero de amostras que serão coletadas
tempo = np.zeros(numAmostras) #Arrays para armazenar o tempo e as leituras de tensão
y = np.zeros(numAmostras)

Ts = 20e-3 #Tempo de amostragem (intervalo de tempo entre as amostras)

fre = 2 #Frequencia do sinal gerado
Amplitude = 0.5 #Amplitude do sinal gerado
setpoint = 6 #valor desejado para o controle
#a = 2*np.ones(int(numAmostras/2))
#b = 4*np.ones(int(numAmostras/2))
#u = np.concatenate([a,b]) #degrau
r = np.zeros(numAmostras) #Array para armazenar o sinal de referencia
toc = np.zeros(numAmostras) #Armazena o tempo de execução de cada iteração
######################


for n in range(numAmostras): #Loop que cria um sinal de referencia para a onda, somada ao setpoint, garantindo que o valor minimo da onda seja igual ao setpoint
    #r[n] = Amplitude*square(2*np.pi*fre*n*Ts) + setpoint
    r[n] = Amplitude*sawtooth(2*np.pi*fre*n*Ts) + setpoint
    #r[n] = Amplitude*np.sin(2*np.pi*fre*n*Ts) + setpoint
    #r[n] = u[n]
    
print('\nEstabelecendo conexão.')
conexao = serial.Serial(port='COM8', baudrate=9600, timeout=0.005) #Alterar a porta de conexão serial de acordo com a do arduino
#Ocorre uma conexão serial com a porta especificada, com uma taxa de transferencia (baudrate) de 9600 bits por segundo e timeout de 5ms

t.sleep(1)
print('\nIniciando coleta.')

for n in range(numAmostras): #Loop responsavel pela coleta de dados
    tic = t.time() #Marca o inicio da coleta de cada amostra

    if (conexao.inWaiting() > 0): #Codigo verifica se ha dados disponiveis na porta serial

        y[n] = conexao.readline().decode() #Lê o dado recebido e armazena no array "y"
        #if(n<170):       
        #    r[n] = 2.8 #Fixa o valor de referencia para 2.8, dentro das primeiras 170 amostras
    u = (r[n]*255)/tensao_alimentacao  # COnverte a referencia r[n] para um valor compativel com o microcontralador (0 a 255)
    conexao.write(str(round(u)).encode()) #Envia o valor convertido para o dispositivo
    
    t.sleep(Ts) #Pausa para respeitar o tempo de amostragem
    
    if (n > 0):
        tempo[n] = tempo[n-1] + Ts #Calcula o tempo acumulado
    toc[n] = t.time() - tic #Armazena o tempo de execução de cada iteração
conexao.write('0'.encode())
print('\nFim da coleta.')
conexao.close() #Sinal para parar o dispositivo e encerrar a conexão
#Abaixo ocorre a analise e a exebição dos dados coletados.
print('media=',np.mean(r))

print('\nPeríodo real:', np.mean(toc))
print('Nivel_DC:', np.mean(y[tempo>2]))

plt.figure(figsize=(10,10))
plt.subplot(211)
plt.plot(tempo,r,'-b',linewidth=1.2)
plt.xlabel('Tempo(s)')
plt.ylabel('Tensão (V)')
plt.grid()
plt.title('Onda Quadrada - Malha Aberta')
plt.legend(loc='lower right', labels=('Sinal de Entrada','Sinal de Saída'))

plt.subplot(212)
#plt.plot(tempo,r,'-b',tempo,y,'-r',linewidth=1.2)
plt.plot(tempo,y,'-r.',linewidth=1.2)
plt.xlabel('Tempo(s)')
plt.ylabel('Tensão (V)')
plt.grid()
# plt.title('Tensão de Saída - Malha Aberta')
plt.show()

dados=np.stack((tempo,r,y),axis=-1)

# np.save("C:/Users/Raissa/OneDrive - Universidade Federal do Pará - UFPA/Área de Trabalho/LAB_CONTROLE/MOTOR GERADOR/Motor_Gerador_Python/Dados/Dados_degrau.npy", dados)