const { uniqueId } = require("lodash");
const mongoose = require("mongoose");
const schema = mongoose.Schema;

const workoutSchema = new schema({
  workoutName: {
    type: String,
    required: true,
    uniqueId: true,
  },
  gif: {
    type: String,
  },
  type:{
   type:string
  }
});

const user = mongoose.model("workout", workoutSchema);
module.exports = user;
