// server.js - Backend Node.js + Express para Render.com
const express = require('express');
const axios = require('axios');
const app = express();

app.use(express.json());

// CONFIGURAÇÕES - SUBSTITUA COM SEUS DADOS
const WEBHOOK_SECRET = '66906f52e82893871708630b373c6046fbd4de7a'; // Mesma que salvou no GestãoPro
const BASE44_API_URL = 'https://app-gestaopro.base44.app'; // URL da API Base44
const BASE44_API_KEY = '94152a0f65cf4aa5b1353066c6db6696'; // Gere em Dashboard → Settings → API → Chaves de API

// Endpoint que recebe webhooks da Braip
app.post('/webhook/braip', async (req, res) => {
  try {
    console.log('📥 Webhook recebido:', req.body);
    
    // 1. VALIDAR CHAVE ÚNICA (Segurança)
    const secret = req.headers['x-webhook-secret'] || req.body.webhook_secret;
    if (secret !== WEBHOOK_SECRET) {
      console.log('❌ Chave inválida');
      return res.status(401).json({ error: 'Unauthorized' });
    }
    
    // 2. EXTRAIR DADOS DA BRAIP
    const {
      trans_id,           // ID da transação
      trans_status,       // Status: 2=aprovado, 3=cancelado, 5=reembolsado
      trans_value,        // Valor
      client_name,        // Nome do cliente
      client_email,       // Email
      subs_key,           // Chave de assinatura (se for recorrente)
      product_name,       // Nome do produto
      // ... outros campos que a Braip envia
    } = req.body;
    
    // 3. DETERMINAR TIPO DE EVENTO
    let eventType = 'manual';
    let status = 'pendente';
    
    if (trans_status === 2) {
      eventType = 'payment.approved';
      status = 'aprovado';
    } else if (trans_status === 3) {
      eventType = 'subscription.canceled';
      status = 'cancelado';
    } else if (trans_status === 5) {
      eventType = 'payment.refunded';
      status = 'reembolsado';
    }
    
    if (subs_key) {
      eventType = 'subscription.created';
    }
    
    // 4. CALCULAR MÊS DE REFERÊNCIA
    const hoje = new Date();
    const mes = String(hoje.getMonth() + 1).padStart(2, '0');
    const ano = hoje.getFullYear();
    const mesReferencia = `${mes}/${ano}`;
    const dataVencimento = `${ano}-${mes}-01`;
    
    // 5. CRIAR PAGAMENTO NO BASE44
    const pagamentoData = {
      empresa_id: client_email, // Ou use ID do cliente
      empresa_nome: client_name,
      valor: parseFloat(trans_value),
      mes_referencia: mesReferencia,
      data_vencimento: dataVencimento,
      data_pagamento: hoje.toISOString().split('T')[0],
      status: status,
      braip_transaction_id: trans_id,
      braip_event_type: eventType,
      is_subscription: !!subs_key,
      forma_pagamento: 'braip',
      observacoes: `Produto: ${product_name || 'N/A'}`
    };
    
    // 6. ENVIAR PARA BASE44 VIA API
    const response = await axios.post(
      `${BASE44_API_URL}/entities/Pagamento`,
      pagamentoData,
      {
        headers: {
          'Authorization': `Bearer ${BASE44_API_KEY}`,
          'Content-Type': 'application/json'
        }
      }
    );
    
    console.log('✅ Pagamento criado:', response.data);
    
    // 7. RESPONDER À BRAIP
    return res.status(200).json({ 
      success: true, 
      message: 'Webhook processado com sucesso',
      pagamento_id: response.data.id 
    });
    
  } catch (error) {
    console.error('❌ Erro ao processar webhook:', error.response ? error.response.data : error.message);
    return res.status(500).json({ 
      error: 'Internal server error',
      details: error.response ? error.response.data : error.message
    });
  }
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Iniciar servidor
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`🚀 Servidor rodando na porta ${PORT}`);
  console.log(`📡 Webhook endpoint: http://localhost:${PORT}/webhook/braip`);
});
