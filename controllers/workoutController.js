const mongoose = require("mongoose");
const workout = require("../models/workout");

const searchForWorkout = async (req, res) => {
  console.log("hiiiiii");
  workout
    .find({ workoutName: { $regex: req.body.name, $options: "i" } })
    .select({ workoutName: 1, gif: 1 })
    .then((result) => res.send(result))
    .catch((error) => console.log(error));
};
const getAllWorkouts = async (req, res) => {
  workout
    .find()
    .then((result) => res.send(result))
    .catch((error) => console.log(error));
};

module.exports = {
  searchForWorkout,
  getAllWorkouts,
};
