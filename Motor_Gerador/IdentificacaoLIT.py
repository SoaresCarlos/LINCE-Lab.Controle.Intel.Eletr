import numpy as np  # Biblioteca para operações matemáticas e manipulação de arrays
import matplotlib.pyplot as plt  # Biblioteca para criar gráficos
import scipy.signal as sg 

# Carregar os dados:
data = np.load('EnsaioPRBS3.npy')

t = data[:-50,0]
u = data[50:,1] - np.mean(data[50:,1])
y = data[50:,2] - np.mean(data[50:,2])
Ts = 20e-3

plt.figure(figsize=(7,6))
plt.subplot(211)
plt.plot(t,u)
plt.grid()
plt.subplot(212)
plt.plot(t,y)
plt.grid()
plt.show()

# Pré-processamento dos dados:

print('Numero de amostras: ', len(u))

Ni = int(0.7*len(u))
print('Numero de amostras de identificação: ', Ni)


plt.figure(figsize = (12,6))
plt.subplot(211)
plt.step(t[:Ni+1],u[:Ni+1],label='Dados de Identificação')
plt.step(t[Ni:],u[Ni:],label='Dados de Validação')
plt.ylabel('u(n)')
plt.legend()
plt.grid()
plt.subplot(212)
plt.plot(t[:Ni+1],y[:Ni+1], label='Dados de Identificação')
plt.plot(t[Ni:],y[Ni:],label='Dados de Validação')
plt.legend()
plt.grid()
plt.ylabel('y(n)')
plt.show()

ui = u[:Ni+1]
yi = y[:Ni+1]
uv = u[Ni:]
yv = y[Ni:]


# Matriz de regressão:
nb = 1
na = 2
ni = np.arange(na,Ni+na)
Ar = np.zeros((Ni,na+nb))

Ar[:,0] = y[ni-1]
Ar[:,1] = y[ni-2]
Ar[:,2] = u[ni-1]

theta = np.linalg.inv(Ar.T@Ar)@Ar.T@y[ni]

a1 = theta[0]
a2 = theta[1]
b1 = theta[2]

B = [b1]
A = [1, -a1, -a2]


Gi = sg.TransferFunction(B,A, dt = Ts)


# Resposta do modelo identificado:
yp = np.squeeze(sg.dlsim(Gi, u, t = t)[1])
print('yp', len(yp))
plt.figure(figsize = (12,6))
plt.subplot(211)
plt.step(t[:Ni+1],u[:Ni+1],label='Dados de Identificação')
plt.step(t[Ni:],u[Ni:],label='Dados de Validação')
plt.ylabel('u(n)')
plt.legend()
plt.grid()
plt.subplot(212)
plt.plot(t[:Ni+1],y[:Ni+1],linewidth = 3.0,label='Dados de Identificação')
plt.plot(t[Ni:],y[Ni:],linewidth = 3.0,label='Dados de Validação')
plt.plot(t[:-1],yp,'k',label='Modelo identificado')
plt.legend()
plt.grid()
plt.ylabel('y(n)')
plt.show()


corr_matrix = np.corrcoef(y[1:], yp)
corr = corr_matrix[0,1]
R_sq = np.round(corr**2, 2)*100
 
print(R_sq)