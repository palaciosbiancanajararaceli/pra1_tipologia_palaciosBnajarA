# Librerias utilizadas
import requests
from bs4 import BeautifulSoup
import pandas as pd
from random import randint
from time import sleep

# Construcción scraper

class bestsellers_scraper():

    
    def __contenido_pagina(self, pagina_url):
        #´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´
        # Esta función utiliza la librería requests para acceder al contenido de
        # la web, mostrando un aviso si se produce un error durante el proceso.
        # Posteriormente se parsea el contenido de la web con BeautifulSoup
        #´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´
        page = requests.get(pagina_url)
        if page.status_code != 200:
            raise Exception('Error al acceder al contenido de la web')
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup


    def __titulo_autor(self, libro):
        #´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´
        # Esta función busca y devuelve el título del libro y el nombre del autor
        # dentro del resultado obtenido con BeautifulSoup
        # Si no se encuentra registrado se devuelve el valor 'None'
        #´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´
        titulo_autor = libro.find_all('div', class_="_cDEzb_p13n-sc-css-line-clamp-1_1Fn1y")
        if len(titulo_autor) < 2:
            titulo_doc = libro.find_all('div', class_="_cDEzb_p13n-sc-css-line-clamp-2_EWgCb")
            if len(titulo_doc)<1:
                titulo = 'None'  
            else:
                titulo = titulo_doc[0].text
            autor_doc = libro.find_all('div', class_="_cDEzb_p13n-sc-css-line-clamp-1_1Fn1y")
            if len(autor_doc)<1:
                autor = 'None'  
            else:
                autor = autor_doc[0].text
        else:
            titulo = titulo_autor[0].text
            autor = titulo_autor[1].text
        return titulo, autor


    def __precio_libro(self, libro):
        #´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´
        # Esta función busca y devuelve el precio del libro
        # Si no se encuentra registrado se devuelve el valor 'None'
        # Se elimina el símbolo del € para solo mostrar la cifra numérica
        #´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´
        precio_doc = libro.find('span', class_="p13n-sc-price")
        if precio_doc == None:
            precio = 'None'  
        else:
            precio = precio_doc.text.strip('€')
        return precio


    def __puntuacion_numreviews(self, libro):
        #´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´
        # Esta función busca y devuelve la puntuación media del libro y el nº de reseñas
        # Si no se encuentran registrados se devuelve el valor 'None'
        #´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´
        puntuacion_numreviews = libro.find('div', class_="a-icon-row")
        if puntuacion_numreviews == None:
            puntuacion = 'None'
            num_reviews = 'None'
        else:
            puntuacion = puntuacion_numreviews.find('i').text.split(' ')[0]
            reviews = puntuacion_numreviews.find('span', class_="a-size-small").text
            num_reviews = ''
            for i in reviews.split(','):
                num_reviews += i
        return puntuacion, num_reviews


    def __datos_libro(self, libro):
        #´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´
        # Esta función aplica las funciones definidas con anterioridad
        # para obtener el título, autor, puntuación, nº reseñas y precio
        # Además busca en el contenido de la página para obtener el ranking y la portada
        # Todo esto lo hace para un único libro
        #´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´
        ranking = libro.find('span', class_="zg-bdg-text").text.strip('#')
        portada = libro.find('img')['src']
        titulo, autor = self.__titulo_autor(libro)
        puntuacion, num_reviews = self.__puntuacion_numreviews(libro)
        precio = self.__precio_libro(libro)
        sleep(randint(1,5))
        return {
            'ranking' : ranking,
            'titulo' : titulo,
            'autor' : autor,
            'precio_euros' : precio,
            'puntuacion' : puntuacion,
            'num_reviews' : num_reviews,
            'portada' : portada
        }


    def __datos_libros_full(self, libro_info):
        #´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´
        # Esta función recibe toda la información de todos los libros de la página
        # Es decir, el contenido de la web donde se encuentra la información que las anteriores funciones
        # irán encontrando. Inicia un diccionario vacío sobre el que se incluirá la información de cada libro
        # Utiliza la función datos_libro() para obtener las variables del dataset para cada uno de los libros
        #´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´
        libro_dict = {
            'ranking' : [],
            'titulo' : [],
            'autor' : [],
            'precio_euros' : [],
            'puntuacion' : [],
            'num_reviews' : [],
            'portada' : []
        }
        sleep(randint(1,5))
    
        for item in libro_info:
            datos_libros_full = self.__datos_libro(item)
            libro_dict['ranking'].append(datos_libros_full['ranking'])
            libro_dict['titulo'].append(datos_libros_full['titulo'])
            libro_dict['autor'].append(datos_libros_full['autor'])
            libro_dict['precio_euros'].append(datos_libros_full['precio_euros'])
            libro_dict['puntuacion'].append(datos_libros_full['puntuacion'])
            libro_dict['num_reviews'].append(datos_libros_full['num_reviews'])
            libro_dict['portada'].append(datos_libros_full['portada'])
        
        return libro_dict


    def bestsellers_scraper(self, num_paginas=1):
        #´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´
        # Esta función realiza el proceso de scraping completo 
        # y devuelve el dataset final en formato .csv
        # Su argumento de entrada es el número de páginas 
        # que queremos incluir a la hora de recopilar los bestsellers. 
        # 1 página = 50 libros bestsellers.
        #´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´
        libros_total = []
        for pagina in range(1, num_paginas+1):
            # se modifica el url para recoger información de otras páginas
            pagina_url =  f'https://www.amazon.es/gp/bestsellers/books/ref=zg_bs_pg_{pagina}?ie=UTF8&pg={pagina}'
   
            soup = self.__contenido_pagina(pagina_url)
            sleep(randint(1,5))
    
            # para cada libro, se extrae su información de la página web
            libro_info = soup.find_all('div', id='gridItemRoot')
            libros_total += libro_info
        libro_dict = self.__datos_libros_full(libros_total) # se unifica la info extraída del conjunto de libros
        bestseller_df = pd.DataFrame(libro_dict) # df con la info de todos los libros
        bestseller_df.to_csv(f'amazon_{num_paginas*50}bestsellers.csv', index = True) # se guarda el df en un fichero .csv

