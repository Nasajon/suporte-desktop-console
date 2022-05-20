# suporte-desktop-console
Ferramenta de console (linha de comando) para execução de rotinas de suporte ao ERP (principalmente para manipulação do banco de dados).

## Atenção

Essa ferramenta de linha de comando é de caráter de suporte, e portanto pode realizar procedimentos de alto risco no banco de dados, e portanto não deve ser utilizada diretamente num BD de produção.

Se for necessário utilizar num ambiente de produção, deve-se utilizar o parâmetro "-n" da linha de comando (ou --new_database), por meio do qual é criado um banco de dados novo, cópia do original, e sobre o qual os procedimentos são realizados (presenrvando o banco original, mas também viabilizando o uso do mesmo servidor de produção).

**Obs.: Caso se utilize o parâmetro "-n", é necessário verificar se há espaço em disco o suficiente para a duplicação do banco de dados.**

## Modo de uso

1. Baixar o `.exe` "suporte-console.exe" mais recente, contido na página de [releases do projeto.](https://github.com/Nasajon/suporte-desktop-console/releases)
2. Executar o script em si (ver sessão do manual da linha de comando).

## Manual da linha de comando

Sintaxe básica de uso:

> ./dist/suporte-console.exe -d {NOME_BANCO} -n {NOME_NOVO_BANCO_TRATADO} -c {COMANDO_DESEJADO}

**Vale destacar que esta sintaxe assume os valores padrões de acesso ao BD: porta ```5432```, usuário ```postgres``` e ```postgres```.**

Além disso, o parâmetro ```--n``` é opcional, mas é recomendado para não causar impactos negativos no BD original (ver mais sobre esse parâmetro na sessão de Atenção, no início desta documentação).

**Obs.: De acordo com o comando escolhido, outros parâmetros podem ser necessários (inclusive podem ser obrigatórios). Donde se torna necessário consultar a documentação do comando desejado.**

### Parâmetros opcionais:

* **-u:** Usuário para conexão com o banco de dados. Valor padrão: ```postgres```
* **-p:** Senha para conexão com o banco de dados. Valor padrão: ```postgres```
* **-t:** IP ou nome do servidor do banco de dados. Valor padrão: ```localhost```
* **-o:** Porta para conexão com o banco de dados. Valor padrão: ```5432```

## LOGs de execução

Cada execução do script criará o arquivo de log:

* ```suporte-console - {ano}-{mes}-{dia}-{hora}-{minuto}.log``` - Contendo o log do processo geral, inclusive erros de FK (esse log também é impresso no console da linha de comando).

No entanto, de acordo com o comando escolhido para execução, outros arquivos de log podem ser criados, e deve-se consultar a respectiva documentação do comando.

## Comandos Disponíveis

### Conversão para o modo empresa

ID do comando (para o parâmetro ```-c```):

> converte_modo_empresa

Este comando tem por objetivo converter um BD para o modo empresa (onde o compartilhamento de dados se dá pelos grupos empresariais, e não pelas empresas). O que é útil para viabilizar o uso de vários módulos do ERP como: Serviços, Finanças, Estoque, etc.

Informações importantes:

* Esse comando não demanda nenhum novo parâmetro para execução.
* Esse script gera um arquivo de log específico, com padrão de nome: ```converte_modo_empresa - {ano}-{mes}-{dia}-{hora}-{minuto}.log```

**Obs.: Esse script é "ireversível" (no sentido de que uma reversão pode gerar manipulação não ideal dos dados). Logo utilize com muita cautela.**


### Exclusão de empresas do banco de dados

ID do comando (para o parâmetro ```-c```):

> exclusao_empresas

Comando destinado à exclusão (em alta performance) de empresas de um banco de dados. [Ver a documentação específica.](suporte_console/exclusao_empresas/README.md)

### Diagnóstico de Conjuntos

ID do comando (para o parâmetro ```-c```):

> diagnostico_conjuntos

Comando destinado a detecção de problemas de conjuntos numa base, tentativas de correção dos tais problemas, e criação de uniques para evitar novos problemas no futuro. [Ver a documentação específica.](suporte_console/diagnostico_conjuntos/README.md)

## Empactoando para Disrtibuição

O comando pode ser empacotado em zip ou exe.

Caso se opte pelo zip, é necessário instalar o Python3.9 (ou maior, ainda dentro da versão 3) e todas as dependências no arquivo requirements.txt, no ambiente que for executado. Já o arquivo executável, pode ser rodado de modo por si só.

Os comandos para empacotar serão apresentados a seguir, mas ambos exportarão para o disretório `dist`:

### ZIP

> python empacotar.py

### EXE

> ./run-pyinstaller.bat