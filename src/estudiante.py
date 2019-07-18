import random as rd

class Estudiante:
	nombre = None
	matricula = None
	genero = None
	paralelo = None
	cod_carrera = None
	veces_tomadas= None
	sustent = None
	proyecto = None
	examen = None
	calif_final = None
	lecciones = None

	def __init__(self, datos, columnas):

		self.nombre = datos[0]
		self.matricula = datos[1]
		self.genero = datos[2]
		self.paralelo = datos[3]
		self.cod_carrera = datos[4]
		self.veces_tomadas = datos[5]
		self.actividades = {
			"sustent" : {
				"1er_sustent": datos[columnas.index("1er_sustent")], 
				#"2do_sustent": datos[columnas.index("2do_sustent")]
			},
			"proyecto" : {
				"1er_proyecto":datos[columnas.index("1er_proyecto")],
				#"2do_proyecto":datos[columnas.index("2do_proyecto")],
				#"3er_proyecto":datos[columnas.index("3er_proyecto")]
			},
			"lecciones" : { 
				"1er_lecciones":datos[columnas.index("1er_lecciones")],
				#"2do_lecciones":datos[columnas.index("2do_lecciones")]
			},
			"calif_final":{
				"1er_calif_final":datos[columnas.index("1er_calif_final")],
				#"2do_calif_final":datos[columnas.index("2do_calif_final")],
				#"3er_calif_final":datos[columnas.index("3er_calif_final")],
				#"calif_final_practica": datos[columnas.index("calif_final_practica")]
			}		
		}

		examen_dict = {}
		#exam_list = ["1er_exam_","2do_exam_","3er_exam_"]
		exam_list = ["1er_exam_"]
		for exam in exam_list:
			q = {}
			for i,c in enumerate(columnas):
				if c == None:
					continue
				if exam in c:
					q[c] = datos[i]
			examen_dict[exam]=q

		self.examen = examen_dict

	def validarDatoVacio(self,dato,VACIO):
		if not dato and dato!=0:
			return VACIO

	def validarGenero(self,genero,OPCION_NO_VALIDA, generos):
		if genero not in generos:
			return OPCION_NO_VALIDA

	def validarVecesTomadas(self,veces_tomadas,OPCION_NO_VALIDA,veces):
		if veces_tomadas and veces_tomadas not in veces:
			return OPCION_NO_VALIDA

	def validarCalificacion(self,calificacion,FUERA_DE_RANGO, max):
		if not 0<=calificacion<=max:
			return FUERA_DE_RANGO

	def validarRedondeo(self,calificacion,NO_REDONDEADO):
		if isinstance(calificacion, float):
			return NO_REDONDEADO

	def validarNumero(self,calificacion,TIPO_NO_NUMERICO):
		if not isinstance(calificacion,float) and not isinstance(calificacion, int):
			return TIPO_NO_NUMERICO

	def validarDatos(self,errores_mensajes,validaciones):
		VACIO,OPCION_NO_VALIDA,FUERA_DE_RANGO,TIPO_NO_NUMERICO,NO_REDONDEADO = errores_mensajes #Editar en caso de agregar mas mensajes
		d = {}
		d['nombre'] = self.validarDatoVacio(self.nombre,VACIO)
		d['matricula'] = self.validarDatoVacio(self.matricula,VACIO)
		d['paralelo'] = self.validarDatoVacio(self.paralelo,VACIO)
		d['cod_carrera'] = self.validarDatoVacio(self.cod_carrera,VACIO)
		d['veces_tomadas'] = self.validarVecesTomadas(self.veces_tomadas,OPCION_NO_VALIDA,validaciones['veces_tomadas'])
		#Variables con más validaciones
		d['genero'] = self.validarDatoVacio(self.genero,VACIO) or self.validarGenero(self.genero,OPCION_NO_VALIDA, validaciones['genero'])

		for actividad, califD in self.actividades.items():
			for nombre,calif in califD.items():
				if calif:
					if actividad=="proyecto":
						valorValidacion = validaciones['proyecto'][nombre]
					else:
						valorValidacion = validaciones[actividad]
					validacion = self.validarNumero(calif,TIPO_NO_NUMERICO) or self.validarCalificacion(calif, FUERA_DE_RANGO, valorValidacion )
					if actividad=="calif_final":
						validacion = validacion or self.validarRedondeo(calif,NO_REDONDEADO)
					d[nombre] = validacion

		for examen, temas in self.examen.items():
			for tema, calif in temas.items():
				if calif!=None:
					d[tema] = self.validarNumero(calif,TIPO_NO_NUMERICO) or self.validarCalificacion(calif, FUERA_DE_RANGO, validaciones['examen'][examen][tema])
				else:
					#d[tema] = VACIO
					print("** Warning ",self.nombre, " tiene el ",tema, " vacio")
		return d

	def validar(self, errores_mensajes,validaciones):
		validaciones = self.validarDatos(errores_mensajes,validaciones)
		errores  = {}
		for e in errores_mensajes:
			errores[e]=[]
		for campo, validacion in validaciones.items():
			if validacion:
				errores[validacion].append(campo)
		return errores

	def convertir(self):
		for actividad, califD in self.actividades.items():
			for nombre,calif in califD.items():
				if calif:
					if actividad == "calif_final": #Notas finales siempre deben ser redondeadas
						valor = int(calif)
					else:
						valor = float(calif)
					self.actividades[actividad][nombre] = valor

		for examen, temas in self.examen.items():
			for tema, calificacion in temas.items():
				if calificacion:
					self.examen[examen][tema] = float(calificacion)