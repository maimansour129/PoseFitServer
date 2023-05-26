const { number, boolean } = require("joi");
const { uniqueId } = require("lodash");
const mongoose = require("mongoose");
const schema = mongoose.Schema;

const planSchema = new schema({
  _id: mongoose.Schema.Types.ObjectId,
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
      status: {
        type: String,
        default: "false",
      },
    },
  ],
});

const user = mongoose.model("plan", planSchema);
module.exports = user;
