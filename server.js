const express = require("express");

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 10000;

// File xác thực domain Zalo
app.get(
  "/zalo_verifierH8Ao4CU77paTguim-Pa52GYzrpRaomrkCpCq.html",
  (req, res) => {
    res
      .type("html")
      .send(
        "zalo-platform-site-verification=H8Ao4CU77paTguim-Pa52GYzrpRaomrkCpCq"
      );
  }
);

// Trang chính
app.get("/", (req, res) => {
  res.status(200).send("Zalo Webhook is running!");
});

// Webhook kiểm tra GET
app.get("/webhook", (req, res) => {
  res.status(200).send("Webhook OK");
});

// Webhook nhận POST
app.post("/webhook", (req, res) => {
  console.log("Webhook received:", JSON.stringify(req.body));

  res.status(200).json({
    ok: true
  });
});

app.listen(PORT, "0.0.0.0", () => {
  console.log(`Server running on port ${PORT}`);
});
