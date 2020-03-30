import bs4, requests, re, time, sys

url = 'https://www.elespectador.com/search'
selector = '?page='
lista_paginas = []
lista_articulos = []
print('URL = ' + url)
res = requests.get(url)
res.raise_for_status()
print(res)
#crear lista de páginas en .txt
lista_paginas_guardada = open('lista_paginas.txt', 'w')
lista_paginas_guardada.write('Lista de páginas ' + url)
lista_paginas_guardada.close()

soup = bs4.BeautifulSoup(res.text, 'lxml')
last = soup.select('body > div.l-page > div > div.l-content > div.search-api-page-results > ul > li.pager__item.pager__item--last > a')
last_regex = re.compile(r'\d\d\d\d\d')
last_mo = last_regex.search(str(last))
last_num = int(last_mo.group())
print('Número de páginas = ' + str(last_num))

#def buscadorElespectador(url):
	#iterar por cada página del buscador, guardarlas en lista_paginas y appendear el .txt
for i in range(1, (last_num + 1)):
	print('Página ' + str(i))
	seq = str(i)
	pagina = url + selector + seq
	print(pagina)

lista_paginas.append(pagina)
lista_paginas_guardada = open('lista_paginas.txt', 'a')
lista_paginas_guardada.write(lista_paginas)
lista_paginas_guardada.close()


#ir a cada página y guardar cada artículo en lista_articulos
#for i in lista_paginas:
#	res2 = requests.get(i)
#	res2.raise_for_status()
#	soup2 = bs4.BeautifulSoup(res2.text, 'lxml')
#	links = soup2.select('h3 > a')
#	lista_articulos.append(links)
#	print(lista_articulos)
	#time.sleep(20

for i in lista_paginas:
	res3 = requests.get(i)
	soup3 = bs4.BeautifulSoup(res3.text, 'lxml')
	links = soup3.select('h3 > a')
	lista_articulos.append(links)
	print(lista_articulos)

	#for link in links:
		#buscar links y hacer lista	
		#href = re.compile(r'"(.*?)"')
		#mo = href.search(str(link))
		#link_b = mo.group()
		#link = link_b[1:-1]
		#articulo = url + link
		#print(articulo)
		#lista.append(articulo)
		#abrir links
		#resArt = requests.get(articulo)	
		#soup2 = bs4.BeautifulSoup(resArt.text, 'lxml')

		#si hay caricatura, omitir
		#caricatura = 'field--name-field-cartoon'

		#if caricatura in resArt.text == True:
			#break
		#else:	
			#texto = soup2.select('p')
			#print(texto)
#buscadorElespectador(url)
print(lista_articulos)