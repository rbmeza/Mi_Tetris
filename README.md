# Mi_Tetris
Para correr el Tetris en local se debe:

1. Crear un entorno virtual (El siguiente comando es para Windows):

```
py -3 -m venv .venv
```

2. Activar el entorno virtual:
```
.venv\Scripts\activate
```

3. Instalar la librería de pygame:
```
pip install pygame
```

4. Iniciar el juego:
```
python Tetris.py 
```

Mi solución tiene la implementación del sistema de rotación solicitado, la random bag y la eliminación de las líneas completadas. El resto de funcionalidades no las pude implementar debido a que me encontré en el camino con un funcionamiento extraño del juego. Este "bug" sucede cuando se genera una pieza "I", la cual luego de caer, deja de generar el resto de piezas (a pesar de sacarlas correctamente de la random bag) y sólo muestra la próxima "I" que se saca de la bolsa.
