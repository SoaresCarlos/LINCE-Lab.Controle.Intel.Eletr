import serial  # Biblioteca para comunicação serial
import numpy as np  # Biblioteca para operações matemáticas e manipulação de arrays
import matplotlib.pyplot as plt  # Biblioteca para criar gráficos
import time as t  # Biblioteca para manipulação do tempo (pausas, contagem)
from scipy.signal import max_len_seq

tensao_alimentacao = 13
nbits = 8
nsm = 200  # Número de amostras que serão coletadas


Amplitude = 0.25  # Amplitude do sinal gerado
setpoint = 5  # Valor desejado do sistema (referência)

usm = Amplitude*2*(max_len_seq(nbits,length = nsm)[0]-0.5 ) + setpoint
u = np.kron(usm,np.ones(3))
numAmostras = len(u)

tempo = np.zeros(numAmostras)  # Array para armazenar o tempo das amostras
y = np.zeros(numAmostras)  # Array para armazenar as leituras de tensão
toc = np.zeros(numAmostras) #Armazena o tempo de execução de cada iteração


Ts = 0.02  # Tempo de amostragem (intervalo de tempo entre amostras)

print('\nEstabelecendo conexão.')
conexao = serial.Serial(port='COM8', baudrate=9600, timeout=0.005)  # Configura a porta serial COM8 para comunicação a 9600 bps com timeout de 5 ms

t.sleep(1)
print('\nIniciando coleta.')

for n in range(numAmostras): #Loop responsavel pela coleta de dados
    tic = t.time() #Marca o inicio da coleta de cada amostra

    us = (u[n]*255)/tensao_alimentacao  # COnverte a referencia r[n] para um valor compativel com o microcontralador (0 a 255)
    conexao.write(str(round(us)).encode()) #Envia o valor convertido para o dispositivo
    
    if (conexao.inWaiting() > 0): #Codigo verifica se ha dados disponiveis na porta serial
        y[n] = conexao.readline().decode() #Lê o dado recebido e armazena no array "y"

    
    t.sleep(Ts) #Pausa para respeitar o tempo de amostragem
    
    if (n > 0):
        tempo[n] = tempo[n-1] + Ts #Calcula o tempo acumulado
    toc[n] = t.time() - tic #Armazena o tempo de execução de cada iteração
conexao.write('0'.encode())
print('\nFim da coleta.')
conexao.close() #Sinal para parar o dispositivo e encerrar a conexão
#Abaixo ocorre a analise e a exebição dos dados coletados.
print('media=',np.mean(u))

print('\nPeríodo real:', np.mean(toc))
print('Nivel_DC:', np.mean(y[tempo>2]))

dados=np.stack((tempo,u,y),axis=-1)
np.save('EnsaioPRBS3.npy', dados)

plt.figure(figsize=(10,10))
plt.subplot(211)
plt.plot(tempo,u,'-b',linewidth=1.2)
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


