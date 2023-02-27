const mongoose = require("mongoose");
const [User, validateUser] = require("../models/user");
const _ = require("lodash");
const bcrypt = require("bcrypt");
const jwt = require("jsonwebtoken");

function createToken(id) {
   return jwt.sign({ id }, "my private key");
}

const login = async (req, res) => {
   const { error } = validateUser(req.body);
   if (error) return res.status(400).send(error.details[0].message);

   try {
      let user = await User.findOne({ email: req.body.email });
      if (!user) return res.status(400).send("Invalid email or password");

      const isValidPassword = await bcrypt.compare(
         req.body.password,
         user.password
      );

      if (!isValidPassword)
         return res.status(400).send("Invalid email or password");

      const token = createToken(user._id);

      res.cookie("jwt", token);
      res.status(200).send(`Authenticated ${token}`);
   } catch (error) {
      console.log(error);
   }
};

const signup = async (req, res) => {
   const { error } = validateUser(req.body);

   if (error) return res.status(400).send(error.details[0].message);

   const user = new User(
      _.pick(req.body, [
         "email",
         "password",
         "name",
         "age",
         "targetWeight",
         "height",
         "weight",
      ])
   );

   const salt = await bcrypt.genSalt(10);
   user.password = await bcrypt.hash(user.password, salt);

   await user.save();

   const token = createToken(user._id);
   res.cookie("jwt", token);
  
   res.status(201).send(user);
};


const updateUser = async (req, res) => {
   const entries = Object.keys(req.body);
   const updates = {};
   for (let i = 0; i < entries.length; i++) {
      updates[entries[i]] = Object.values(req.body)[i];
   }

   let user = await User.findByIdAndUpdate(
      req.params.id,
      { $set: updates },
      { new: true }
   );

   console.log(user);
   if (user) {
      return res.status(201).send("done");
   }
   return res.status(400).send("not done");
};
module.exports = {
   login,
   signup,
   updateUser,
};
