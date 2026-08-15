const express = require("express");

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 10000;

// Zalo domain verification
app.get(/^\/zalo_verifier(.+)\.html$/, (req, res) => {
  const token = req.params[0];

  res
    .status(200)
    .type("html")
    .send(`zalo-platform-site-verification=${token}`);
});

// Trang chính
app.get("/", (req, res) => {
  res.status(200).send("Zalo Webhook is running!");
});

// Kiểm tra webhook
app.get("/webhook", (req, res) => {
  res.status(200).send("Webhook OK");
});

// Nhận webhook POST
app.post("/webhook", (req, res) => {
  console.log("Webhook received:", JSON.stringify(req.body));

  res.status(200).json({
    ok: true
  });
});

app.listen(PORT, "0.0.0.0", () => {
  console.log(`Server running on port ${PORT}`);
});
