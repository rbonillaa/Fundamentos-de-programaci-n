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
		#La tupla contiene el objeto celda del excel para cada variable
		nombre,matricula,genero,paralelo,cod_carrera,veces_tomadas, \
			primer_proyecto,primer_sustent,primer_lecciones,primer_calif_final, \
			primer_exam_tema1,primer_exam_tema2,primer_exam_tema3, \
			segundo_proyecto,segundo_sustent,segundo_lecciones,segundo_calif_final, \
			segundo_exam_tema1,segundo_exam_tema2,segundo_exam_tema3, \
			segundo_exam_tema4,segundo_exam_tema5,segundo_exam_tema6, \
			segundo_exam_tema7,segundo_exam_tema8,segundo_exam_tema9, \
			segundo_exam_tema10, \
			calif_final_practica, \
			tercer_proyecto,tercer_calif_final, \
			tercer_exam_tema1,tercer_exam_tema2,tercer_exam_tema3 = datos[:columnas]

		self.nombre = nombre
		self.matricula = matricula
		self.genero = genero
		self.paralelo = paralelo
		self.cod_carrera = cod_carrera
		self.veces_tomadas = veces_tomadas
		self.actividades = {
			"sustent" : {
				"1er_sustent": primer_sustent, 
				"2do_sustent": segundo_sustent
			},
			"proyecto" : {
				"1er_proyecto":primer_proyecto,
				"2do_proyecto":segundo_proyecto,
				"3er_proyecto":tercer_proyecto
			},
			"lecciones" : { 
				"1er_lecciones":primer_lecciones,
				"2do_lecciones": segundo_lecciones
			},
			"calif_final":{
				"1er_calif_final":primer_calif_final,
				"2do_calif_final":segundo_calif_final,
				"3er_calif_final":tercer_calif_final,
				"calif_final_practica": calif_final_practica
			}		
		}

		self.examen = {
			"1er_exam_": { "tema1": primer_exam_tema1 , "tema2": primer_exam_tema2 , "tema3": primer_exam_tema3 },
			"2do_exam_": { "tema1": segundo_exam_tema1 , "tema2": segundo_exam_tema2 , "tema3": segundo_exam_tema3,
							"tema4":segundo_exam_tema4,"tema5":segundo_exam_tema5,"tema6":segundo_exam_tema6,
							"tema7":segundo_exam_tema7,"tema8":segundo_exam_tema8,"tema9":segundo_exam_tema9,"tema10":segundo_exam_tema10},
			"3er_exam_": { "tema1": tercer_exam_tema1 , "tema2": tercer_exam_tema2 , "tema3": tercer_exam_tema3 }
		}


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
				if calif:
					d[examen+tema] = self.validarNumero(calif,TIPO_NO_NUMERICO) or self.validarCalificacion(calif, FUERA_DE_RANGO, validaciones['examen'][examen][tema])
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