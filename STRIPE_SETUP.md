# Ligar a Stripe (passo a passo)

O código da app já está pronto. Falta configurar as contas. Usa primeiro o **modo de teste** da Stripe.

## 1. Segurança do Supabase (importante, fazer antes de tudo)

No SQL Editor do Supabase corre:

```sql
alter table profiles add column if not exists stripe_customer_id text;

-- Lista as políticas atuais da tabela profiles
select policyname, cmd from pg_policies where tablename = 'profiles';
```

Confirma que **não existe** uma política de `UPDATE` (ou `ALL`) para utilizadores normais. Se existir, qualquer pessoa podia mudar o próprio plano para `admin` pelo browser. Apaga-a com:

```sql
drop policy "NOME_DA_POLITICA" on profiles;
```

Deve ficar só `SELECT` (e `INSERT` do próprio registo). O plano só é alterado pelo webhook (usa a chave service_role, que ignora o RLS) ou por ti no Table Editor.

## 2. Stripe: produtos e links de pagamento

1. Cria conta em stripe.com e fica no **modo de teste**.
2. Product catalog: cria "Freenomics Premium" com dois preços recorrentes: 4,99 EUR/mês e 39,99 EUR/ano.
3. Payment Links: cria um link para cada preço. Em "After payment" aponta para o URL da tua app.
4. Copia os dois URLs (`https://buy.stripe.com/...`).

## 3. Secrets da app

Em `.streamlit/secrets.toml` (local) **e** em Streamlit Cloud, Settings, Secrets:

```toml
STRIPE_LINK_MONTHLY = "https://buy.stripe.com/..."
STRIPE_LINK_YEARLY = "https://buy.stripe.com/..."
```

## 4. Webhook (atualiza o plano automaticamente)

Com o Supabase CLI (`brew install supabase/tap/supabase`):

```bash
cd /Users/bernardolemos/Desktop/freenomics
supabase login
supabase link --project-ref aaxvuocptemqxiuzryez
supabase functions deploy stripe-webhook --no-verify-jwt
```

Depois, na Stripe: Developers, Webhooks, Add endpoint:

- URL: `https://aaxvuocptemqxiuzryez.supabase.co/functions/v1/stripe-webhook`
- Eventos: `checkout.session.completed` e `customer.subscription.deleted`

Copia o "Signing secret" (`whsec_...`) e define os segredos da função (as chaves ficam só no Supabase, nunca no GitHub):

```bash
supabase secrets set STRIPE_SECRET_KEY=sk_test_... STRIPE_WEBHOOK_SECRET=whsec_...
```

(`SUPABASE_URL` e `SUPABASE_SERVICE_ROLE_KEY` já existem por defeito nas funções.)

## 5. Testar

Na app: cria conta, vai a Preços, subscreve com o cartão de teste `4242 4242 4242 4242`. Em até 1 minuto o plano passa a Premium. Quando tudo funcionar, repete com o modo real da Stripe (novos links e novas chaves).

## 6. Antes de cobrar a sério

- Preenche os teus dados e contacto em `pages/15_Legal.py`.
- Configura na Stripe o portal de cliente (para cancelamentos) e os dados fiscais/IVA.
- Pede a revisão dos Termos e da Privacidade a um profissional.
