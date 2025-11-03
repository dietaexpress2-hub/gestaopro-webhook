# GestãoPro

Uma plataforma web completa para gerenciar o dia a dia da sua empresa — clientes, vendas, cobranças, estoque, documentos, relatórios e suporte — com uma interface moderna, responsiva e focada em produtividade.

> GestãoPro foi pensado para pequenos e médios empreendimentos que precisam centralizar operações administrativas de forma simples e eficiente.

## Principais recursos

- Painel administrativo intuitivo com tema claro/escuro
- Gestão completa de clientes, cobranças e parcelas
- Emissão e controle de documentos fiscais e recibos
- Controle de estoque e cadastro de produtos
- Relatórios consolidados e exportáveis (há script de geração de relatório em `scripts/`)
- Integrações com serviços externos via adaptadores em `src/api/`
- Sistema de suporte e documentação integrada

## Tecnologias

- Frontend: React + Vite
- Estilização: Tailwind CSS
- Scripts auxiliares: Node.js / Python (scripts de relatório)
- Containerização: Docker (opcional)

## Teste rápido (desenvolvimento)

Abra um terminal (PowerShell no Windows) e execute:

```powershell
npm install
npm run dev
```

Depois abra http://localhost:5173 no navegador.

## Build para produção

```powershell
npm run build
npm run preview
```

O comando `preview` serve para testar o build localmente.

## Docker (exemplo rápido)

Crie a imagem e execute (exemplo genérico):

```powershell
docker build -t gestao-pro .
docker run -p 3000:3000 gestao-pro
```

Ajuste portas e variáveis conforme seu ambiente.

## Scripts úteis

- `scripts/gera_relatorio.py` — normaliza e gera relatórios consolidados (HTML)
- `scripts/generate-html-report.js` — utilitário JS para relatórios

## Estrutura importante do projeto

- `src/` — código da aplicação
	- `src/pages/` — páginas (ex.: `Layout.jsx`, `Login.jsx`)
	- `src/components/` — componentes reutilizáveis (cards, formulários, dialogs)
	- `src/api/` — clientes e integrações (ex.: `integrations.js`)
- `scripts/` — scripts auxiliares (relatórios, geração de dados)
- `Dockerfile` — exemplo de containerização
- `package.json` — comandos e dependências

Exemplos de arquivos úteis:

- Layout: `src/pages/Layout.jsx`
- Login: `src/pages/Login.jsx`
- Política de privacidade e termos: `src/components/auth/`
- Geração de relatórios: `scripts/gera_relatorio.py`

## Como contribuir

1. Abra uma issue descrevendo a proposta ou bug.
2. Crie um branch com um nome descritivo (ex.: `feat/relatorio-html`).
3. Faça PRs pequenas e com escopo claro.
4. Siga as regras de lint do projeto e escreva descrições claras.

Se quiser, posso ajudar a criar templates de PR e ISSUE.

## Licença

Adicione aqui a sua licença (ex.: MIT) ou a política de uso interna da empresa.

## Contato

Para dúvidas, integração ou suporte, utilize os canais internos da empresa ou abra uma issue no repositório.

---

Obrigado por contribuir com o GestãoPro — vamos tornar a gestão do seu negócio mais simples e eficiente!

# Base44 App


This app was created automatically by Base44.
It's a Vite+React app that communicates with the Base44 API.

## Running the app

```bash
npm install
npm run dev
```

## Building the app

```bash
npm run build
```

For more information and support, please contact Base44 support at app@base44.com.
