"""Recortes aplicados a las infografías de origen.

Las dos infografías que aportó el autor traen seis cajas cada una. Solo cuatro se
reutilizan como imagen en la presentación (A1, A2, A3 y A4); las ocho restantes se
reemplazaron por gráficos nativos de PowerPoint porque su texto contenía erratas o
afirmaciones que el informe no sostiene.

A3 se recorta por arriba y por abajo: su título original («RAG Contextual para Evitar
Alucinaciones») y su pie («... eliminando alucinaciones en modelos más pequeños»)
afirman que la recuperación elimina las alucinaciones, lo que contradice §5.4 del
informe, donde deepseek-r1:1.5b llega al 21,59 % precisamente con recuperación. El
título y el pie se rehacen como texto nativo en la lámina 14.
"""
from PIL import Image

# A3.png mide 861x633. Se conserva la banda central, sin título ni pie.
Image.open("cajas/A3.png").crop((0, 76, 861, 536)).save("cajas/A3c.png")
