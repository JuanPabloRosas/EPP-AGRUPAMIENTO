#		V1.0 Problema de Planificacion Educativa (PPE) - Gurobi - Python
#		Autor: Juan Pablo Rosas Baldazo		02/09/19
#		
#		
#-------------------------------------------------------------------------------------------

from gurobipy import *
from math import log
import time

def res(a,act,hab1,hab2):
   suma = 0
   lista=[a]
   while(len(lista)>0):
      act = lista.pop()
      for h1 in hab1:
         if(act == h1):
            suma = suma + 1
            lista.append(hab1[h1])
      for h2 in hab2:
         if(act == h2):
            suma = suma + 1
            lista.append(hab2[h2])
      
   return suma

def habilitan(a,act,hab1,hab2):
   lista = []
   for h1 in hab1:
      if(a == h1):
         lista.append(hab1[h1])
   for h2 in hab2:
      if(act == h2):
         lista.append(hab2[h2])
      
   return lista
         
def ppeCISec(kmin,actividades,subtemas,temas,materias,obligatorias,habilitamiento1,habilitamiento2,duracion,valor,estres,CI,arcs):
   Dmax = 66 #   Debe de ser la suma de la duracion de todas las actividades dividido entre la cantidad de subtemas para dar un promedio de tiempo a cada subtema
   Kmax = 100
   start_time = time.time()	
   #	Crea ambiente
   model = Model('----- AGRUPAMIENTO -----')
   model.setParam('TimeLimit', 900)
   # #	Variables
   # -------------------------------------------------------------------------------------
	
   #	Actividades
   x={}
   #	Subtemas
   y={}
   for a,s,t,m in arcs:
      for p in range(1,89):
         x[a,s,t,m,p] = model.addVar(0.0,1.0,obj=1.0, vtype=GRB.BINARY ,name='%s_%s_%s_%s_%s' % (a,s,t,m,p))
         y[s,t,m] = model.addVar(lb = 0, ub=Kmax, vtype=GRB.INTEGER ,name='score_s_%s_%s_%s' % (s,t,m))
   model.update()

	#	Restricciones
	#-------------------------------------------------------------------------------------
   #"""
   
   for s in subtemas:
      #	Duración menor a Dmax por subtema
      model.addConstr(quicksum(duracion[a,s2,t,m] * (1 + estres[p-1] * log(p,10)) * (p**log(CI,2)) * x[a,s2,t,m,p] for a,s2,t,m in arcs.select('*', s ,'*','*') for p in range(1,89)) <= Dmax,"Kmax_%s_%s_%s_%s_%s" % (a,s,t,m,p))
	   #	Score menor a kmax por subtema
      model.addConstr(quicksum(valor[a,s2,t,m] * x[a,s2,t,m,p] for a,s2,t,m in arcs.select('*', s ,'*','*') for p in range(1,89)) <= Kmax,"Kmax_%s_%s_%s_%s_%s" % (a,s,t,m,p))

   #	Actividades Obligatorias
   for o,s,t,m in obligatorias:
      model.addConstr(quicksum(x[o,s,t,m,p] for p in range(1,89)) == 1, "mandatory_%s_%s_%s_%s_%s" % (o,s,t,m,p))

	# # #	No permite posiciones repetidas
   for p in range(1,89):
      model.addConstr(quicksum(x[a,s,t,m,p] for a,s,t,m in arcs) <= 1, "No_repetir_act_%s_%s_%s_%s_%s" % (a,s,t,m,p))

   for a,s,t,m in arcs:
      #  No permite actividades repetidas
      model.addConstr(quicksum(x[a,s,t,m,p] for p in range(1,89)) <= 1, "No_repetir_pos_%s_%s_%s_%s_%s" % (a,s,t,m,p))
      #	Acumula el score de los subtemas
      model.addConstr(y[s,t,m] == quicksum(valor[a,s,t,m]*x[a,s2,t2,m2,p] for a,s2,t2,m2 in arcs.select('*',s,t,m,'*') for p in range(1,89)))

	# #	Habilitamiento i requiere i2	
   for a in actividades:
      hab = habilitan(a,actividades,habilitamiento1,habilitamiento2)
      for a2,s,t,m in arcs.select(a,'*','*','*'):
         for p in range(res(a,actividades,habilitamiento1,habilitamiento2) + 1,89):
            model.addConstr((quicksum(x[a3,s2,t2,m2,q] for h in hab for a3,s2,t2,m2 in arcs.select(h,'*','*','*') for q in range(1,p) if(q<p)))
               >= len(hab)*x[a2,s,t,m,p],"Habilitamiento_%s_%s_%s" % (a,a2,p))

	#model.printStats()
   #model.write("file.lp")
	
	#	Funcion Objetivo
	#-------------------------------------------------------------------------------------
   # MODELO AGRUPAMIENTO
   obj = quicksum(valor[a,s,t,m] * x[a,s,t,m,p] for a,s,t,m in arcs for p in range(1,89))

   model.setObjective(obj, GRB.MAXIMIZE)

   #	Optimiza
   #-------------------------------------------------------------------------------------
   model.optimize()
   solucion=[]
   data = []
   if model.status == GRB.INFEASIBLE:
      # Las siguientes cuatro lineas ayudan a mantener la estructura de las soluciones.
      data.append(0)
      data.append(-1)
      data.append(-1)
      data.append(100)
      print("INFEASIBLE")
   else:
      data.append(1)
      obj = model.getObjective()
      print("------------------------------ \n")
      print("Valor objetivo: \n")
      print(obj.getValue())
      solucion.append("Valor Objetivo:"+str(obj.getValue()))
      data.append(obj.getValue())

      print("------------------------------ \n")
      print("Runtime: \n")
      runtime = time.time() - start_time
      print(runtime)
      solucion.append("Runtime:"+str(runtime))
      data.append(runtime)

      print("------------------------------ \n")
      print("Gap: \n")
      print(model.MIPGap)
      solucion.append("Gap:"+str(model.MIPGap))
      data.append(model.MIPGap)

      print("------------------------------ \n")
      print("Solucion: \n")
      for v in model.getVars():
         if v.X != 0:
            s =  round(float(v.X),1)
            if(s > 0):
               print(v.Varname,s)
               solucion.append(v.Varname + '_' + str(s))
               if(v.Varname.startswith('score')):
                  data.append(s)
      print("------------------------------ \n")

      solucion.append("DURACION")
      for (a,s,t,m) in duracion:
         solucion.append(str(duracion[(a,s,t,m)]))
      solucion.append("VALOR")
      for (a,s,t,m) in valor:
         solucion.append(str(valor[(a,s,t,m)]))
      solucion.append("ESTRES")
      for i in range(0,len(estres)):
         solucion.append(str(estres[i]))
   
   return(solucion,data)


if __name__ == '__main__':
   ppeCISec()
