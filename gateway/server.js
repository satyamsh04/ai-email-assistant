const http = require("http");

const port = Number(process.env.PORT || 3001);
const mlBaseUrl = process.env.ML_SERVICE_URL || "http://127.0.0.1:8000";

const server = http.createServer(async (request, response) => {
  response.setHeader("Access-Control-Allow-Origin", "https://localhost:3000");
  response.setHeader("Access-Control-Allow-Headers", "content-type");
  response.setHeader("Access-Control-Allow-Methods", "GET,POST,OPTIONS");

  if (request.method === "OPTIONS") {
    response.writeHead(204);
    response.end();
    return;
  }

  if (!request.url.startsWith("/api/ml/")) {
    sendJson(response, 404, { error: "Not found" });
    return;
  }

  const targetPath = request.url.replace(/^\/api\/ml/, "");
  try {
    const body = await readBody(request);
    const upstream = await fetch(`${mlBaseUrl}${targetPath}`, {
      method: request.method,
      headers: { "content-type": request.headers["content-type"] || "application/json" },
      body: request.method === "GET" ? undefined : body,
    });
    response.writeHead(upstream.status, {
      "content-type": upstream.headers.get("content-type") || "application/json",
    });
    response.end(Buffer.from(await upstream.arrayBuffer()));
  } catch (error) {
    sendJson(response, 502, { error: "ML service unavailable", detail: error.message });
  }
});

function readBody(request) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    request.on("data", chunk => chunks.push(chunk));
    request.on("end", () => resolve(Buffer.concat(chunks)));
    request.on("error", reject);
  });
}

function sendJson(response, status, payload) {
  response.writeHead(status, { "content-type": "application/json" });
  response.end(JSON.stringify(payload));
}

server.listen(port, "127.0.0.1", () => {
  console.log(`ML bridge listening on http://127.0.0.1:${port}`);
});
