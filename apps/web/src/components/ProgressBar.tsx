export default function ProgressBar({ percent }: { percent: number }) {
  return (
    <div style={{ background: "#eee", height: 6, borderRadius: 3 }}>
      <div
        style={{
          width: `${Math.min(100, Math.max(0, percent))}%`,
          background: "#5b5bd6",
          height: "100%",
          borderRadius: 3,
        }}
      />
    </div>
  );
}
