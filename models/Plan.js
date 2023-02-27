const { number } = require("joi");
const { uniqueId } = require("lodash");
const mongoose = require("mongoose");
const schema = mongoose.Schema;

const planSchema = new schema({
  planName: {
    type: String,
    required: true,
    uniqueId: true,
  },

  workouts: [
    {
      workout: {
        type: mongoose.Schema.Types.ObjectId,
        ref: "workouts",
      },
      rep: {
        type: Number,
      },
      sets: {
         type: Number,
       },
    },
  ],
});

const user = mongoose.model("plan", planSchema);
module.exports = user;
