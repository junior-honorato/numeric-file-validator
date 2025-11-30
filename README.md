# 🧮 VGBL Portabilidade Checker  
Ferramenta em Python para validar e conferir a soma das contribuições em arquivos TXT utilizados no processo de **Portabilidade de Saída** de planos VGBL via plataforma **SIDE**.

---

## 📌 Problema

No processo de portabilidade entre entidades previdenciárias, o valor total das contribuições é gerado em um arquivo **.txt** padronizado conforme regras da plataforma **SIDE**.

Porém:

- As contribuições são armazenadas internamente com **9 casas decimais nos centavos** (alta precisão).
- O arquivo SIDE exige valores com **apenas 2 casas decimais**.
- Essa redução gera **arredondamentos matemáticos**.
- O resultado final pode **não bater com o saldo real do VGBL**, causando rejeições e inconsistências.

Isso leva a retrabalho, reenvio de arquivos e impactos operacionais no processo de portabilidade.

---

## 🎯 Objetivo da Ferramenta

Automatizar a conferência do valor total das contribuições do arquivo `.txt` antes do envio, garantindo consistência e evitando erros de soma.

A aplicação:

1. Lê o arquivo `.txt` na pasta da aplicação  
2. Identifica cada contribuição  
3. Soma automaticamente os valores informados  
4. Exibe para o usuário o total encontrado  
5. Solicita o valor correto informado pela entidade  
6. Recalcula e compara  
7. Informa se a soma do arquivo corresponde ao valor esperado  

Tudo isso em uma interface simples (estilo Prompt de Comando), facilitando auditorias rápidas.

---

## ⚙️ Funcionalidades

- ✔ Leitura automática de arquivos TXT no padrão SIDE  
- ✔ Soma precisa das contribuições  
- ✔ Comparação do valor interno × valor informado  
- ✔ Validação final antes do envio à instituição financeira  
- ✔ Interface simples e direta (CLI)  
- ✔ Versão compilada em `.exe` (opcional)

---

## 🖥️ Como usar

### **Via executável (.exe)**
1. Coloque o arquivo TXT na mesma pasta do `.exe`  
2. Execute o programa  
3. Informe o valor correto quando solicitado  
4. Veja a validação final

### **Via Python (código fonte)**
```bash
pip install -r requirements.txt
python main.py
