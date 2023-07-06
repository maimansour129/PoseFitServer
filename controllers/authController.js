const [User, validateUser] = require("../models/user");
const jwt = require("jsonwebtoken");
const _ = require("lodash");
const bcrypt = require("bcrypt");
const { log } = require("console");

const handleErrors = (err) => {
   console.log(err.message, err.code);
   let errors = "";

   //duplicate error code
   if (err.code === 11000) {
      errors = "This email is already registered";
      return errors;
   }

   //validation errors
   if (err.message.includes("user validation failed")) {
      Object.values(err.errors).forEach(
         ({ properties }) => (errors[properties.path] = properties.message)
      );
   }

   return errors;
};

const createToken = (id) => {
   return jwt.sign({ id }, "my private key");
};

module.exports.signup_post = async (req, res) => { 
   const { error } = validateUser(req.body);

   try {
      if (error) return res.status(400).send(error.details[0].message);

      const user = new User(
         _.pick(req.body, [
            "email",
            "password",
            "name",
            "age",
            "gender",
            "height",
            "weight",
            "plan",
            "activityLevel"
         ])
        
      );

      const salt = await bcrypt.genSalt(10);
      user.password = await bcrypt.hash(user.password, salt);

      await user.save();

      const token = createToken(user._id);
      res.cookie("jwt", token);

      res.status(201).send(user);
   } catch (err) {
      const errors = handleErrors(err);
      res.status(400).json({ errors });
   }
};

module.exports.login_post = async (req, res) => {
   const { email, password } = req.body;
   const user = await User.findOne({ email });

  if (user) {
    const auth = await bcrypt.compare(password, user.password);

    if (auth) {
      res.send("done")
    } else {
      console.log("hello3");
      res.send("Invalid email or password")

    }
  }
};

module.exports.logout_get = (req, res) => {
   res.clearCookie("jwt");
   res.send("Cleared cookie");
};
