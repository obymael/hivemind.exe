import express from "express";
import axios from "axios";
import dotenv from "dotenv";

dotenv.config();

const app = express();
app.use(express.json());

const APPEEARS_URL = "https://appeears.earthdatacloud.nasa.gov/api";

// Step A: Login and get token
async function getToken() {
  const resp = await axios.post(`${APPEEARS_URL}/login`, {}, {
    auth: {
      username: process.env.APPEEARS_USER,
      password: process.env.APPEEARS_PASS
    }
  });
  return resp.data.token;
}

app.get("/", (req, res) => {
  res.send("🚀 NASA Bloom Backend is running!");
});


// Test route to verify login works
app.get("/login-test", async (req, res) => {
  try {
    const token = await getToken();
    res.json({ success: true, token });
  } catch (err) {
    console.error(err.response?.data || err.message);
    res.status(500).json({ error: "Login failed" });
  }
});

app.listen(5000, () => console.log("Backend running at http://localhost:5000"));
