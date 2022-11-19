from scraper import bestsellers_scraper
num_paginas = int(input('Introduzca nº de páginas a extraer (>=1):'))

s = bestsellers_scraper()

# número de páginas a incluir en el dataset final
# 1: los 50 libros más vendidos
# 2: los 100 libros más vendidos
# 3: los 150 libros más vendidos
# 4: los 200 libros más vendidos ...

s.bestsellers_scraper(num_paginas)