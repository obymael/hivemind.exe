import express from "express";
import axios from "axios";
import dotenv from "dotenv";

dotenv.config();

const app = express();
app.use(express.json());



app.get("/", (req, res) => {
  res.send("🚀 NASA Bloom Backend is running!");
});



app.listen(5000, () => console.log("Backend running at http://localhost:5000"));
