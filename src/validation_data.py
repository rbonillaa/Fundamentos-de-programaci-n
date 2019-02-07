from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from estudiante import Estudiante
import pandas as pd
import sys


#Escriba el nombre del archivo de los datos a validar
if (len(sys.argv)<2):
	print("Error, ingrese el nombre del archivo")
	print("$python3 validation_data.py archivo.xlsx")
	exit()

filename = sys.argv[1]
print("**",filename,"**")



OPCION_NO_VALIDA = 'dato_no_valido'
VACIO = 'dato_vacio'
FUERA_DE_RANGO = 'dato_fuera_de_rango'
NO_REDONDEADO = 'dato_no_redondeado'
TIPO_NO_NUMERICO = 'dato_no_numerico'



def fillCell(cell,color,fill_type=None):
	fill = PatternFill(fgColor=color,fill_type=fill_type)
	cell.fill = fill

def convertirDatosNumericos(estudiante,row,columnas):
	for i,columna in enumerate(columnas):
		if "exam" in columna:
			for examen, temas in estudiante.examen.items():
				for tema, calif in temas.items():
					if calif and examen+tema == columna: 
						row[i].value = calif
		else:
			for actividad,dataD in estudiante.actividades.items():
				for item,calif in dataD.items():
					if calif and item==columna:
						row[i].value = calif

def validateDataSheet(filename,columnas,colores,errorsMessages,validaciones):
	header_rows = 2
	VACIO = errorsMessages[0]
	NO_REDONDEADO = errorsMessages[-1]
	TIPO_NO_NUMERICO = errorsMessages[-2]
	try:
		wb = load_workbook(filename)
		data_sheet = wb["DATA"]
		total_students = data_sheet.max_row - header_rows
		total_columns = data_sheet.max_column 

		print("Total estudiantes a revisar: "+str(total_students))
		total_errors = 0
		for row in data_sheet.iter_rows(min_row=header_rows+1, max_col=total_columns, max_row=data_sheet.max_row):
			data = []
			for cell in row:
				data.append(cell.value)
				fillCell(cell,colores[VACIO]) #Restore cell color
			estudiante = Estudiante(data, len(columnas))
			estudiante.convertir()
			convertirDatosNumericos(estudiante,row,columnas)
			#Luego de convertir datos numéricos, se valida
			errores = estudiante.validar(errorsMessages,validaciones)
			countErrorStudent = 0
			for error, campos in errores.items():
				color = colores[error]
				countErrorStudent += len(campos)
				for columna in campos:
					if columna in columnas:
						i = columnas.index(columna)
						if error==NO_REDONDEADO: #El error detectado es corregido por el script
							row[i].value = estudiante.calif_final[columna]
						else:
							fillCell(row[i],color,'solid') #Errores no corregidos se pintan
			
			if countErrorStudent:
				print('{:<9}{}'.format('FALLÓ',estudiante.nombre))
				total_errors += 1
			else:
				print('{:<9}{}'.format('OK',estudiante.nombre))
		if total_errors:
			print("RESULTADOS: Se detectaron errores en las calificaciones de ", total_errors," estudiantes.")
			print()
			print("Revise su archivo de calificaciones, y corrija los errores de las CELDAS RESALTADAS con los siguientes colores:")
			print("1. Naranja \t --> \t Dato requerido.")
			print("2. Azul \t --> \t Valor no válido, revise la cabecera del archivo modelo para las posibles opciones.")
			print("3. Amarillo \t --> \t Valor fuera del rango posible.")
			#print("4. Verde \t --> \t El dato no es numérico.")
			print("="*150)
			print("**OJO: Los errores tipo dato_no_redondeado y dato_no_numerico fueron corregidos por el script")
		else:
			print("="*150)
			print('¡Felicidades! Tu archivo de excel está listo para ser enviado')
			print('Por favor enviar a rabonilla@espol.edu.ec y a eslozano@espol.edu.ec')
		print("="*150)
		print("Copyright (c) 2018 eslozano")
		print('All Rights Reserved :)')
		wb.save(filename)
	except IOError as e:
		print("ERROR: No." , e.errno , e )
		if e.errno == 2:
			print("El archivo ",filename," no se encuentra en la carpeta del script.")
		if e.errno == 13:
			print("El archivo ",filename," se encuentra abierto.")

def dataAnalysis(filename):
	df = pd.read_excel("filename",skiprows =2)


#Las columnas deben estar en el orden del excel
columnas = ["nombre","matricula","genero","paralelo","cod_carrera","veces_tomadas",
			"1er_proyecto", "1er_sustent","1er_lecciones", "1er_calif_final",
			"1er_exam_tema1","1er_exam_tema2","1er_exam_tema3",
			"2do_proyecto", "2do_sustent","2do_lecciones", "2do_calif_final",
			"2do_exam_tema1","2do_exam_tema2","2do_exam_tema3",
			"2do_exam_tema4","2do_exam_tema5","2do_exam_tema6",
			"2do_exam_tema7","2do_exam_tema8","2do_exam_tema9",
			"2do_exam_tema10",
			"calif_final_practica",
			"3er_proyecto","3er_calif_final",
			"3er_exam_tema1","3er_exam_tema2","3er_exam_tema3"
]
#Los colores en los que se resaltarán las celdas según los errores
colors = {
	VACIO:"ffd8bf", #naranja 
	OPCION_NO_VALIDA: '6aa2fc', #azul 
	FUERA_DE_RANGO: 'fffa00', #amarillo
	TIPO_NO_NUMERICO: '96D701', #verde
	NO_REDONDEADO: 'ff7ff4' #rosado
}

errorsMessages= [VACIO,OPCION_NO_VALIDA,FUERA_DE_RANGO,TIPO_NO_NUMERICO,NO_REDONDEADO]

validaciones = {	
	"genero": ["F","M"],
	"veces_tomadas":[2,3],
	"calif_final": 100,
	"sustent": 1,
	"proyecto": {"1er_proyecto":20,"2do_proyecto":20,"3er_proyecto":25},
	"examen":{
		"1er_exam_": { "tema1": 40, "tema2": 50, "tema3": 10 },
		"2do_exam_": { "tema1": 40, "tema2": 50, "tema3": 10 },
		"3er_exam_": { "tema1": 40, "tema2": 50, "tema3": 10 }
	},
	"lecciones":10,
}

validateDataSheet(filename,columnas,colors,errorsMessages, validaciones)