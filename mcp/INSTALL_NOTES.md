# Notas de Instalação e Ambiente

Este arquivo documenta as ações que foram necessárias para executar o projeto e resolver o erro "npx not found".

## Resumo
- Arquivo principal: `mcp_cli.py` (local: raiz do projeto `C:\Users\Kaio\Documents\MCP\mcp_cli.py`).
- Ambiente virtual Python usado: pasta `dotenv` (activate: `dotenv\Scripts\activate`).
- Foi necessário instalar Node.js (npm/npx) e ajustar o PATH do Windows para que o comando `mcp` encontrasse `npx`.

## O que houve
O comando `mcp dev mcp_cli.py` devolvia o erro:

```
ERROR    npx not found. Please ensure Node.js and npm are properly installed and added to your system PATH.
```

Motivo: o Node.js estava instalado em `C:\Program Files\nodejs\`, mas essa pasta não estava incluída no `PATH` da sessão do PowerShell que foi usada para rodar o comando.

## Versões observadas no diagnóstico
- node: v25.2.1
- npm: 11.6.2
- npx: 11.6.2

(essas versões foram obtidas ao adicionar temporariamente `C:\Program Files\nodejs\` ao `PATH` da sessão.)

## Passos que eu executei / que você deve seguir
1. Ative o ambiente Python (se aplicável):

```powershell
dotenv\Scripts\activate
```

2. Verificar versões/estado atual:

```powershell
node -v
npm -v
npx -v
```

3. Solução temporária (válida apenas para a sessão atual do PowerShell):

```powershell
$env:PATH = "$env:PATH;C:\Program Files\nodejs\"
node -v
npx -v
mcp dev mcp_cli.py
```

4. Tornar a mudança permanente (opção recomendada):

- Usando PowerShell (adiciona ao PATH do usuário):

```powershell
$userPath = [Environment]::GetEnvironmentVariable('Path','User')
if ($userPath -notlike '*C:\Program Files\nodejs*') {
  [Environment]::SetEnvironmentVariable('Path', $userPath + ';C:\Program Files\nodejs', 'User')
  Write-Host 'Adicionado ao PATH do usuário. Feche e reabra o PowerShell para aplicar.'
} else {
  Write-Host 'C:\\Program Files\\nodejs já está no PATH do usuário.'
}
```

- Ou via GUI: Painel de Controle → Sistema → Configurações Avançadas do Sistema → Variáveis de Ambiente → editar `Path` nas Variáveis do Usuário e adicionar `C:\Program Files\nodejs`.

5. Após reiniciar o PowerShell, confirme que `node`, `npm` e `npx` funcionam e reexecute o comando do projeto:

```powershell
node -v
npm -v
npx -v
mcp dev mcp_cli.py
```

## Instalar o `uv` e por que é necessário

O erro `Error: spawn uv ENOENT` indica que o sistema tentou executar um comando chamado `uv` e não o encontrou no `PATH` — ou seja, o executável não estava instalado ou acessível. O projeto `mcp` (e sua documentação) recomenda o uso da ferramenta `uv` para gerenciar e executar projetos Python com dependências e processos auxiliares.

Por que instalar `uv` neste caso:
- `mcp` pode delegar a execução de servidores e scripts para o comando `uv` (ex.: `uv run --with mcp ...`).
- Se `uv` não estiver disponível, chamadas como `uv run --with mcp mcp run mcp_cli.py` falham com ENOENT, impedindo que o servidor/CLI inicie corretamente.

Como instalar `uv` no ambiente usado pelo projeto:

```powershell
# Ative o virtualenv (se aplicável)
dotenv\Scripts\activate

# Instalar com pip dentro do venv (recomendado para projetos isolados)
pip install uv

# Alternativa: instalar globalmente via pipx (isola o binário)
pipx install uv
```

Verifique a instalação:

```powershell
uv --version
Get-Command uv -ErrorAction SilentlyContinue | Format-List *
```

Depois de instalar `uv`, reexecute o comando que falhou originalmente (ou execute explicitamente):

```powershell
uv run --with mcp mcp run mcp_cli.py
# ou
mcp dev mcp_cli.py
```

Instalar `uv` é o passo que resolveu o erro `spawn uv ENOENT` durante o diagnóstico.

## Observações e dicas
- Se você preferir gerenciar múltiplas versões do Node no Windows, considere instalar `nvm-windows` (https://github.com/coreybutler/nvm-windows). Ele altera a forma como o Node é exposto no PATH.
- Se `npm` existir mas `npx` não, é possível instalar `npx` globalmente com:

```powershell
npm install -g npx
```

- Mantive o foco nas correções mínimas: garantir que `npx` esteja disponível para que o `mcp` consiga executar ferramentas JavaScript que dependem dele.

## Onde o código está
- `C:\Users\Kaio\Documents\MCP\mcp_cli.py` — ponto de entrada que você chamou com `mcp dev`.

---
Arquivo gerado automaticamente para documentar as ações realizadas em 10/12/2025.
