const mongoose = require("mongoose");
const Joi = require("joi");
const bcrypt = require("bcrypt");

const userSchema = new mongoose.Schema({
  email: {
    type: String,
    required: true,
    unique: true,
  },
  password: {
    type: String,
    required: true,
    minlength: 8,
  },
  name: {
    type: String,
    required: true,
    minlength: 2,
    maxlenght: 1024,
  },
  gender: {
    type: String,
    required: true,
  },
  age: {
    type: Number,
    required: true,
  },
  height: {
    type: Number,
    required: true,
  },
  weight: {
    type: Number,
    required: true,
  },
  plan: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "plan",
    required: true,
  },
  activityLevel: {
    type: String,
    required: true,
  },
  history: [
    {
      workoutName: {
         type: String,
      },
      reps: {
        type: Number,
      },
      date: {
        type: Date,
      },
    },
  ],
});

function validateUser(user) {
  const schema = Joi.object({
    email: Joi.string().email(),
    password: Joi.string().min(8),
    name: Joi.string().min(2).max(1024),
    gender: Joi.string().min(0),
    age: Joi.number().min(0),
    weight: Joi.number().min(0),
    height: Joi.number().min(0),
    plan: Joi.string().min(0),
    activityLevel: Joi.string().min(0),
  });

  return schema.validate(user);
}

userSchema.statics.login = async function (email, password) {
  const user = await this.findOne({ email });
  console.log("in static login");

  if (user) {
    const auth = await bcrypt.compare(password, user.password);

    if (auth) {
      return user;
    } else {
      throw Error("Incorrect email or password");
    }
  }
};

const user = mongoose.model("User", userSchema);
module.exports = [user, validateUser];
