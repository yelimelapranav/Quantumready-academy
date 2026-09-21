import Stripe from "stripe";
import { NextResponse } from "next/server";

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

// POST /api/checkout — creates a Stripe Checkout session for course enrollment.
// TODO(Pranav): require a signed-in user (read from Supabase session) before creating
// the session, and pass their user id through as `client_reference_id` so the webhook
// below can attribute the resulting enrollment to the right person.
export async function POST() {
  const session = await stripe.checkout.sessions.create({
    mode: "payment",
    line_items: [{ price: process.env.STRIPE_PRICE_ID!, quantity: 1 }],
    success_url: `${process.env.NEXT_PUBLIC_SITE_URL}/academy?checkout=success`,
    cancel_url: `${process.env.NEXT_PUBLIC_SITE_URL}/academy?checkout=cancelled`,
    // client_reference_id: userId,  // TODO(Pranav): see above
  });

  return NextResponse.json({ url: session.url });
}
