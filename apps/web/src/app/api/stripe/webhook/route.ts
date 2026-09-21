import Stripe from "stripe";
import { NextRequest, NextResponse } from "next/server";
import { createServiceRoleClient } from "@/lib/supabase/server";

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

// POST /api/stripe/webhook — Stripe calls this on checkout events.
// Configure the endpoint URL + this exact secret in the Stripe dashboard once deployed.
//
// TODO(Pranav): this currently only handles `checkout.session.completed`. Decide whether
// `charge.refunded` should flip enrollments.status back to 'refunded' (schema already
// supports it) before launch.
export async function POST(req: NextRequest) {
  const body = await req.text();
  const signature = req.headers.get("stripe-signature")!;

  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(body, signature, process.env.STRIPE_WEBHOOK_SECRET!);
  } catch (err) {
    return NextResponse.json({ error: `Webhook signature verification failed` }, { status: 400 });
  }

  if (event.type === "checkout.session.completed") {
    const session = event.data.object as Stripe.Checkout.Session;
    const userId = session.client_reference_id;

    if (!userId) {
      // TODO(Pranav): once /api/checkout passes client_reference_id, this branch
      // should no longer be reachable — treat it as a bug, not a silent skip, once wired.
      return NextResponse.json({ received: true, warning: "no client_reference_id on session" });
    }

    const supabase = createServiceRoleClient();
    await supabase.from("enrollments").upsert({
      user_id: userId,
      stripe_checkout_session_id: session.id,
      status: "active",
      enrolled_at: new Date().toISOString(),
    });
  }

  return NextResponse.json({ received: true });
}
