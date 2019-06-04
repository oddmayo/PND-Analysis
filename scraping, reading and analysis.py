# -*- coding: utf-8 -*-
"""
Created on Tue May 14 12:52:08 2019

@author: ScmayorquinS
"""

# Necessary libraries
import requests
from bs4 import BeautifulSoup
import re
import itertools
import pandas as pd
import os
import urllib
import PyPDF2
import time
import glob

#------------------------------------------------
# Scraping to extract PND text since 1961 to 2018
#------------------------------------------------

# Request html
html = requests.get('https://www.dnp.gov.co/Plan-Nacional-de-Desarrollo/Paginas/Planes-de-Desarrollo-anteriores.aspx').text

# Html structure
soup = BeautifulSoup(html,'lxml')

# Easy reading html
pretty = soup.prettify()

# 'a' tag contains every document in web page
documents = soup.find_all('a')

# 'span' tag contains the name of every PND
dirty_names = soup.find_all('span')

# Use regex to extract the names of every PND
names = re.findall("FondoGris\">(.+?)<", str(dirty_names))

# Use regex to extract years from names
years = re.findall('\d+-\d+', str(names))


# Extract every link with regex
links = re.findall("(?P<url>https?://[^\s]+)", str(documents))

# Delete links that do not belong to chapters
del(links[91:113])
del(links[0:6])
del(links[0])
del(links[84])

# Extract name of every chapter
chapters = re.findall("textoRojo\">(.+?)<", str(documents))

# Insert missing chapter from Betancur
chapters.insert(40, 'Fundamentos Plan')

# Match both lists
del(chapters[1])
del(links[9])


# Remove other unnecessary pdfs
del(links[0])
del(links[2])
del(links[4])
del(links[4])

# Insert more missing chapters to match with 'links'
chapters.insert(0, 'Santos I Tomo II')
chapters.insert(0, 'Santos I Tomo I')
chapters.insert(0, 'Santos II Tomo II')
chapters.insert(0, 'Santos II Tomo I')

# Clean links: Remove " at the end of element in list
clean_links = [s.replace('"', '') for s in links]
clean_links = [s.replace('><span', '') for s in clean_links]

# Last PND not available in initial html
duque = 'https://colaboracion.dnp.gov.co/CDT/Prensa/BasesPND2018-2022n.pdf'

# Insert document in pdf list and fill the rest of the lists with its data
clean_links.insert(0, duque)
chapters.insert(0, 'Pacto por Colombia pacto por la equidad')
names.insert(0, 'Pacto por Colombia pacto por la equidad (2018-2022) - Iván Duque')
years.insert(0, '2018-2022')

# Other PND not available in initial html
uribe2_tome2 = "https://colaboracion.dnp.gov.co/CDT/PND/PND_Tomo_2.pdf"

clean_links.insert(5, uribe2_tome2)
chapters.insert(5, 'Estado Comunitario_Tomo_2')
names.insert(3, 'Estado Comunitario (2006-2010) - Alvaro Uribe Velez')
years.insert(3, '2006-2010')

uribe2_tome1 = "https://colaboracion.dnp.gov.co/CDT/PND/PND_Tomo_1.pdf"
clean_links.insert(6, uribe2_tome1)
chapters.insert(6, 'Estado Comunitario_Tomo_1')


# Match number of chapters with its repeating name; list of lists
rep_pnds = [names[0]] * 1, [names[1]] * 2, [names[2]] * 2, [names[3]] * 2, [names[4]] * 1, [names[5]] * 9, [names[6]] * 10, [names[7]] * 12, [names[8]] * 7, [names[9]] * 5, [names[10]] * 6, [names[11]] * 5, [names[12]] * 3, [names[13]] * 9, [names[14]] * 8

# Unlist previous object
lista_pnds = list(itertools.chain.from_iterable(rep_pnds))

#-------------------------------------------------------------------------
# Paste previous list to its respective links and chapters in a data frame
#-------------------------------------------------------------------------

# Dicctionary with the data frame columns
dic = {'Planes Nacionales de Desarrollo':lista_pnds, 'Capítulos o tomos':chapters, 'Link':clean_links}

# Convert dictionary to data frame
pnd_table = pd.DataFrame(dic, columns = ['Planes Nacionales de Desarrollo','Capítulos o tomos','Link'])

#os.chdir(r'C:/Users/ScmayorquinS/Desktop/PND Python scraping and mining/PDFs')

#-----------------------------
# Download in folder every pdf
#-----------------------------

# External folder not in repository (size issue) - DNP
download_directory = 'C:/Users/ScmayorquinS/Desktop/PND Python scraping and mining/PDFs'
# Home
download_directory =  'C:/Users/CamiloAndrés/Desktop/PND Python scraping and mining/PDFs'

# Numerate list of links to keep same order once downloaded
sequence = list(range(82))

# For every link in list: clean_links
i = 0
for url in clean_links[0:82]:
    # Split to the right and take text next to it
    name = str(sequence[i]) + str('. ') + url.rsplit('/', 1)[-1]

    # Combina name with directory to obtain download path
    filename = os.path.join(download_directory, name)

    # If file does no exist, download it
    if not os.path.isfile(filename):
        urllib.request.urlretrieve(url, filename)
    i = i + 1


#---------------------------
# Read pdfs and text extract
#---------------------------
    

# Absolute working directory
# Necessary for relative call inside big loop
# DNP
os.chdir('C:/Users/ScmayorquinS/Desktop/PND Python scraping and mining/PDFs')
# Home
os.chdir('C:/Users/CamiloAndrés/Desktop/PND Python scraping and mining/PDFs')


# Load every pdf in list

# DNP
files = os.listdir('C:/Users/ScmayorquinS/Desktop/PND Python scraping and mining/PDFs')[0:81]
# Home
files = os.listdir('C:/Users/CamiloAndrés/Desktop/PND Python scraping and mining/PDFs')[0:81]
# Natural sort
files = sorted(files, key=lambda x: int(x.split('.')[0]))

# Empty list to fill with every pdf
Database = []

# For each FILE in files
for FILE in files:
    # If ends with .pdf, read it in binary format and append it to the list 
    if FILE.endswith('.pdf'):
        data = open(FILE,'rb') 
        Database.append(data)
        

# pdf that do not throw an error when reading. All but indexes 0,1 and 79
pdf_files_working = files[2:81]

# data frame with contents of all pdfs
tabla_texto = pd.DataFrame(index = [0], columns = ['PDF','Texto'])

fileIndex = 0

# Execution time of loop
t0 = time.time()

# For every pdf that can be read
for file in pdf_files_working:
  # Binary
  pdfFileObj = open(file,'rb')
  # PyPDF2 magick
  pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
  # Start page count
  startPage = 0
  # To be filled with text
  text = ''
  cleanText = ''
  # While counter is less than number of pages
  while startPage <= pdfReader.numPages-1:
    pageObj = pdfReader.getPage(startPage)
    text += pageObj.extractText()
    startPage += 1
  pdfFileObj.close()
  # For every word inside the text
  for myWord in text:
    # Ignore line skips
    if myWord != '\n':
      cleanText += myWord
  # Almost clean text
  text = cleanText
  # Row for every pdf in the data frame
  newRow = pd.DataFrame(index = [0], columns = ['PDF', 'Texto'])
  # Insert each value of the columns per row
  newRow.iloc[0]['PDF'] = file
  newRow.iloc[0]['Texto'] = text
  # Concatenate each generated row to the empty (no so empty after 1 iteration) data frame
  tabla_texto = pd.concat([tabla_texto, newRow], ignore_index=True)        


t1 = time.time()

# 20 minutes to process all pdfs more or less
total = t1-t0


#------------------------------------------------------------
# As reading all text from the pdfs is a expensive operation,
# it is better to save the final object from the loop
#-----------------------------------------------------------

# Saving object as .py in absolute directory
import pickle
 

 # Select name of desired python object
with open('tabla_texto.py', 'wb') as text_table_file:
 
  # Select which object to export
  pickle.dump(tabla_texto, text_table_file)
  
  
# Loading .py object
  # Step 2
with open('tabla_texto.py', 'rb') as text_table_file:
 
    # Step 3
    text_table = pickle.load(text_table_file)
    
    
# If desired, also export to Excel file
tabla_texto.to_excel("tabla_texto.xlsx")

#-------------
# Continuation
#-------------

# Insert text from Santos II Tome I
os.chdir('C:/Users/ScmayorquinS/Desktop/PND Python scraping and mining/texto tomo I Santos II')
read_files = glob.glob("*.txt")

# Condense all chapters into one .txt file
with open("result.txt", "wb") as outfile:
    for f in read_files:
        with open(f, "rb") as infile:
            outfile.write(infile.read())
            
# Read .txt file
with open('C:/Users/ScmayorquinS/Desktop/PND Python scraping and mining/texto tomo I Santos II/result.txt', 'rb') as f:
    santos_tome = f.read().decode('latin-1').replace(u'\r', u'')

# Append row to text_table
row = ['Santos 2014-2018 tomo I', santos_tome]
text_table.loc[0] = row


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








