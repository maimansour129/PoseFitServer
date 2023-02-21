const mongoose = require("mongoose");
const User = require("../models/user");

const login = async (req, res) => {
   User.findOne(
      { email: req.body.email, password: req.body.password },
      function (error, user) {
         if (user === null) {
            res.status(200).send("not found");
         } else {
            res.status(404).send("found");
         }
      }
   );
};
const register = (req, res) => {
   const user = new User({
      email: req.body.email,

      password: req.body.password,
   });
   user
      .save()
      .then((result) => {
         res.send("User added");
      })
      .catch((err) => {
         console.log(err);
      });
};
module.exports = {
   login,
   register,
};
