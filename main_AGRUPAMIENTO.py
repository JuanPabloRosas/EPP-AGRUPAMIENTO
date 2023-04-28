#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gurobipy import *
from gurobipy import tuplelist
import csv

import numpy as np
import EPP_PSL_AGRUPAMIENTO
import os




#	LEE INSTANCIA
# #-----------------------------------------------------------------
#	WINDOWS
folder = 'C:\\Users\\pablo\\Documents\\PISIS\\Doctorado\\Paper\\RepoPaper\\EPPS\\instancias\\'
folder_estudiantes = 'C:\\Users\\pablo\\Documents\\PISIS\\Doctorado\\Paper\\RepoPaper\\EPPS\\estudiantes_AGRUPAMIENTO.csv'
#carpeta = "soluciones/final/"
#	LINUX
#folder = '/home/juanpablo/Documentos/PISIS/Doctorado/ExperimentacionGurobi/instancias_nuevas/caso_real/'
#folder = '/home/juanpablo/Documentos/PISIS/Doctorado/ExperimentacionGurobi/instancias/'


def leeEstudiantes(file):
   estudiantes = [[] for i in range(40)]
   with open(file, 'rt') as f:
      reader = csv.reader(f)
      for row in reader:
         for i in range(0,40):
            estudiantes[i].append(float(row[i]))
   
   return estudiantes

students = leeEstudiantes(folder_estudiantes)
with open(folder+'soluciones_agrupamiento/acumulado.csv', 'a+',newline='') as file:
   writer=csv.writer(file)
   for filename in os.listdir(folder):
      if filename.endswith('.csv'):
         print('----------------------------------------'+ filename +'----------------------------------------' )
         materias = []
         temas = []
         subtemas = []
         actividades = []
         obligatorias = []
         habilitamiento1 = {}
         habilitamiento2 = {}
         duracion = {}
         valor = {}
         estres = []
         with open(folder+filename, 'rt') as f:
            reader = csv.reader(f)
            for row in reader:
               materias.append(row[0])
               temas.append(row[1])
               subtemas.append(row[2])
               actividades.append(row[3])
               duracion[(row[3],row[2],row[1],row[0])]=float(row[4])
               valor[(row[3],row[2],row[1],row[0])]=float(row[5])
               #estres.append(float(row[6]))
               if(row[7]!="0"):
                  habilitamiento1[row[3]]=row[7]
               if(row[8]!="0"):
                  habilitamiento2[row[3]]=row[8]
               if(row[9] == "1"):
                  obligatorias.append((row[3],row[2],row[1],row[0]))
         arcs=[]
         
         for i in range(0,88):
            if ((actividades[i],subtemas[i],temas[i],materias[i]) in duracion):
               arcs.append((actividades[i],subtemas[i],temas[i],materias[i]))

         arcs = tuplelist(arcs)

         #	CREA ARCHIVO SALIDA
         # #-----------------------------------------------------------------
         kmin = 100
         kmax = 100
         CI_test=[0.95,0.99,1.03]
         #CI_test=[0.95]
         ev = 's'
         for s in range(40):
            for k in range(kmin,kmax + 1,5):	
               for CI in CI_test:
                  print('KMIN: ' + str(k) + '   CI: ' + str(CI))
                  f2= open(folder+'soluciones_agrupamiento/'+filename.split('.')[0]+'_'+str(k)+'_'+str(CI)+'_'+ev+'_'+ str(s+1) + '_EPP-SL'+'.txt',"w+")
                  ppeCISec_sol,d=EPP_PSL_AGRUPAMIENTO.ppeCISec(k,actividades,np.unique(subtemas),np.unique(temas),np.unique(materias),obligatorias,habilitamiento1, habilitamiento2, duracion,valor,students[s],CI,arcs)
                  if ppeCISec_sol is not None:
                     for v in ppeCISec_sol:
                        f2.write(v+'\n')
                        #print(v)
                  f2.close()
                  writer.writerow([filename.split('.')[0],str(k),str(CI),ev,str(s+1),'EPP-SL'] + d)
   file.close()
                  