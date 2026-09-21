// Hand-written types mirroring supabase/migrations/0001_init.sql.
// TODO(Pranav): once the schema stabilizes, swap this for generated types via
// `supabase gen types typescript` and drop the hand-maintained version.

export type QuizQuestion = {
  question: string;
  choices: string[];
  answer_index: number;
};

export type Lesson = {
  id: string;
  slug: string;
  order_index: number;
  title: string;
  cloudflare_video_id: string | null;
  duration_seconds: number | null;
  transcript: string | null;
  quiz: QuizQuestion[] | null;
  published: boolean;
};

export type EnrollmentStatus = "pending" | "active" | "refunded" | "cancelled";

export type Enrollment = {
  id: string;
  user_id: string;
  stripe_checkout_session_id: string | null;
  status: EnrollmentStatus;
  enrolled_at: string | null;
};

export type LessonProgress = {
  user_id: string;
  lesson_id: string;
  watched: boolean;
  quiz_score: number | null;
  completed_at: string | null;
};
