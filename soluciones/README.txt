El nombre de cada archivo solución significa los siguiente:
			Ejemplo: i_5_2_100_1.03_s_38_EPP-SL
	PosiciónEstres_NumInstancia_RequerimientosPrecedencia_Kmax_IQ_FormaEvaluar_Estudiante_ModeloUtilizado

En este caso la posición de estrés no es relevante, ya que no consideramos el de la instancia
de actividades, si no, el de cada estudiante, se dejó en el nombre para no modificar el código.

Cada archivo de solución contiene la siguiente información:
- Valor objetivo
- Runtime
- gap%
- Solución
- Duración
- Valor
- Estrés

Los n renglones de 'Solución' hasta 'DURACION' conforman la solución a la instancia. El
formato de cada renglón es el siguiente:

			Ejemplo: 13_2_1_1_50_1.0
	actividad_subtema_tema_materia_posición_valorDeLaVariableEnElModelo

			Ejemplo: score_s_1_1_1_79.0
	EtiquetaScore_FormaDeEvaluar_subtema_tema_materia_CalificaciónDelSubtema 

La forma de evaluar hace referencia a si se evaluó por subtema, tema o materia, nuestro
modelo considera esas opciones, en este caso la evaluación fue por subtema. Los siguientes
renglones son solo informativos, contienen la Duración y el Valor de cada una de las 88 
actividades y el estrés del estudiante con el que se resolvión la instancia.