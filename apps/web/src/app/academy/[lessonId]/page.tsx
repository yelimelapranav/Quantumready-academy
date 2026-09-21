import { createServerClient } from "@/lib/supabase/server";
import type { Lesson } from "@/lib/types";
import VideoPlayer from "@/components/VideoPlayer";
import { notFound } from "next/navigation";

// Note: [lessonId] here is actually matched against `lessons.slug`, not a uuid —
// keeps URLs readable (/academy/lesson-02-bits-vs-qubits). Rename the folder to
// [lessonSlug] if that's confusing — purely cosmetic, doesn't affect the query below.
export default async function LessonPage({ params }: { params: { lessonId: string } }) {
  const supabase = createServerClient();

  const { data: lesson } = await supabase
    .from("lessons")
    .select("*")
    .eq("slug", params.lessonId)
    .eq("published", true)
    .single();

  if (!lesson) notFound();

  const l = lesson as Lesson;

  return (
    <main>
      <h1>{l.title}</h1>
      {l.cloudflare_video_id ? (
        <VideoPlayer cloudflareVideoId={l.cloudflare_video_id} />
      ) : (
        <p>Video not yet rendered for this lesson.</p>
      )}

      {/* TODO(Pranav): quiz UI reading l.quiz, submitting to lesson_progress.quiz_score */}
      {/* TODO(Pranav): "mark watched" button writing lesson_progress via the browser client */}
    </main>
  );
}
