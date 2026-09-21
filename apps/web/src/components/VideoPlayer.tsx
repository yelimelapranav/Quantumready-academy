// Thin wrapper around Cloudflare Stream's iframe embed.
// Docs: https://developers.cloudflare.com/stream/viewing-videos/using-the-player-api/

export default function VideoPlayer({ cloudflareVideoId }: { cloudflareVideoId: string }) {
  const accountId = process.env.CLOUDFLARE_ACCOUNT_ID;

  return (
    <div style={{ position: "relative", paddingTop: "56.25%" }}>
      <iframe
        src={`https://customer-${accountId}.cloudflarestream.com/${cloudflareVideoId}/iframe`}
        style={{ border: "none", position: "absolute", top: 0, left: 0, height: "100%", width: "100%" }}
        allow="accelerometer; gyroscope; autoplay; encrypted-media; picture-in-picture;"
        allowFullScreen
      />
    </div>
  );
}
