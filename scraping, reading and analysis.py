# -*- coding: utf-8 -*-
"""
Created on Tue May 14 12:52:08 2019

@author: ScmayorquinS
"""
#-----------------------------
# Parte que adelantó Alejandra
#-----------------------------

import requests
from bs4 import BeautifulSoup

# Scraping para extraer los pdfs en los PND desde 1961

# Ejemplo para Alberto Lleras Camargo 1961 - 1070
html = requests.get('https://www.dnp.gov.co/Plan-Nacional-de-Desarrollo/Paginas/Planes-de-Desarrollo-anteriores.aspx').text

# estructurar datos a partir de archivos HTML
soup = BeautifulSoup(html,'lxml')

type(soup)

# presentar HTML en estructura de fácil lectura
pretty = soup.prettify()

soup.title

# Extraer todos capítulos/partes/tomos de los PND
todo = soup.find_all('a')

# Como lo anterior no extrae los nombres de los planes, los extraigo por aparte
planes=soup.find_all('span')
planes

type(planes)

str(planes)

import re

# Extraer solo los nombres de los planes utilizando regex
names=re.findall("FondoGris\">(.+?)<", str(planes))
names

names[1]

anios =re.findall('\d+-\d+', str(names))

'''
#Voy a crear una lista para cada plan, en la cual voy a meter todos los capitulos que le correspondan
for i in range(len(names)):
    anios_i=[]
    anios_i = anios_i.append([names[i],0,0,0])
    print (anios_i)
'''

plans = list(planes)

# Ejemplo para uno
Lleras_Camargo = []
Lleras_Camargo.append(anios[12])
Lleras_Camargo.append(names[12])

#para meterle los capítulos
planes_prueba = list(planes)
capitulos_Lleras_Camargo = planes[129:137]

capitulos_Lleras_Camargo
nombres_capitulos_Lleras_Camargo = re.findall("textoRojo\">(.+?)<", str(capitulos_Lleras_Camargo))

# En 'todo' se encuentran almacenados los links
links_Lleras_Camargo = todo[95:105]

# Sacar un link
link_ejemplo = re.search("(?P<url>https?://[^\s]+)", str(links_Lleras_Camargo[1])).group("url")
links_Lleras_Camargo_final = re.findall("(?P<url>https?://[^\s]+)", str(links_Lleras_Camargo))

#--------------------------
# Parte que adenlató Camilo
#--------------------------

# Extraer todos los links de la página con regex
prueba_links = re.findall("(?P<url>https?://[^\s]+)", str(todo))

# Eliminar links que no pertenecen a capítulos
del(prueba_links[91:113])
del(prueba_links[0:6])
del(prueba_links[0])
del(prueba_links[84])

# Extraer nombre de todos los capítulos y documentos
prueba_capitulos = re.findall("textoRojo\">(.+?)<", str(todo))

# Insertar capítulo faltante de Betancur
prueba_capitulos.insert(40, 'Fundamentos Plan')

# Emparejar ambas listas
del(prueba_capitulos[1])
del(prueba_links[9])


# Eliminar otros pdfs innecesarios
del(prueba_links[0])
del(prueba_links[2])
del(prueba_links[4])
del(prueba_links[4])

# Completar capítulos para empareejar con links
prueba_capitulos.insert(0, 'Santos I Tomo II')
prueba_capitulos.insert(0, 'Santos I Tomo I')
prueba_capitulos.insert(0, 'Santos II Tomo II')
prueba_capitulos.insert(0, 'Santos II Tomo I')

# Limpiar links: quitar " al final de todos
links_limpios = [s.replace('"', '') for s in prueba_links]
links_limpios = [s.replace('><span', '') for s in links_limpios]

# Último plan de desarrollo
duque = 'https://colaboracion.dnp.gov.co/CDT/Prensa/BasesPND2018-2022n.pdf'

# Insertar el documento en la lista y complementar los demás
links_limpios.insert(0, duque)
prueba_capitulos.insert(0, 'Pacto por Colombia pacto por la equidad')
names.insert(0, 'Pacto por Colombia pacto por la equidad (2018-2022) - Iván Duque')
anios.insert(0, '2018-2022')



uribe2_tomo2 = "https://colaboracion.dnp.gov.co/CDT/PND/PND_Tomo_2.pdf"

links_limpios.insert(5, uribe2_tomo2)
prueba_capitulos.insert(5, 'Estado Comunitario_Tomo_2')
names.insert(3, 'Estado Comunitario (2006-2010) - Alvaro Uribe Velez')
anios.insert(3, '2006-2010')

uribe2_tomo1 = "https://colaboracion.dnp.gov.co/CDT/PND/PND_Tomo_1.pdf"
links_limpios.insert(6, uribe2_tomo1)
prueba_capitulos.insert(6, 'Estado Comunitario_Tomo_1')


# Emparejar nombre del plan con capítulos que le corresponde; lista de listas
import itertools
rep_pnds = [names[0]] * 1, [names[1]] * 2, [names[2]] * 2, [names[3]] * 2, [names[4]] * 1, [names[5]] * 9, [names[6]] * 10, [names[7]] * 12, [names[8]] * 7, [names[9]] * 5, [names[10]] * 6, [names[11]] * 5, [names[12]] * 3, [names[13]] * 9, [names[14]] * 8

# desenlistar rep_pnds para tener una sola lista
lista_pnds = list(itertools.chain.from_iterable(rep_pnds))

# Pegar la lista anterior al los links respectivos y sus capítulos en un data frame
import pandas as pd

# Diccionario de cómo quiero dejar del dataframe
dic = {'Planes Nacionales de Desarrollo':lista_pnds, 'Capítulos o tomos':prueba_capitulos, 'Link':links_limpios}

# Dataframe con la información
tabla_pnds = pd.DataFrame(dic, columns = ['Planes Nacionales de Desarrollo','Capítulos o tomos','Link'])

#os.chdir(r'C:/Users/ScmayorquinS/Desktop/PND Python scraping and mining/PDFs')


#-------------------------
# Descargar todos los PDFs
#-------------------------
import os
import requests
import urllib

# Directorio En DNP
directorio_descarga = 'C:/Users/ScmayorquinS/Desktop/PND Python scraping and mining/PDFs'
# Directorio En casa
directorio_descarga =  'C:/Users/CamiloAndrés/Desktop/PND Python scraping and mining/PDFs'

# Enumerar lista de links para mantener el orden al descargarlos
secuencia = list(range(82))

# Para cada link en la lista de links_limpios
i = 0
for url in links_limpios[0:82]:
    # Partir hacia la derecha y tomar el texto que le sigue
    name = str(secuencia[i]) + str('. ') + url.rsplit('/', 1)[-1]

    # Combinar el nombre con el directorio para obtener el path del archivo a guardar
    filename = os.path.join(directorio_descarga, name)

    # Si el archivo no existe, descargarlo
    if not os.path.isfile(filename):
        urllib.request.urlretrieve(url, filename)
    i = i + 1

#--------------------------
# Leer pdfs y extraer texto
#--------------------------
import PyPDF2
# Directorio de trabajo de trabajo de forma absoluta
# Si esta línea no se corre, el for para extraer el texto del pdf leído no funciona por llamar la ruta de forma relativa
# En DNP
os.chdir('C:/Users/ScmayorquinS/Desktop/PND Python scraping and mining/PDFs')
# En casa
os.chdir('C:/Users/CamiloAndrés/Desktop/PND Python scraping and mining/PDFs')


# Cargar todos los pdfs en una lista 

# En DNP
files = os.listdir('C:/Users/ScmayorquinS/Desktop/PND Python scraping and mining/PDFs')
# En casa
files = os.listdir('C:/Users/CamiloAndrés/Desktop/PND Python scraping and mining/PDFs')
files = sorted(files, key=lambda x: int(x.split('.')[0]))

# Lista vacía para rellenar con cada pdf
Database = []

# Para cada archivo de la lista
for FILE in files:
    # Si termina en .pdf, leerlo en formato binario y pegarlo a la lista
    if FILE.endswith('.pdf'):
        data = open(FILE,'rb') 
        Database.append(data)




#----------------------------------------------------------------------------------------------------
# Aquí es donde debería ir el 'for' para extraer el texto de todo, pero por ahora se puede uno por uno:
#----------------------------------------------------------------------------------------------------

# Objeto que lee algún pdf a escoger entre la lista de Database, por el ejemplo el cuarto de acuerdo a como se ordenó
# Hay que arreglar ese orden por el original
reader_prueba = PyPDF2.PdfFileReader(Database[4])

# Extraer el texto de todas las páginas del pdf escogido, la idea es después de todos los pdfs
# Variable que contiene el número de páginas
number_of_pages = reader_prueba.getNumPages()
# Variable para almacenar contenido, un string
page_content=""
# Para cada página en el total de páginas
for page_number in range(number_of_pages):
    # Obtener cada una de las páginas
    page = reader_prueba.getPage(page_number)
    # Extraer el texto de la página y pegárselo a page_content; repetir hasta todas
    page_content += page.extractText()

# Page content tendrá el texto en string de un pdf

#-----------------------

# PDF con su texto
import pandas as pd
import PyPDF2

import time

# Archivos pdf que se dejan leer, están todos excepto los de índice 0,1 y 79
pdf_files_working = files[2:81]

tabla_texto = pd.DataFrame(index = [0], columns = ['PDF','Texto'])

fileIndex = 0

#Tiempo de ejecución del bucle
t0 = time.time()

# Para cada link de los pdfs que se dejan leer
for file in pdf_files_working:
  # abrir en modo binario
  pdfFileObj = open(file,'rb')
  # leer con PyPDF2
  pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
  # Inicia conteo de páginas
  startPage = 0
  # Para rellenar con el texto
  text = ''
  cleanText = ''
  # Mientras que el contador no llegue al número de páginas...
  while startPage <= pdfReader.numPages-1:
    pageObj = pdfReader.getPage(startPage)
    text += pageObj.extractText()
    startPage += 1
  pdfFileObj.close()
  # Para cada palabra dentro del texto leído
  for myWord in text:
    # No sacar spacios
    if myWord != '\n':
      cleanText += myWord
  #text = cleanText.itemize()
  # texto semilimpio
  text = cleanText
  # Crear dataframe de todos los textos
  newRow = pd.DataFrame(index = [0], columns = ['PDF', 'Texto'])
  # ir insertando cada nombre y cada texto en el pdf
  newRow.iloc[0]['PDF'] = file
  newRow.iloc[0]['Texto'] = text
  # Concatenar todos los resultados
  tabla_texto = pd.concat([tabla_texto, newRow], ignore_index=True)        


t1 = time.time()

total = t1-t0

tabla_texto['Texto'][15]


# Insertar texto del Tomo I de Santos II
import glob
os.chdir('C:/Users/ScmayorquinS/Desktop/PND Python scraping and mining/texto tomo I Santos II')
read_files = glob.glob("*.txt")

with open("result.txt", "wb") as outfile:
    for f in read_files:
        with open(f, "rb") as infile:
            outfile.write(infile.read())
# Leer txt
with open('C:/Users/ScmayorquinS/Desktop/PND Python scraping and mining/texto tomo I Santos II/result.txt', 'rb') as f:
    tomo_santos = f.read().decode('latin-1').replace(u'\r', u'')

row = ['Santos 2014-2018 tomo I', tomo_santos]
tabla_texto.loc[0] = row
#-----------------------------------------
# Análisis de texto
#-----------------------------------------

import nltk


# In[84]:


type(tabla_texto['Texto'])


# In[86]:

all_tokens = []
for i in range(len(tabla_texto['Texto'])):
    a_few_tokens = str(tabla_texto['Texto'][i]).split()
    # Remover puntuación
    a_few_tokens_2 = [a_few_tokens.lower() for a_few_tokens in a_few_tokens ]
    all_tokens.append(a_few_tokens_2)
    
all_tokens


# In[87]:


len(all_tokens)


# Hacerle limpieza al texto

# In[88]:

def alpha_f(lista):
    alpha = [w for w in lista if w.isalpha()]
    return  alpha

# Dejar caracteres alfabéticos
alpha = []
for i in range(len(all_tokens)):
    alpha_i = alpha_f(all_tokens[i])
    alpha.append(alpha_i)

#############################################################################
# VAMOS ACÁ
############################################################################
    

# In[89]:


import string
# Tomar los caracteres de puntuación
string.punctuation


# In[90]:


# Añadir caracteres adicionales relevantes encontrados para hacer punctuation strip

punctuation = string.punctuation + '–¡¿”“•\r´'
punctuation


# In[91]:


# Strip punctuation from string

def no_punct(string):
    transtable = string.maketrans('', '', punctuation)
    return string.translate(transtable)


# In[92]:

tokens_no_punc = []
for i in range(len(all_tokens)):
    tokens_iteration = list(map(no_punct, alpha[i]))
    tokens_no_punc.append(tokens_iteration)
tokens_no_punc


# In[93]:



# In[94]:


# Quitar números
#alpha = [w for w in lower if not w.isdigit()]
#alpha


# In[95]:


len(alpha)


# In[96]:


#Para mirar cuántas palabras únicas hay
len(set(alpha))





# In[98]:


from nltk.corpus import stopwords
# Grab stopwords in Spanish
stopwords_esp = stopwords.words('spanish')
stopwords_esp


# In[99]:


# Filtrar la lista de todos los tokens con base en la lista de words_of_interest
tokens_no_stop = []
for i in range(len(tokens_no_punc)):    
    tokens_no_stop_i = [w for w in tokens_no_punc[i] if w not in stopwords_esp]
    tokens_no_stop.append(tokens_no_stop_i)
tokens_no_stop


# In[100]:

# recortar lista

parte_1 = tokens_no_stop[0:15]
part_2 = tokens_no_stop[45:49]
part_3 = tokens_no_stop[75]

tokens_no_stop_all = []
tokens_no_stop_all.append(parte_1)
tokens_no_stop_all.append(part_2)


tokens_no_stop_all = list(itertools.chain.from_iterable(tokens_no_stop_all))
tokens_no_stop_all.append(part_3)

freqdist = nltk.FreqDist(tabla_texto['Texto'][11])
freqdist.most_common()

#no_imagen =  itertools.chain.from_iterable(tokens_no_stop_all)

freqdist = []
for i in range(len(tokens_no_stop_all)):
    freqdist_i = nltk.FreqDist(tokens_no_stop_all[i])
    freqdist.append(freqdist_i)

ensayo = freqdist[10].most_common()


# In[102]:


# De la inspección de la distribución de frecuencia, hacer una lista de palabras de no interés
# Por planes de desarrollo

not_of_interest = [".",'¨','ccaammbbiioo','ppaarraa','ccoonnssttrruuiirr','llaa','ppaazz','iii', "así", "través", "b", "c", "d", "cada", "tal", "p", "j", "f", "km", "g", "h","'", ' ','a','e','i','o','r','n','s','c','t','d','l','p','m','u','ó','g','b','v','f','í','á','z','j','h','y','é','q','x','ú','ñ','ˇ','š','ﬁ','ˆ','œ','k','ﬂ','ł','w','[',']','ü','ò','è']


# In[112]:


# Filter list of all tokens based on list of words of interest
tokens_of_interest = []
for i in range(len(tokens_no_stop_all)):
    tokens_of_interest_i = [w for w in tokens_no_stop_all[i] if w not in not_of_interest]
    tokens_of_interest.append(tokens_of_interest_i)

# Frecuencia
#freqdist_2 = nltk.FreqDist(str(tokens_of_interest))
#freqdist_2.most_common()

freqdist_2 = []
for i in range(len(tokens_of_interest)):
    freqdist_i = nltk.FreqDist(tokens_of_interest[i])
    freqdist_2.append(freqdist_i)

ensayo = freqdist_2[10].most_common()

# Ordenar de más viejo a nuevo
tokens_of_interest = tokens_of_interest[::-1]

# In[113]:


# In[114]:


# Para aplicar métodos de objetos nltk.Text:

no_imagen =  itertools.chain.from_iterable(tokens_of_interest)
tokens_nltk = nltk.Text(no_imagen)
tokens_nltk


# objeto para cada plan
tokens_enlistados = []
for i in range(len(tokens_of_interest)):
    tokens_enlistados_i = nltk.Text(tokens_of_interest[i])
    tokens_enlistados.append(tokens_enlistados_i)


# In[116]:


# Palabras SCTI
tokens_nltk.concordance("tecnología")
tokens_nltk.concordance("innovación")
tokens_nltk.concordance("patentes")
tokens_nltk.concordance("emprendimiento")

# Palabras SPIC
tokens_nltk.concordance("formalización")
tokens_nltk.concordance("turismo")
tokens_nltk.concordance("competitividad")
tokens_nltk.concordance("productividad")


# In[117]:

# Palabras SCTI
tokens_nltk.similar("tecnología")
tokens_nltk.similar("innovación")
tokens_nltk.similar("patentes")
tokens_nltk.similar("emprendimiento")

# Palabras SPIC
tokens_nltk.similar("formalización")
tokens_nltk.similar("turismo")
tokens_nltk.similar("competitividad")
tokens_nltk.similar("productividad")


# In[120]:


import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = [18.0, 8.0]


# Defino las palabras a analizar con base en la descripción de la Dirección de Innovación y Desarrollo Empresarial en la página del DNP

# In[122]:


scti = ["ciencia", "tecnología", "innovación", "cti", "adopción", "tecnológica","conocimiento", "propiedad", "intelectual", "patentes", "emprendimiento"]
scti


# In[124]:


spic = ["productividad", "competitividad", "formalización", "internacionalización", "comercio", "exterior", "turismo"]
spic


# In[125]:


tokens_nltk.dispersion_plot(scti);


# In[126]:


tokens_nltk.dispersion_plot(spic);


# ## Frecuencia de las palabras para hacer nube de palabras en wordart y gráficos en tableau

# In[129]:

# Para guardar en excel
os.chdir('C:/Users/ScmayorquinS/Desktop/PND Python scraping and mining')

# Lista de palabras para todos los PNDs
for i in scti:
    x =tokens_nltk.count(i)
    print (i,x)

# Lista de palabras para cada PND
for element in range(len(tokens_enlistados)):
    for word in scti:
        x = tokens_enlistados[element].count(word)
        print (word, x)





# In[130]:

# Lista de palabras para todos los PNDs
for i in spic:
    x =tokens_nltk.count(i)
    print (i,x)

# Lista de palabras para cada PND
for element in range(len(tokens_enlistados)):
    for word in spic:
        x = tokens_enlistados[element].count(word)
        print (word, x)





# Guardar un objeto

# Step 1
import pickle
 

 # Step 2
with open('tabla_texto.py', 'wb') as tabla_texto_file:
 
  # Step 3
  pickle.dump(tabla_texto, tabla_texto_file)
  
  
# Cargar objeto
  # Step 2
with open('tabla_texto.py', 'rb') as tabla_texto_file:
 
    # Step 3
    tabla_texto2 = pickle.load(tabla_texto_file)
    
    
# Excel
tabla_texto.to_excel("tabla_texto.xlsx")

pd.DataFrame(data=tokens_of_interest)
data.to_excel("data.excel")
