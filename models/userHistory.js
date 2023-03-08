const mongoose = require("mongoose");
const schema = mongoose.Schema;

const userHistorySchema = new schema({
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "User",
  },
  history:[{
    workoutName: {
        type: mongoose.Schema.Types.ObjectId,
        ref: "workouts",
      },
      reps: {
        type: Number,
      },
      date: {
        type: Date,
      },
  }]

});

const userHistory = mongoose.model("userHistory", userHistorySchema);
module.exports = userHistory;
