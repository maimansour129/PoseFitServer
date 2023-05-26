const jwt = require("jsonwebtoken");
const [User] = require("../models/user");
const dailyChallenge = require("../models/dailyChallenge");
const cron = require('node-cron');
const Plan = require("../models/Plan");
const mongoose = require("mongoose");

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

//cron.schedule('0 */5 * * *', () => {
//console.log('Generating daily challenge...');
//getDailyChallenge();
//});
var CronJob=require('cron').CronJob;

var cronJob1 = new CronJob({

    cronTime: '00 00 00 * * * ',
    onTick: function () {
    //Your code that is to be executed on every midnight
    setDailyChallenge();
    },
    start: true,
    runOnInit: false
});
const setDailyChallenge = async (req, res) => {
  console.log('getDailyChallenge called!');
  try {
    const result = await dailyChallenge.aggregate([{ $sample: { size: 1 } }]);
    await dailyChallenge.updateMany(
      { _id: { $ne: result[0]._id } },
      { $set: { flag: false } }
    );
    await dailyChallenge.findOneAndUpdate(
      { _id: result[0]._id },
      { $set: { flag: true } }
    );
    console.log(result[0]); // the randomly selected document
    res.send("success");
  } catch (error) {
    console.error(error);
  }
};

const getDailyChallenge = async (req, res) => {
  dailyChallenge.find({ flag: true })
  .populate({
    path: "workout",
    model: "workout"
  })
    .then((p) => res.send(p))
    .catch((error) => console.log(error));
};
module.exports = {
  updateUser,
  getPlan,
  getName,
  updateStatus,
  assignPlan,
  addToUserHistory,
  setDailyChallenge,
  getDailyChallenge
};
