const mongoose = require("mongoose");
const [User, validateUser] = require("../models/user");
const _ = require("lodash");
const bcrypt = require("bcrypt");

const login = async (req, res) => {

   const { error } = validateUser(req.body);
   if (error) return res.status(400).send(error.details[0].message);

   let user = await User.findOne({ email: req.body.email });
   if (!user) return res.status(400).send("Invalid email or password");

   const isValidPassword = await bcrypt.compare(
      req.body.password,
      user.password
   );
   
   if (!isValidPassword)
      return res.status(400).send("Invalid email or password");

   res.status(200).send("Authenticated");

};

const register = async (req, res) => {
   const { error } = validateUser(req.body);

   if (error) {
      return res.status(400).send(error.details[0].message);
   }

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

   res.status(201).send(user);
};
module.exports = {
   login,
   register,
};
