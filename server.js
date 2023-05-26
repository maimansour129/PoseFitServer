const express = require("express");
const app = express();
const userRouter = require("./routes/userRoutes");
const workoutRouter = require("./routes/workoutRoutes");

const {requireAuth, checkUser} = require("./middleware/authMiddleware")
const bodyParser = require("body-parser");
const cookieParser = require("cookie-parser");
const mongoose = require("mongoose");
const authRouter = require("./routes/authRoutes");
const modelRouter=require("./routes/modelRoutes");

const dbURI =
  "mongodb+srv://PoseFit:PoseFit@cluster.y1yvcw2.mongodb.net/PoseFit?retryWrites=true&w=majority";
mongoose
  .connect(dbURI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(app.listen(3000))
  .catch((err) => console.log(err));

// Middleware
app.use(bodyParser.json({ limit: "50mb" }));
app.use(express.json());
//app.use(cookieParser());

// app.use((req, res, next) => {
//   console.log(req.path, req.method);
//   next();
// });

// routes
//app.use("*", checkUser);
app.use("/api/workout", workoutRouter);
app.use("/api/user", userRouter);
app.use("/api/workout", workoutRouter);
app.use("/api/model", modelRouter);
app.use("/api/auth",authRouter);

