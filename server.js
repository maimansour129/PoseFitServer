const express = require("express");
const app = express();
const userRouter = require("./routes/userRoutes");
const workoutRouter=require("./routes/workoutRoutes");
const bodyParser = require("body-parser");
const cookieParser = require("cookie-parser");
const mongoose = require("mongoose");


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

// routes
app.use("/api/user", userRouter);
app.use("/api/workout", workoutRouter);


