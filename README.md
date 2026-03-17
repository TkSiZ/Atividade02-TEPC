# Documentação – Cliente e Servidor TFTP em Python

Este projeto implementa um **cliente e servidor TFTP** utilizando Python e a biblioteca `tftpy`. O script permite realizar **upload e download de arquivos** entre máquinas conectadas à mesma rede utilizando o protocolo TFTP.

O protocolo TFTP (Trivial File Transfer Protocol) é um protocolo simples baseado em **UDP**, geralmente utilizado para transferência de arquivos em redes locais.

---

# 1. Requisitos

Antes de executar o projeto, certifique-se de ter:

- **Python 3.10 ou superior**
- Instalar as dependências necessárias

Instalação das dependências:

```bash
# Execute dentro do seu VENV
python -m pip install -r requirements.txt
```

---

# 2. Estrutura do Projeto

Exemplo de estrutura do diretório:

```
projeto-tftp/
│
├── tftp.py
├── .env
├── config.py
├── tftpboot/
├── tftp.log
└── README.md
```

### Arquivos

- **tftp.py** → script principal que contém o cliente e o servidor
- **.env** → arquivo com variáveis de ambiente
- **tftpboot/** → pasta onde os arquivos serão armazenados no servidor
- **config.py** → script onde cria o .env e tftboot com as permissões e o ip local correto
- **tftpboot.log** → arquivo que registra todas as requisições feitas entre cliente e servidor

---

# 3. Configuração do arquivo `.env`

O arquivo `.env` define os parâmetros de rede utilizados pelo cliente e pelo servidor.

### Exemplo de `.env`

```
SERVER_IP=192.444.8.201
SERVER_BIND=0.0.0.0
```

### Explicação das variáveis

**SERVER_IP**

Endereço IP do servidor TFTP que o cliente irá acessar.

Exemplo:

```
SERVER_IP=192.168.1.100
```

**SERVER_BIND**

Interface de rede onde o servidor irá escutar conexões.

```
SERVER_BIND=0.0.0.0
```

`0.0.0.0` significa que o servidor irá aceitar conexões de **todas as interfaces de rede disponíveis**.

---

# 4. Configuração da rede

Para que o TFTP funcione corretamente, algumas configurações de rede são necessárias.

*   O cliente e o servidor precisam estar conectados à **mesma rede local**.

*   Se estiver usando **hotspot do celular ou rede corporativa**, verifique se os dispositivos conseguem se comunicar entre si.


# 5. Definir a rede como privada

No Windows, a rede deve estar configurada como **Privada**.

Passos:

1. Abrir **Configurações**
2. Ir em **Rede e Internet**
3. Selecionar **Wi-Fi** ou **Ethernet**
4. Clicar na rede atual
5. Selecionar **Perfil de rede: Privado**

Isso permite comunicação entre dispositivos da rede local.

---

# 6. Desativar ou configurar o Firewall

O protocolo TFTP utiliza **UDP na porta 69**.

O firewall do Windows pode bloquear essa comunicação.

## 6.1 Desativar temporariamente o firewall

Passos:

1. Abrir **Painel de Controle**
2. Ir em **Sistema e Segurança**
3. Abrir **Windows Defender Firewall**
4. Selecionar **Ativar ou desativar o Firewall**
5. Desativar para redes privadas

⚠️ Recomendado apenas para testes.

---

## 6.2 Alternativa: permitir Python no firewall

1. Abrir **Windows Defender Firewall**
2. Clicar em **Permitir um aplicativo pelo firewall**
3. Adicionar **Python**
4. Permitir em **Redes privadas**

---

# 7. Permissões da pasta `tftpboot`

O servidor utiliza a pasta `tftpboot` como diretório raiz para armazenar arquivos transferidos.

É necessário garantir que essa pasta tenha permissões de **leitura e escrita**.

## Criar a pasta

Se ela não existir:

```bash
mkdir tftpboot
```

## Permissões necessárias

A pasta precisa permitir:

- leitura
- escrita

No Windows:

1. Clique com botão direito na pasta `tftpboot`
2. Selecione **Propriedades**
3. Vá em **Segurança**
4. Garanta que seu usuário possui:
   - **Read**
   - **Write**

---

# 8. Executando o servidor

Caso os arquivos não estejam configurados

```bash
python config.py
```
Saída esperada:

```
Your Local IP Address is: 192.168.x.xxx
```

Abra um terminal na pasta do projeto e execute:

```bash
python tftp.py --server
```

Saída esperada:

```
Server on 0.0.0.0:69
Starting receive loop...
```

O servidor ficará aguardando conexões.

---

# 9. Executando o cliente

Em outro terminal:

```bash
python tftp.py --client
```

Menu exibido:

```
What do you want to do?

Download file
Upload file
Exit
```

---

# 10. Download de arquivos

Fluxo:

1. Selecionar **Download file**
2. Informar o nome do arquivo no servidor
3. Informar o nome do arquivo local que armazenará o conteúdo

Exemplo:

```
Remote filename: exemplo.txt
Local filename: exemplo_download.txt
```

---

# 11. Upload de arquivos

Fluxo:

1. Selecionar **Upload file**
2. Informar o nome do arquivo detro servidor
3. Informar o nome do arquivo local

Exemplo:

```
Remote filename: teste.txt
Enter local filename to upload: arquivo_cliente.txt
```

O arquivo será enviado para a pasta:

```
tftpboot/
```

no servidor.

---

# 12. Observações importantes

### O cliente e servidor devem estar na mesma rede

Caso contrário o TFTP não funcionará.

### Executar o servidor primeiro

O servidor precisa estar ativo antes do cliente iniciar a transferência.

### Porta 69

A porta 69 pode exigir permissões administrativas em alguns sistemas.

Caso ocorra erro, execute o terminal como **Administrador**.

---

# 13. Troubleshooting

## Arquivo transferido com 0 bytes

Verifique:

- caminho do arquivo
- permissões da pasta
- firewall
- se o cliente está na mesma rede do servidor

---

## Conexão não funciona

Verifique:

- IP do servidor no `.env`
- firewall
- rede privada
- conectividade entre máquinas

Teste com:

```bash
ping IP_DO_SERVIDOR
```

---

# 14. Encerrando o servidor

Para parar o servidor, pressione:

```
CTRL + C
```

no terminal.

---

# 15. Conclusão

Este projeto demonstra o funcionamento básico do **TFTP em Python**, permitindo transferências simples de arquivos em redes locais utilizando cliente e servidor.

O sistema depende principalmente de:

- configuração correta da rede
- permissões da pasta `tftpboot`
- firewall configurado corretamente
- cliente e servidor na mesma rede



# 16. Testes
-   Servidor inicializado
![Console Servidor](imagens\server_console.png)
-   Arquivo Enviado pelo cliente e recebido no servidor + arquivos presentes no servidor
![Arquivo Enviado para o servidor](imagens\servidor.png)
-   Lado do cliente enviando o arquivo e baixando um arquivo do servidor
![Console do Cliente](imagens\console_client.png)
- Arquivo que foi baixado do servidor
![Arquivo baixado do servidor](imagens\arquivo_client.png)

# 17. Diagrama C4 de componentes
![Diagrama C4 de componentes](imagens\C4_TFTP.png)
