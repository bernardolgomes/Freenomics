// Supabase Edge Function: recebe eventos da Stripe e atualiza o plano em profiles.
// Deploy: ver STRIPE_SETUP.md na raiz do projeto.
import Stripe from "https://esm.sh/stripe@14?target=denonext";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const stripe = new Stripe(Deno.env.get("STRIPE_SECRET_KEY")!, { apiVersion: "2024-06-20" });
const cryptoProvider = Stripe.createSubtleCryptoProvider();
const supabase = createClient(
  Deno.env.get("SUPABASE_URL")!,
  Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!, // só existe no servidor, nunca no repositório
);

Deno.serve(async (req) => {
  const signature = req.headers.get("Stripe-Signature");
  const body = await req.text();
  let event;
  try {
    event = await stripe.webhooks.constructEventAsync(
      body,
      signature!,
      Deno.env.get("STRIPE_WEBHOOK_SECRET")!,
      undefined,
      cryptoProvider,
    );
  } catch (err) {
    return new Response(`Webhook error: ${err.message}`, { status: 400 });
  }

  if (event.type === "checkout.session.completed") {
    const s = event.data.object;
    const userId = s.client_reference_id;
    if (userId) {
      await supabase
        .from("profiles")
        .update({ plan: "premium", stripe_customer_id: s.customer })
        .eq("id", userId)
        .neq("plan", "admin");
    }
  }

  if (event.type === "customer.subscription.deleted") {
    const sub = event.data.object;
    await supabase
      .from("profiles")
      .update({ plan: "free" })
      .eq("stripe_customer_id", sub.customer)
      .neq("plan", "admin");
  }

  return new Response(JSON.stringify({ received: true }), {
    headers: { "Content-Type": "application/json" },
  });
});
