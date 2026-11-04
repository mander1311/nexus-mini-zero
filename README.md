# NEXUS MINI ZERO

Aplicativo local e desktop para gestão de oportunidades de produtos de afiliado.

## Visão geral

A V1 do NEXUS MINI ZERO inclui:
- banco SQLite local persistente
- dashboard com métricas principais
- cadastro, edição e exclusão de produtos
- calculadora de comissão com projeções
- pontuação `balanced` explicável
- gerador de textos para divulgação
- inicializador para abrir a interface local em um clique

## Requisitos

- Python 3.10+
- Windows 10 ou 11

## Instalação

1. Abra a pasta do projeto.
2. Execute:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Inicie a aplicação:
   ```bash
   python app.py
   ```
   ou
   ```bash
   python launcher.py
   ```
4. O navegador abrirá a interface em `http://127.0.0.1:5000`.

## Empacotamento para Windows

No Windows, execute:

```bat
build.bat
```

O executável será gerado em `dist\NEXUS_MINI_ZERO.exe`.

## Observações

- Os dados ficam salvos em `data/nexus.db`.
- A aplicação não inventa dados automáticos de marketplace.
- A pontuação e as projeções são estimativas, não garantias de venda.
