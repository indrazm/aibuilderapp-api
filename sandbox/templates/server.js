const server = Bun.serve({
  port: {PORT},
  async fetch(req) {
    const url = new URL(req.url);
    const path = url.pathname;

    // Serve index.html for root path
    if (path === "/") {
      try {
        return new Response(Bun.file("index.html"), {
          headers: {
            "Content-Type": "text/html",
          },
        });
      } catch (error) {
        return new Response("index.html not found", { status: 404 });
      }
    }

    // Serve static files
    try {
      const filePath = path.slice(1); // Remove leading slash
      const file = Bun.file(filePath);

      // Check if file exists
      if (await file.exists()) {
        const contentType = getContentType(filePath);
        return new Response(file, {
          headers: {
            "Content-Type": contentType,
          },
        });
      }
    } catch (error) {
      // File doesn't exist, continue to 404
    }

    return new Response("Not Found", { status: 404 });
  },
});

function getContentType(filePath) {
  const ext = filePath.split(".").pop()?.toLowerCase();
  switch (ext) {
    case "html":
      return "text/html";
    case "css":
      return "text/css";
    case "js":
      return "application/javascript";
    case "json":
      return "application/json";
    case "png":
      return "image/png";
    case "jpg":
    case "jpeg":
      return "image/jpeg";
    case "gif":
      return "image/gif";
    case "svg":
      return "image/svg+xml";
    default:
      return "text/plain";
  }
}

console.log(`Server running at http://localhost:${server.port}`);
