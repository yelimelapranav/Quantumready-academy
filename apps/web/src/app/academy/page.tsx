import { createServerClient } from "@/lib/supabase/server";
import type { Lesson } from "@/lib/types";
import ProgressBar from "@/components/ProgressBar";

// TODO(Pranav): gate this page — redirect signed-out or non-enrolled users to
// the checkout flow (see api/checkout/route.ts) instead of rendering the list.
export default async function AcademyPage() {
  const supabase = createServerClient();

  const { data: lessons, error } = await supabase
    .from("lessons")
    .select("*")
    .eq("published", true)
    .order("order_index", { ascending: true });

  if (error) {
    // TODO(Pranav): real error UI
    return <p>Could not load lessons: {error.message}</p>;
  }

  return (
    <main>
      <h1>Curious to Capable</h1>
      <ol>
        {(lessons as Lesson[] | null)?.map((lesson) => (
          <li key={lesson.id}>
            <a href={`/academy/${lesson.slug}`}>{lesson.title}</a>
            {/* TODO(Pranav): wire real per-user progress once auth exists */}
            <ProgressBar percent={0} />
          </li>
        ))}
      </ol>
    </main>
  );
}
