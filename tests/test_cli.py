# tests/test_cli.py
"""Suite de tests para planilla.cli."""

from planilla.cli import main, parse_args


# ---------- parse_args ----------

class TestParseArgs:
    def test_pares_bien_formados(self):
        datos = parse_args(["salario_base=4000", "horas_extra=8"])
        assert datos == {"salario_base": 4000.0, "horas_extra": 8.0}

    def test_argumentos_sin_igual_se_ignoran(self):
        datos = parse_args(["salario_base=4000", "basura", "--help"])
        assert datos == {"salario_base": 4000.0}

    def test_valor_no_numerico_se_conserva_como_texto(self):
        datos = parse_args(["afiliado_igss=no"])
        assert datos == {"afiliado_igss": "no"}

    def test_lista_vacia(self):
        assert parse_args([]) == {}


# ---------- main ----------

class TestMain:
    def test_sin_salario_base_imprime_uso_y_retorna_1(self, monkeypatch, capsys):
        monkeypatch.setattr("sys.argv", ["planilla"])
        codigo = main()
        salida = capsys.readouterr().out
        assert codigo == 1
        assert "uso:" in salida

    def test_con_salario_base_retorna_0_e_imprime_resumen(self, monkeypatch, capsys):
        monkeypatch.setattr("sys.argv", ["planilla", "salario_base=4000"])
        codigo = main()
        salida = capsys.readouterr().out
        assert codigo == 0
        assert "Liquido" in salida

    def test_afiliado_igss_no_excluye_del_igss(self, monkeypatch, capsys):
        monkeypatch.setattr(
            "sys.argv",
            ["planilla", "salario_base=4000", "afiliado_igss=no"],
        )
        main()
        salida_no_afiliado = capsys.readouterr().out

        monkeypatch.setattr("sys.argv", ["planilla", "salario_base=4000"])
        main()
        salida_afiliado = capsys.readouterr().out

        # Con IGSS descontado el liquido es menor.
        assert salida_no_afiliado != salida_afiliado

    def test_afiliado_igss_valor_numerico_no_excluye_bug(self, monkeypatch, capsys):
        """Documenta un comportamiento real de la CLI, no una regla del README.

        parse_args convierte 'afiliado_igss=0' a float(0.0). La comparacion
        en main() es `datos.get(...) != "no"`, y `0.0 != "no"` es True, asi
        que el usuario queda afiliado igual, aunque su intencion (0 = no)
        sea la contraria.
        """
        monkeypatch.setattr(
            "sys.argv",
            ["planilla", "salario_base=4000", "afiliado_igss=0"],
        )
        main()
        salida_con_cero = capsys.readouterr().out

        monkeypatch.setattr("sys.argv", ["planilla", "salario_base=4000"])
        main()
        salida_default_afiliado = capsys.readouterr().out

        # Mismo resultado que estar afiliado: el "0" no tuvo efecto.
        assert salida_con_cero == salida_default_afiliado