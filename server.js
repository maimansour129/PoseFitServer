const express = require("express");
const app = express();
const userRouter = require("./routes/userRoutes");
const workoutRouter = require("./routes/workoutRoutes");
const {requireAuth, checkUser} = require("./middleware/authMiddleware")
const bodyParser = require("body-parser");
const cookieParser = require("cookie-parser");
const mongoose = require("mongoose");
const axios = require("axios");
const authRouter = require("./routes/authRoutes");

const dbURI =
  "mongodb+srv://PoseFit:PoseFit@cluster.y1yvcw2.mongodb.net/PoseFit?retryWrites=true&w=majority";
mongoose
  .connect(dbURI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(app.listen(3000))
  .then(console.log("Connected to mongodb, Listening on port 3000"))
  .catch((err) => console.log(err));

// Middleware
app.use(express.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cookieParser());
app.use((req, res, next) => {
  console.log(req.path, req.method);
  next();
});

// routes
app.use("*", checkUser);
app.use("/api/user", userRouter);
app.use("/api/workout", requireAuth, workoutRouter);
app.use(authRouter);

app.post("/model", (req, res) => {
  console.log("hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii  "+req.body.image)
  const imageFile = req.body;
  const imageStr = Buffer.from(imageFile.image).toString("base64");
  

  axios
    .post("http://127.0.0.1:5000/bicepCurl", imageStr, {
      headers: { "Content-Type": "application/json; charset=UTF-8" },
    })
    .then((response) => res.json(response.data))
    .catch((err) => res.send(err));
  console.log(res.body);
});
