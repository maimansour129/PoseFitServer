const jwt = require("jsonwebtoken");
const [User] = require("../models/user");
const dailyChallenge = require("../models/dailyChallenge");
const cron = require('node-cron');
const Plan = require("../models/Plan");
const mongoose = require("mongoose");
const Rank=require("../models/rankingBoard");
const _ = require("lodash");


function getUserToken(token) {
  const decodedToken = jwt.verify(token, "my private key");
  return decodedToken;
}

const updateUser = async (req, res) => {
  console.log("updating user");

  const updatedData = req.body;
  console.log(updatedData);
  let user;

  const decodedToken = getUserToken(req.cookies.jwt);
  //console.log(decodedToken);
  user = await User.findOneAndUpdate({ _id: decodedToken.id }, updatedData, {
    new: true,
  });
  console.log(user);

  res.status(200).send(user);
};

const getPlan = async (req, res) => {
  console.log("teeeeeeeeeest " + req.body.email);
  User.find({ email: req.body.email })
    .select({ email: 1, _id: 0 })
    .populate({
      path: "plan",
      populate: {
        path: "workouts.workout",
        model: "workout",
      },
    })
    .then((p) => res.send(p))
    .catch((error) => console.log(error));
};

const getName = async (req, res) => {
  console.log("teeeeeeeeeest23 " + req.body.email);
  User.find({ email: req.body.email })
    .select({ name: 1, _id: 0 })
    .then((p) => res.send(p))
    .catch((error) => console.log(error));
};

const assignPlan = async (req, res) => {
  try {
    const plan = await Plan.findOne({ planName: req.body.name });
    const userPlan = new Plan({
      _id: new mongoose.Types.ObjectId(),
      planName: plan.planName,
      workouts: plan.workouts,
    });
    const savedPlan = await userPlan.save();
    await User.findOneAndUpdate(
      { email: req.body.email },
      { plan: savedPlan._id }
    );
    res.send("done");
  } catch (error) {
    console.log(error);
    res.status(500).send("Internal server error");
  }
};

const updateStatus = async (req, res) => {
  User.findOne({ email: req.body.email }, (err, user) => {
    Plan.findOne({ _id: user.plan }, (err, plan) => {
      const workout = plan.workouts.find((w) =>
        w.workout.equals(req.body.workoutId)
      );
      console.log("ahoooooo ", workout);
      workout.status = "true";

      plan.save((err) => {
        if (err) {
          res.send(err);
        } else {
          res.send({
            success: true,
            message: "Workout status updated successfully",
          });
        }
      });
    });
  });
};
const addToUserHistory = async (req, res) => {
  User.findOneAndUpdate(
    { email: req.body.email },
    { $push: { history: req.body.record } },
    { new: true }
  )
    .then((p) => res.send(p))
    .catch((error) => console.log(error));
};
const getHistory = async (req, res) => {
  User.find({ email: req.body.email })
  .select({ history: 1, _id: 0 })
    .then((p) => res.send(p))
    .catch((error) => console.log(error));
};
const addRank= async(req,res)=>{
  const rank = new Rank(
    _.pick(req.body, [
       "user",
       "reps",
       "duration"
    ]));

   await rank.save()
  .then(() => console.log('Rank saved to database'))
  .catch((err) => console.error('Error saving user to database', err));
}
const getAllRanks = async (req, res) => {
  Rank
    .find()
    .then((result) => res.send(result))
    .catch((error) => console.log(error));
};

module.exports = {
  updateUser,
  getPlan,
  getName,
  updateStatus,
  assignPlan,
  addToUserHistory,
  getHistory,
  addRank,
  getAllRanks
};
