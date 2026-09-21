// Server-side Supabase clients.
//
// `createServerClient` — reads the caller's session from cookies (Server Components,
//   Route Handlers acting on behalf of the signed-in user). Respects RLS.
//
// `createServiceRoleClient` — the service-role key, bypasses RLS. Only ever use this
//   for admin-style writes with no untrusted user input: the Stripe webhook flipping
//   `enrollments.status`, and the manifest importer writing to `lessons`. Never call
//   this from a path that takes a user_id from a request body/query string.

import { createServerClient as createSupabaseServerClient } from "@supabase/ssr";
import { createClient as createSupabaseClient } from "@supabase/supabase-js";
import { cookies } from "next/headers";

export function createServerClient() {
  const cookieStore = cookies();
  return createSupabaseServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return cookieStore.get(name)?.value;
        },
        // TODO(Pranav): implement set/remove once wiring real auth (magic link) flows —
        // stubbed out for now since no cookie-writing route exists yet.
      },
    }
  );
}

export function createServiceRoleClient() {
  return createSupabaseClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!,
    { auth: { persistSession: false } }
  );
}
