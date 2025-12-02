🧮 VGBL Portabilidade Checker

Ferramenta em Python para validar automaticamente a soma de valores em arquivos TXT, garantindo consistência antes de etapas importantes de um processo.

📌 Problema

No processo de portabilidade entre entidades previdenciárias, o valor total das contribuições é gerado em um arquivo .txt padronizado conforme regras da plataforma SIDE.

Porém:
- As contribuições são armazenadas internamente com 9 casas decimais nos centavos (alta precisão).
- O arquivo SIDE exige valores com apenas 2 casas decimais.
- Essa redução gera arredondamentos matemáticos.
- O resultado final pode não bater com o saldo real do VGBL, causando rejeições e inconsistências.
- Isso leva a retrabalho, reenvio de arquivos e impactos operacionais no processo de portabilidade.

🎯 Objetivo da Ferramenta
Automatizar a conferência do valor total das contribuições do arquivo .txt antes do envio, garantindo consistência e evitando erros de soma.

A aplicação:
- Lê o arquivo .txt na pasta da aplicação
- Identifica cada contribuição
- Soma automaticamente os valores informados
- Exibe para o usuário o total encontrado
- Solicita o valor correto informado pela entidade
- Recalcula e compara
- Informa se a soma do arquivo corresponde ao valor esperado
- Tudo isso em uma interface simples (estilo Prompt de Comando), facilitando auditorias rápidas.

🧪 Exemplo de Execução
- Lendo arquivo portabilidade.txt…
- Total encontrado no arquivo: 12.345,67
- Informe o valor correto esperado: 12.345,67
- ✔ A soma do arquivo confere com o valor informado.

💼 Impacto no Negócio
A ferramenta contribui diretamente para:
- Evitar rejeições de portabilidade por inconsistência de valores
- Reduzir retrabalho entre equipes de Previdência e Tecnologia
- Padronizar a validação dos arquivos enviados via SIDE
- Minimizar erros causados por arredondamentos inevitáveis
- Aumentar a confiabilidade operacional no processo de portabilidade
- Melhorar o SLA no relacionamento com instituições financeiras
- Uma automação pequena, mas com impacto real no dia a dia operacional.

⚙️ Funcionalidades

✔ Leitura automática de arquivos TXT no padrão SIDE

✔ Soma precisa das contribuições

✔ Comparação do valor interno × valor informado

✔ Validação final antes do envio à instituição financeira

✔ Interface simples e direta (CLI)

✔ Versão compilada em .exe (opcional)

🛠 Tecnologias Utilizadas
- Python 3.11
- Manipulação de arquivos TXT
- PyInstaller (para geração opcional de executável)
- IA generativa como apoio no desenvolvimento

🖥️ Como usar

Via executável (.exe) -> Coloque o arquivo TXT na mesma pasta do .exe -> Execute o programa -> Informe o valor correto quando solicitado -> Veja a validação final.

Via Python (código fonte) pip install -r requirements.txt python main.py

📂 Estrutura do Projeto

vgbl-portabilidade-checker/

├── ajuste_portabilidade_saida.py

├── entradas/

├── saidas/

├── README.md

└── .gitignore


🤖 Uso de Inteligência Artificial
- A IA generativa foi utilizada como copiloto técnico, auxiliando principalmente em: estruturação da lógica inicial, revisão de código e escrita de documentação.

- O conhecimento do domínio (SIDE, VGBL, arredondamentos e processos operacionais) foi aplicado manualmente.

👤 Autor

Arlindo Júnior Honorato

Product Owner | IA Practitioner.