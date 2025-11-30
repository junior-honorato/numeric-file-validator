#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Somar e ajustar arquivo de Portabilidade — LAYOUT FIXO (49..63)
- Lê valores monetários a partir da 3ª linha (janela [49..63], 1-based, inclusiva).
- Imprime todos os valores lidos e, ao final: "Valor Total da Portabilidade no Arquivo:".
- Pede o VALOR CORRETO DO ARQUIVO (entrada tolerante: remove . e , e usa apenas dígitos => centavos).
- Guard-rail: se |Total(incorreto) − ValorCorreto| > R$ 1,00, pede para revisar o valor.
- Ajuste: aplica na PRIMEIRA linha de movimento (da linha 3 em diante), trocando somente o grupo numérico na janela 49..63,
  preservando o restante da linha e o alinhamento (sem deslocar colunas).
- Revalida a soma e só salva em ./saidas/<arquivo>_alterado_SIDE.txt se bater com o Valor Correto.
"""

from __future__ import annotations
from pathlib import Path
from typing import List, Tuple, Optional

POS_INICIO_VAL = 49     # 1-based inclusivo
POS_FIM_VAL    = 63     # 1-based inclusivo
ENCODING = "cp1252"

def pause(msg="Clique Enter para sair..."):
    try:
        input(msg)
    except EOFError:
        pass

def garantir_pastas(base: Path) -> Tuple[Path, Path]:
    entradas = base / "entradas"
    saidas = base / "saidas"
    entradas.mkdir(parents=True, exist_ok=True)
    saidas.mkdir(parents=True, exist_ok=True)
    return entradas, saidas

def listar_txts(entradas: Path):
    arquivos = list(entradas.iterdir())
    txts = [p for p in arquivos if p.is_file() and p.suffix.lower() == ".txt"]
    nao_txts = [p for p in arquivos if p.is_file() and p.suffix.lower() != ".txt"]
    return txts, nao_txts

def selecionar_arquivo(txts: List[Path]) -> Optional[Path]:
    if not txts:
        return None
    if len(txts) == 1:
        return txts[0]
    print("Foram encontrados vários arquivos .TXT na pasta 'entradas':")
    for i, p in enumerate(txts, start=1):
        print(f"  {i}) {p.name}")
    while True:
        escolha = input("Digite o número do arquivo que deseja usar: ").strip()
        if not escolha.isdigit():
            print("Por favor, digite um número válido.\n"); continue
        idx = int(escolha)
        if 1 <= idx <= len(txts):
            return txts[idx-1]
        print("Opção fora do intervalo.\n")

def ler_txt(p: Path, encoding: str = ENCODING) -> str:
    b = p.read_bytes()
    try:
        return b.decode(encoding)
    except UnicodeDecodeError:
        return b.decode("latin-1")

def escrever_txt(p: Path, conteudo: str, encoding: str = ENCODING):
    p.write_bytes(conteudo.encode(encoding))

def format_brl(cents: int) -> str:
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    reais = cents // 100
    cent = cents % 100
    reais_str = f"{reais:,}".replace(",", ".")
    return f"{sign}R$ {reais_str},{cent:02d}"

def parse_valor_correto_usuario(valor_str: str) -> int:
    # Remove tudo exceto dígitos, ponto e vírgula; depois remove . e ,; interpreta resultado como CENTAVOS
    s = "".join(ch for ch in valor_str if ch.isdigit() or ch in ".,")
    if not s:
        raise ValueError("Valor vazio ou sem dígitos.")
    digits = "".join(ch for ch in s if ch.isdigit())
    if not digits:
        raise ValueError("Valor sem dígitos.")
    return int(digits)

def janela_indices() -> Tuple[int, int]:
    # Converte 1-based [49..63] para índices Python [48:63)
    i0 = POS_INICIO_VAL - 1
    j0 = POS_FIM_VAL
    return i0, j0

def achar_grupo_numerico_na_janela(linha: str) -> Optional[Tuple[int, int, int]]:
    """
    Retorna (ini, fim, valor_em_centavos) do PRIMEIRO grupo de dígitos consecutivos dentro da janela [49..63].
    ini/fim são índices Python relativos à linha (slice [ini:fim]). Se não achar, retorna None.
    """
    i0, j0 = janela_indices()
    if i0 >= len(linha): 
        return None
    win = linha[i0:j0]
    # achar 1º dígito
    k = None
    for pos, ch in enumerate(win):
        if ch.isdigit():
            k = pos
            break
    if k is None:
        return None
    # estender até acabar dígitos
    m = k + 1
    while m < len(win) and win[m].isdigit():
        m += 1
    digits = win[k:m]
    if not digits:
        return None
    val = int(digits)  # já está em centavos no arquivo
    # converter para índices absolutos na linha
    ini = i0 + k
    fim = i0 + m
    return ini, fim, val

def extrair_valores(conteudo: str) -> List[Tuple[int, int]]:
    """
    Retorna lista de (linha_idx_1based, valor_em_centavos) para todas as linhas de movimento (>=3) que possuem número na janela.
    """
    linhas = conteudo.split("\r\n")
    valores = []
    for idx, ln in enumerate(linhas, start=1):
        if idx < 3 or not ln.strip():
            continue
        grp = achar_grupo_numerico_na_janela(ln)
        if grp is None:
            continue
        _, _, val = grp
        valores.append((idx, val))
    return valores

def imprimir_valores(valores: List[Tuple[int, int]]):
    total = sum(v for _, v in valores)
    print("-------------------------------------")
    print(f"Valor Total da Portabilidade no Arquivo: {format_brl(total)}\n")
    return total

def ajustar_primeira_linha(conteudo: str, ajuste_centavos: int) -> str:
    """
    Aplica o ajuste na PRIMEIRA linha de movimento (>=3) que tiver grupo numérico na janela 49..63.
    Preserva o que está fora da janela e o ALINHAMENTO: substitui apenas o grupo [ini:fim] por um número
    com o MESMO número de dígitos (left-pad com zeros). Clampa mínimo em 0 e verifica overflow.
    """
    linhas = conteudo.split("\r\n")
    for idx, ln in enumerate(linhas, start=1):
        if idx < 3 or not ln.strip():
            continue
        grp = achar_grupo_numerico_na_janela(ln)
        if grp is None:
            continue
        ini, fim, val_atual = grp
        novo_valor = val_atual - ajuste_centavos  # ajuste>0 → diminuir; ajuste<0 → aumentar
        if novo_valor < 0:
            novo_valor = 0
        width = fim - ini  # quantidade de dígitos originais
        novo_digits = str(novo_valor)
        if len(novo_digits) > width:
            raise ValueError(
                f"O ajuste precisa de {len(novo_digits)} dígitos (excede a largura {width} da janela 49..63)."
            )
        novo_digits = novo_digits.rjust(width, "0")
        linhas[idx - 1] = ln[:ini] + novo_digits + ln[fim:]
        return "\r\n".join(linhas)
    raise ValueError("Nenhuma linha de movimento (>=3) contém valor na janela 49..63.")

def somar_total(conteudo: str) -> int:
    vals = extrair_valores(conteudo)
    return sum(v for _, v in vals)

def main():
    base = Path.cwd()
    entradas, saidas = garantir_pastas(base)
    print("=== Portabilidade - Somar (49..63) e Ajustar (1ª linha de movimento) ===")
    print(f"Pasta de ENTRADA : {entradas}")
    print(f"Pasta de SAÍDA   : {saidas}\n")

    txts, nao_txts = listar_txts(entradas)
    if nao_txts:
        print("Aviso: Arquivos não .TXT encontrados em 'entradas':")
        for p in nao_txts:
            print(f"  - {p.name}")
        print()

    if not txts:
        print("Não há nenhum arquivo .TXT na pasta 'entradas'.")
        pause("Clique Enter para sair...")
        return

    alvo = selecionar_arquivo(txts)
    if not alvo:
        print("Nenhum arquivo selecionado.")
        pause("Clique Enter para sair...")
        return

    conteudo = ler_txt(alvo, ENCODING)

    # 1) Lista e soma
    valores = extrair_valores(conteudo)
    if not valores:
        print("Não encontrei nenhum valor na janela 49..63 a partir da linha 3.")
        pause("Clique Enter para sair...")
        return
    total_incorreto = imprimir_valores(valores)

    # 2) Valor correto (entrada tolerante + guard-rail de 100 centavos)
    while True:
        try:
            vcor = input("Informe o VALOR CORRETO DO ARQUIVO (ex: 1.238,65): ").strip()
            # remove . e , e lê como centavos
            digits = "".join(ch for ch in vcor if ch.isdigit())
            if not digits:
                raise ValueError("Valor vazio ou sem dígitos.")
            valor_cor_tot = int(digits)
            ajuste = total_incorreto - valor_cor_tot
            if abs(ajuste) > 100:
                print("\nATENÇÃO: O valor que você inseriu diferencia bastante do valor contido no arquivo.")
                print("Reveja o valor que você inseriu e tente novamente.\n")
                continue
            break
        except Exception as e:
            print(f"Entrada inválida: {e}\n")

    print(f"\nAjuste calculado (incorreto − correto): {format_brl(ajuste)}  ({ajuste} centavos)")

    # 3) Ajusta a PRIMEIRA linha de movimento
    try:
        conteudo_ajustado = ajustar_primeira_linha(conteudo, ajuste)
    except Exception as e:
        print(f"\nErro ao ajustar a primeira linha de movimento: {e}")
        pause("Clique Enter para sair...")
        return

    # 4) Revalida soma
    total_pos = somar_total(conteudo_ajustado)
    print(f"\nValidação pós-ajuste — Valor Total da Portabilidade no Arquivo: {format_brl(total_pos)}")

    if total_pos != valor_cor_tot:
        delta = total_pos - valor_cor_tot
        print("\nATENÇÃO: A validação falhou — a soma após o ajuste não bate com o Valor Correto informado.")
        print(f"Valor Correto esperado: {format_brl(valor_cor_tot)}")
        print(f"Valor obtido          : {format_brl(total_pos)}")
        print(f"Delta                 : {format_brl(delta)}")
        print("\nPor segurança, o arquivo NÃO foi salvo. Verifique o layout/posições e tente novamente.")
        pause("Clique Enter para sair...")
        return

    # 5) Salva se validou
    out_path = saidas / f"{alvo.stem}_alterado_SIDE{alvo.suffix}"
    escrever_txt(out_path, conteudo_ajustado, ENCODING)

    print("\nArquivo ajustado e VALIDADO com sucesso!")
    print(f"- Saída: {out_path}")
    print(f"- Valor Final: {format_brl(total_pos)}\n")
    pause("Clique Enter para sair...")

if __name__ == "__main__":
    main()
