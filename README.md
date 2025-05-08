                                           SISTEMA PARA BIBLIOTECA
                                           
📦 **API REST com FastAPI + CSV**

Este projeto consiste no desenvolvimento de uma API RESTful utilizando o framework FastAPI para o gerenciamento de entidades para um sistema de Biblioteca. Os dados são armazenados em arquivos CSV e diversas funcionalidades adicionais foram implementadas para simular um cenário mais próximo do uso real em aplicações web.

🧠 **Entidades Definidas**

Foram implementadas 3 entidades, cada uma com atributos e CSV próprios:

**Produto**

Atributos: id, nome, categoria, preco, data_criacao

**Cliente**

Atributos: id, nome, email, cpf_cnpj, data_cadastro

**Pedido**

Atributos: id, cliente_id, data_pedido, status, valor_total

🚀 **Funcionalidades Implementadas**

Cada entidade possui rotas específicas, e todas as funcionalidades abaixo são aplicadas individualmente a cada uma:

🔄** F1. CRUD Completo**

Criar, ler, atualizar e excluir registros.

As alterações são refletidas diretamente nos arquivos CSV.

📄** F2. Listagem de Registros**

Endpoint que retorna todos os registros cadastrados da entidade.

🔢** F3. Quantidade Total**

Retorna a quantidade de registros existentes no arquivo CSV.

📦** F4. Compactação CSV**

Gera um arquivo .zip contendo o CSV da entidade e permite download.

🔍** F5. Filtros por Atributo**

Permite a filtragem de registros por campos específicos como categoria, intervalo de preço, etc.

🔐** F6. Hash SHA256 do CSV**

Gera e retorna o hash SHA256 do conteúdo do CSV para verificação de integridade.

🧾** F7. Sistema de Logs**

Toda ação executada na API é registrada em um arquivo de log com data, hora e descrição da operação.

🧬 **F8. Conversão CSV → XML**

Converte os dados do CSV em um arquivo XML e disponibiliza para download.

🛠 **Tecnologias Utilizadas**

FastAPI

Pydantic

CSV (builtin csv module)

Hashlib (para SHA256)

Zipfile (para compactação)

Logging (para registrar operações)

XML.etree.ElementTree (para conversão em XML)

🧠** Considerações Finais**

Este projeto visa proporcionar prática com FastAPI, manipulação de dados persistidos em CSV, e implementação de recursos comuns em aplicações reais, como geração de logs, filtros dinâmicos, compactação de arquivos e verificação de integridade via hash.
