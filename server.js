const express = require("express");

const app = express();
app.use(express.json());
app.get("/zalo_verifierH8Ao4CU77paTguim-Pa52GYzrpRaomrkCpCq.html", (req, res) => {
  res.type("html").send(
    "zalo-platform-site-verification=H8Ao4CU77paTguim-Pa52GYzrpRaomrkCpCq"
  );
});

app.get("/", (req, res) => {
  res.status(200).send("Zalo Webhook is running!");
});

app.get("/webhook", (req, res) => {
  res.status(200).send("Webhook OK");
});

app.post("/webhook", (req, res) => {
  console.log("Webhook received:", JSON.stringify(req.body, null, 2));

  // Trả lời mẫu để kiểm tra webhook.
  // Phần gửi tin nhắn thật qua Zalo OA API sẽ cấu hình ở bước tiếp theo.
  res.status(200).json({
    ok: true,
    message: "[AutoJoin Của Kainel]\\n\\n❌ Không Thể Join (Mã 227)\\n\\n🌅 Join Ngày Nay: 117/117"
  });
});

const PORT = process.env.PORT || 10000;
app.listen(PORT, "0.0.0.0", () => {
  console.log(`Server running on port ${PORT}`);
});
