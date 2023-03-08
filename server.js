const express = require("express");
const app = express();
const userRouter = require("./routes/userRoutes");
const bodyParser = require("body-parser");
const cookieParser = require("cookie-parser");
const mongoose = require("mongoose");
const { spawn } = require("child_process");
const Workout = require("./models/workout");
const Plan = require("./models/Plan");

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

app.post("/addWorkout", (req, res) => {
  const workout = new Workout({
    workoutName: req.body.workoutName,
  });
  workout
    .save()
    .then((result) => {
      res.send(true);
    })
    .catch((err) => {
      console.log(err);
    });
});
app.post("/create", (req, res) => {
   const plan = new Plan({
      planName:req.body.name,
      workouts: req.body.workoutName,
   });

   plan
     .save()
     .then((result) => {
       res.send(true);
     })
     .catch((err) => {
       console.log(err);
     });
 });
 
 app.get("/workout", (req, res) => {
  Plan.find({ "workouts.rep": 15 }).populate('workout').then(result=>{
     res.send(result)
  }).catch(err=>{
     res.send(err);
  })
});


