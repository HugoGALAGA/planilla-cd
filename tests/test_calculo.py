# tests/test_calculo.py
"""Suite de tests para planilla.calculo.

Cubre particiones de equivalencia, valores frontera y tablas de decision
para cada regla de negocio.
"""

import pytest

from planilla.calculo import (
    Planilla,
    bonificacion_incentivo,
    descuento_igss,
    descuento_isr,
    descuento_prestamo,
    isr_anual,
    liquidar,
    pago_horas_extra,
    resumen,
    salario_ordinario,
    valor_hora,
)


# ---------- valor_hora ----------

class TestValorHora:
    @pytest.mark.parametrize("salario_base", [-1, 0])
    def test_salario_invalido_lanza_error(self, salario_base):
        with pytest.raises(ValueError):
            valor_hora(salario_base)

    def test_frontera_minima_valida(self):
        assert valor_hora(0.01) == pytest.approx(0.01 / 240)

    def test_valor_tipico(self):
        assert valor_hora(4000) == pytest.approx(16.6667, rel=1e-4)


# ---------- pago_horas_extra ----------

class TestPagoHorasExtra:
    @pytest.mark.parametrize("horas_extra", [-1, 49])
    def test_fuera_de_rango_lanza_error(self, horas_extra):
        with pytest.raises(ValueError):
            pago_horas_extra(4000, horas_extra)

    def test_frontera_cero(self):
        assert pago_horas_extra(4000, 0) == 0.0

    def test_frontera_maxima_48(self):
        # valor_hora(4000) = 16.6667, *1.5 = 25, *48 = 1200
        assert pago_horas_extra(4000, 48) == pytest.approx(1200.0)

    def test_valor_intermedio(self):
        assert pago_horas_extra(4000, 8) == pytest.approx(200.0)


# ---------- salario_ordinario ----------

def test_salario_ordinario_suma_base_y_extra():
    assert salario_ordinario(4000, 8) == pytest.approx(4200.0)


def test_salario_ordinario_sin_horas_extra():
    assert salario_ordinario(4000, 0) == 4000.0


# ---------- bonificacion_incentivo ----------

class TestBonificacionIncentivo:
    @pytest.mark.parametrize("dias", [-1, 31])
    def test_fuera_de_rango_lanza_error(self, dias):
        with pytest.raises(ValueError):
            bonificacion_incentivo(dias)

    def test_frontera_cero_dias(self):
        assert bonificacion_incentivo(0) == 0.0

    def test_frontera_29_dias_proporcional(self):
        assert bonificacion_incentivo(29) == pytest.approx(250 * 29 / 30)

    def test_frontera_30_dias_completo(self):
        assert bonificacion_incentivo(30) == 250.0

    def test_dia_intermedio_15(self):
        assert bonificacion_incentivo(15) == pytest.approx(125.0)


# ---------- descuento_igss (tabla de decision) ----------

class TestDescuentoIgss:
    def test_afiliado_true_aplica_tasa(self):
        assert descuento_igss(1000, True) == pytest.approx(48.3)

    def test_afiliado_false_no_descuenta(self):
        assert descuento_igss(1000, False) == 0.0

    def test_afiliado_none_no_descuenta(self):
        # Comportamiento real del codigo: None se trata igual que False.
        # No esta en el README, pero es lo que hace la implementacion.
        assert descuento_igss(1000, None) == 0.0


# ---------- isr_anual ----------

class TestIsrAnual:
    @pytest.mark.parametrize("renta", [0, 48000])
    def test_imponible_no_positivo_no_paga(self, renta):
        assert isr_anual(renta) == 0.0

    def test_tramo_1_tipico(self):
        # imponible = 100000, 5%
        assert isr_anual(148000) == pytest.approx(5000.0)

    def test_frontera_exacta_tramo_1(self):
        # imponible = 300000 exacto -> todavia tramo 1 (<=)
        assert isr_anual(348000) == pytest.approx(15000.0)

    def test_frontera_justo_sobre_tramo_1(self):
        # imponible = 300000.01 -> ya es tramo 2
        assert isr_anual(348000.01) == pytest.approx(15000.0007, rel=1e-6)

    def test_tramo_2_tipico(self):
        # imponible = 600000 -> 15000 + 300000*0.07 = 36000
        assert isr_anual(648000) == pytest.approx(36000.0)


# ---------- descuento_isr ----------

class TestDescuentoIsr:
    def test_frontera_exacta_no_paga(self):
        # salario_base=4000 -> renta anual=48000 -> imponible=0
        assert descuento_isr(4000) == 0.0

    def test_tipico_tramo_1(self):
        # salario_base=10000 -> renta anual=120000, imponible=72000
        # isr anual = 3600, mensual = 300
        assert descuento_isr(10000) == pytest.approx(300.0)


# ---------- descuento_prestamo (tabla de decision) ----------

class TestDescuentoPrestamo:
    def test_cuota_negativa_lanza_error(self):
        with pytest.raises(ValueError):
            descuento_prestamo(1000, 1000, -1)

    def test_frontera_margen_cero_no_descuenta(self):
        # ordinario=1000, piso=300; liquido_antes=300 -> margen=0
        assert descuento_prestamo(300, 1000, 500) == 0.0

    def test_margen_negativo_no_descuenta(self):
        assert descuento_prestamo(200, 1000, 500) == 0.0

    def test_cuota_cabe_dentro_del_margen(self):
        # ordinario=1000, piso=300; liquido_antes=1000 -> margen=700
        assert descuento_prestamo(1000, 1000, 500) == 500.0

    def test_cuota_excede_margen_se_limita(self):
        assert descuento_prestamo(1000, 1000, 800) == 700.0

    def test_cuota_cero_no_descuenta(self):
        assert descuento_prestamo(1000, 1000, 0) == 0.0


# ---------- liquidar (integracion) ----------

class TestLiquidar:
    def test_caso_readme_completo(self):
        # salario_base=4000 horas_extra=8 dias_trabajados=30 cuota_prestamo=500
        r = liquidar(
            salario_base=4000,
            horas_extra=8,
            dias_trabajados=30,
            afiliado_igss=True,
            cuota_prestamo=500,
        )
        assert isinstance(r, Planilla)
        assert r.salario_ordinario == pytest.approx(4200.0)
        assert r.bonificacion == pytest.approx(250.0)
        assert r.igss == pytest.approx(202.86)
        assert r.isr == pytest.approx(0.0)
        assert r.prestamo == pytest.approx(500.0)
        assert r.liquido == pytest.approx(3747.14)

    def test_defaults_sin_horas_extra_ni_prestamo(self):
        r = liquidar(salario_base=4000)
        assert r.salario_ordinario == pytest.approx(4000.0)
        assert r.bonificacion == pytest.approx(250.0)
        assert r.prestamo == 0.0

    def test_afiliado_none_no_descuenta_igss(self):
        r = liquidar(salario_base=4000, afiliado_igss=None)
        assert r.igss == 0.0

    def test_prestamo_respeta_piso_del_30_por_ciento(self):
        # cuota enorme, debe quedar limitada por el piso
        r = liquidar(salario_base=4000, cuota_prestamo=999999)
        assert r.liquido == pytest.approx(r.salario_ordinario * 0.30)


# ---------- resumen ----------

def test_resumen_incluye_liquido_y_descuentos():
    r = liquidar(salario_base=4000, horas_extra=8, cuota_prestamo=500)
    texto = resumen(r)
    assert "Liquido" in texto
    assert "Descuentos" in texto