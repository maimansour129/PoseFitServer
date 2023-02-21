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
});

const user = mongoose.model("workout", workoutSchema);
module.exports = user;
