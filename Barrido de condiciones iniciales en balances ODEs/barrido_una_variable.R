#################################
#                               #             
# BARRIDO CONSIDERANDO         #
# UNA SOLA VARIABLE MANIPULADA  #
# VARIACION DE C_S0 PARA        #
# MAXIMIZAR C_Pf                #
#                               #  
#################################



# CARGA DE LIBRERIAS ----
# = = = = = = = = = = = = 

library(deSolve)



# CONDICIONES DE FERMENTACION ----
# = = = = = = = = = = = = = = = = = =

# ___ Tiempo de fermentacion (simulacion)

t0 = 0 #h 
dt = 2 #h
t1 = 100 #h

times <- seq(t0, t1, by = dt)

n_t = length(times)



# ___ Parametros ----

mu_m1 = 1.848  # 1/h
K_S1 = 101.78  # g/l
mu_m2 = 0.502  # 1/h
K_S2 = 0.445  # g/l
Y_XS1 = 0.45998  # g/g
m_S1 = 0.0314  # g/(g.h)
Y_XS2 = 44.444  # g/g
m_S2 = 0.00000109  # g/(g.h)
K_1 = 0.00001075  # g/g
K_2 = 0.00000369  # g/(g.h)
K_3 = 0.0000000246  # g/g
K_4 = 0.000520  # g/(g.h)
S_m = 917.8
n = 2.011 

C_S02 = 5.3  # g/l



# ___ Condiciones iniciales ----

C_X0 = 1.00695  # g/l
C_S10 = 80  # g/l
C_S20 = 0.25  # g/l
C_P10 = 0  # g/l
C_P20 = 0  # g/l
V0 = 1.5  # l



# DECLARACION DE FUNCIONES ----
# = = = = = = = = = = = = = = =


# ___ mu

mu_crec <- function(mu_m1,C_S1,K_S1,mu_m2,C_S2,K_S2,S_m,n) {
  
  mu = ((mu_m1*C_S1)/(K_S1+C_S1)) * ((mu_m2*C_S2)/(K_S2+C_S2)) * ( 1 - ((C_S1/C_S2)/(S_m))^n )
  
  return(mu)
  
}


# ___ Caudal de alimentacion de glucosa

F_1 <- function(t){
  
  F_1 = (t < 10)*(0) + (t >= 10)*(0.005)
  
  return(F_1)
  
}


# ___ Concentracion de glucosa en la alimentacion

C_S01 <- function(t){
  
  C_S01 = (t < 40)*(300) + (t>=40)*(250)
  
  return(C_S01)
  
}


# ___ Caudal de alimentacion de nitrogeno

F_2 <- function(t){
  
  F_2 = (t < 10)*(0) + (10 < t & t < 40)*(0.005) + (t>=40)*(0)
  
  return(F_2)
  
}


# ___ Caudal total 

F_t <- function(F_1,F_2,t){
  
  F_1 = (t < 10)*(0) + (t >= 10)*(0.005)
  
  F_2 = (t < 10)*(0) + (10 <= t & t < 40)*(0.005) + (t>=40)*(0)
  
  F_t = F_1 + F_2
  
  return(F_t)
  
}



# FUNCION DE RESOLUCION ----
# = = = = = = = = = = = = = =

Bces <- function(t, vals0, parametros) {
  with(as.list(c(vals0, parametros)), {
    
    
    mu = mu_crec(mu_m1,C_S1,K_S1,mu_m2,C_S2,K_S2,S_m,n)
    
    F_1 = F_1(t)
    
    F_2 = F_2(t)
    
    F_t = F_t(F_1,F_2,t)
    
    C_S01 = C_S01(t)
    
    # ___ Balances ----
    # -----------------
    
    dC_X.dt = mu*C_X - ( (F_t/V) * C_X )
    
    dC_S1.dt = -(((mu*C_X)/(Y_XS1)) + m_S1*C_X) + ( ((F_1*C_S01)/V) - ((F_t*C_S1)/V) )
    
    dC_S2.dt = -(((mu*C_X)/(Y_XS2)) + m_S2*C_X) + ( ((F_2*C_S02)/V) - ((F_t*C_S2)/V) )
    
    dC_P1.dt = (K_1*mu*C_X + K_2*C_X) - ((F_t/V)*C_P1)
    
    dC_P2.dt = (K_3*mu*C_X + K_4*C_X) - ((F_t/V)*C_P2)
    
    dV.dt = F_t
    
    
    list(c(dC_X.dt,dC_S1.dt,dC_S2.dt,dC_P1.dt,dC_P2.dt,dV.dt))
    
  })
  
}



# SOLVE ----
# = = = = = =

parametros <- c(mu_m1,K_S1,mu_m2,K_S2,Y_XS1,m_S1,Y_XS2,m_S2,K_1,K_2,K_3,K_4,S_m,n,F_1,F_2,F_t,C_S01,C_S02)
vals0 <- c(C_X = C_X0, C_S1 = C_S10, C_S2 = C_S20, C_P1 = C_P10, C_P2 = C_P20, V = V0)
out <- ode(y=vals0, times = times, func = Bces, parms = parametros)



# SETEO VARIABLE MANIPULADA ----
# = = = = = = = = = = = = = = = =

lim_inf = 5 # Cota inferior
lim_sup = 50 # Cota superior 
paso = 5 # Paso de iteracion

vector_C_S0 = seq(lim_inf,lim_sup, by = paso) # Vector de valores de barrido de la variable manipulada: Estos son los valores que va a tener la variable manipulada

C_Pf = c() # Inicializo el vector C_Pf (inicializar = crear objeto vacío ). A este vector vacío le voy a ir agregando los valores de C_Pf que obtenga en cada paso de iteracion 
           # Por lo tanto, este vector va a almacenar todas las C_Pf obtenidas en el barrido, una vez que termine el bucle for


# BARRIDO ----
# = = = = = = 

for (i in vector_C_S0) {
  
  C_S0 = i #g /L # Variable manipulada
  
  vals0 <- c(C_B = C_B0, C_S = C_S0, C_P = C_P0) # Condiciones iniciales para simulacion
  out <- ode(y=vals0, times = times, func = Bces, parms = parametros) # Simulacion
  
  ## POST - PROCESSING ----
  
  t = out[,1]
  res.C_B = out[,2]
  res.C_S = out[,3]
  res.C_P = out[,4]
  
  C_Pf_i = res.C_P[n_t]# Este es el valor de C_Pf en el cada paso de iteracion 
  
  C_Pf = c(C_Pf,C_Pf_i) # Aca le agrego al vector C_Pf el nuevo valor de C_Pf_i obtenido 
  
}  
  


# MOSTRAR RESULTS ----
# = = = = = = = = = = =

resultados <- data.frame(vector_C_S0,C_Pf)

dev.new()
plot(vector_C_S0,C_Pf,xlab = "C_S0 [g/L]", ylab = "C_Pf [g/L]")
