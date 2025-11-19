# Configuração do Chat IA com OpenAI

O sistema TalentMatch inclui um assistente de carreira inteligente powered by OpenAI GPT-4o-mini. Para ativar esta funcionalidade, você precisa configurar uma chave de API do OpenAI.

## 📋 Pré-requisitos

1. Ter uma conta no OpenAI (https://platform.openai.com)
2. Ter créditos disponíveis na sua conta OpenAI

## 🔑 Como Obter a API Key

1. Acesse https://platform.openai.com/api-keys
2. Faça login na sua conta OpenAI
3. Clique em "Create new secret key"
4. Dê um nome para a chave (ex: "TalentMatch")
5. Copie a chave gerada (ela começa com `sk-...`)
6. **IMPORTANTE**: Guarde a chave em local seguro! Ela só será mostrada uma vez

## ⚙️ Como Configurar no Replit

### Opção 1: Via Interface do Replit (Recomendado)

1. No Replit, clique em "Tools" no menu lateral esquerdo
2. Clique em "Secrets"
3. Clique no botão "New Secret"
4. Em "Key", digite: `OPENAI_API_KEY`
5. Em "Value", cole sua chave da OpenAI (ex: `sk-proj-...`)
6. Clique em "Add Secret"
7. Reinicie o servidor Django

### Opção 2: Via Código (Desenvolvimento Local)

Se você está rodando localmente (não no Replit), crie um arquivo `.env` na raiz do projeto:

```env
OPENAI_API_KEY=sk-proj-sua-chave-aqui
```

E instale python-dotenv:

```bash
pip install python-dotenv
```

Em `talentmatch_project/settings.py`, adicione no topo:

```python
from dotenv import load_dotenv
load_dotenv()
```

## ✅ Verificar se Está Funcionando

1. Após configurar a chave, reinicie o servidor Django
2. Faça login como candidato no sistema
3. Vá para a página "Assistente IA" no menu lateral
4. Envie uma mensagem de teste (ex: "Olá!")
5. Se tudo estiver correto, você receberá uma resposta do assistente IA

## ⚠️ Importante - Custos

- O modelo GPT-4o-mini é econômico, mas tem custo por uso
- Monitore seu uso em https://platform.openai.com/usage
- Configure limites de gastos na sua conta OpenAI se desejar
- Custo aproximado: $0.15 por 1M de tokens de entrada, $0.60 por 1M de tokens de saída

## 🤖 Funcionalidades do Assistente IA

O assistente pode ajudar com:

- ✅ Orientação de carreira personalizada
- ✅ Dicas para entrevistas
- ✅ Sugestões de habilidades para desenvolver
- ✅ Análise de compatibilidade com vagas
- ✅ Conselhos sobre currículo e perfil profissional

## 🔒 Segurança

- **NUNCA** compartilhe sua API key publicamente
- **NUNCA** faça commit da API key no Git
- Use sempre variáveis de ambiente ou Secrets do Replit
- Revogue chaves comprometidas imediatamente em https://platform.openai.com/api-keys

## 🐛 Troubleshooting

### Erro: "API key não configurada"

**Solução**: Certifique-se de que adicionou o secret `OPENAI_API_KEY` corretamente no Replit e reiniciou o servidor.

### Erro: "Incorrect API key provided"

**Solução**: Verifique se copiou a chave correta e completa da OpenAI. A chave deve começar com `sk-`.

### Erro: "You exceeded your current quota"

**Solução**: Sua conta OpenAI não tem créditos suficientes. Adicione créditos em https://platform.openai.com/settings/organization/billing

### Chat não responde / demora muito

**Solução**: Verifique sua conexão com a internet e o status da API da OpenAI em https://status.openai.com

## 📚 Documentação Adicional

- OpenAI API Documentation: https://platform.openai.com/docs
- OpenAI Pricing: https://openai.com/pricing
- OpenAI Community: https://community.openai.com

---

**Nota**: O Chat IA é opcional. O sistema TalentMatch funciona normalmente sem ele, apenas esta funcionalidade específica ficará indisponível.
