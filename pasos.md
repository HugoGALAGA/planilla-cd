uv run ruff check . (inicial)
➜ uv run ruff check .
F401 [*] `os` imported but unused
 --> src\planilla\calculo.py:6:8
  |
4 | """
5 |
6 | import os
  |        ^^
7 | from dataclasses import dataclass
8 | from datetime import datetime
  |
help: Remove unused import: `os`
  |
5 |
  - import os
6 | from dataclasses import dataclass
  |

F401 [*] `datetime.datetime` imported but unused
  --> src\planilla\calculo.py:8:22
   |
 6 | import os
 7 | from dataclasses import dataclass
 8 | from datetime import datetime
   |                      ^^^^^^^^
 9 |
10 | VALOR_BONIFICACION = 250.0
   |
help: Remove unused import: `datetime.datetime`
  |
7 | from dataclasses import dataclass
  - from datetime import datetime
8 |
  |

E731 Do not assign a `lambda` expression, use a `def`
  --> src\planilla\calculo.py:23:1
   |
21 | FRACCION_INEMBARGABLE = 0.30
22 |
23 | redondear = lambda x: round(x, 2)
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
help: Rewrite `redondear` as a `def`

E711 Comparison to `None` should be `cond is None`
  --> src\planilla\calculo.py:68:20
   |
66 | def descuento_igss(salario_ordinario_mes, afiliado):
67 |     """Cuota laboral del IGSS sobre el salario ordinario."""
68 |     if afiliado == None:
   |                    ^^^^
69 |         return 0.0
70 |     if not afiliado: return 0.0
   |
help: Replace with `cond is None`

E701 Multiple statements on one line (colon)
  --> src\planilla\calculo.py:70:20
   |
68 |     if afiliado == None:
69 |         return 0.0
70 |     if not afiliado: return 0.0
   |                    ^
71 |     return salario_ordinario_mes * TASA_IGSS
   |

E741 Ambiguous variable name: `l`
   --> src\planilla\calculo.py:120:5
    |
118 | def resumen(planilla):
119 |     """Linea de resumen para imprimir en consola."""
120 |     l = planilla.liquido
    |     ^
121 |     total_descuentos = planilla.igss + planilla.isr + planilla.prestamo
122 |     detalle = f"planilla calculada"
    |

F841 Local variable `detalle` is assigned to but never used
   --> src\planilla\calculo.py:122:5
    |
120 |     l = planilla.liquido
121 |     total_descuentos = planilla.igss + planilla.isr + planilla.prestamo
122 |     detalle = f"planilla calculada"
    |     ^^^^^^^
123 |     return f"Liquido: Q{redondear(l)} | Descuentos: Q{redondear(total_descuentos)}"
    |
help: Remove assignment to unused variable `detalle`

F541 [*] f-string without any placeholders
   --> src\planilla\calculo.py:122:15
    |
120 |     l = planilla.liquido
121 |     total_descuentos = planilla.igss + planilla.isr + planilla.prestamo
122 |     detalle = f"planilla calculada"
    |               ^^^^^^^^^^^^^^^^^^^^^
123 |     return f"Liquido: Q{redondear(l)} | Descuentos: Q{redondear(total_descuentos)}"
    |
help: Remove extraneous `f` prefix
    |
121 |     total_descuentos = planilla.igss + planilla.isr + planilla.prestamo
    -     detalle = f"planilla calculada"
122 +     detalle = "planilla calculada"
123 |     return f"Liquido: Q{redondear(l)} | Descuentos: Q{redondear(total_descuentos)}"
    |

E501 Line too long (108 > 88)
 --> src\planilla\cli.py:7:89
  |
5 | from planilla.calculo import liquidar, resumen
6 |
7 | USO = "uso: planilla salario_base=4000 horas_extra=8 dias_trabajados=30 cuota_prestamo=500 afiliado_igss=si"
  |                                                                                         ^^^^^^^^^^^^^^^^^^^^

E722 Do not use bare `except`
  --> src\planilla\cli.py:19:9
   |
17 |         try:
18 |             datos[clave] = float(valor)
19 |         except:
   |         ^^^^^^
20 |             datos[clave] = valor
21 |     return datos
   |

Found 10 errors.
[*] 3 fixable with the `--fix` option (3 hidden fixes can be enabled with the `--unsafe-fixes` option).