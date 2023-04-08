const jwt = require("jsonwebtoken");
const [User] = require("../models/user");

const requireAuth = (req, res, next) => {
  const token = req.headers.cookie.split("=")[1];
  console.log("cookieeee " + req.headers.cookie);

  //console.log(req.headers.cookie.split("=")[1]);

  // check jwt exists and is verified
  if (token) {
    jwt.verify(token, "my private key", (err, decodedToken) => {
      if (err) {
        console.log(err.message);
        //res.redirect("/login");
      } else {
        console.log(decodedToken);
        next();
      }
    });
  } else {
    //res.redirect("/login");
  }
};

// check current user
const checkUser = (req, res, next) => {
  const token = req.cookies.jwt;
  let user;

  if (token) {
    jwt.verify(token, "my private key", async (err, decodedToken) => {
      if (err) {
        console.log(err.message);
        next();
      } else {
        console.log(decodedToken);
        user = await User.find({ _id: decodedToken.id });
        console.log(user);
        next();
      }
    });
  } else {
    next();
  }
};

module.exports = { requireAuth, checkUser };
