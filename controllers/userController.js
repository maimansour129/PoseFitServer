const jwt = require("jsonwebtoken");
const [User] = require("../models/user");
const Plan = require("../models/Plan");

function getUserToken(token) {
  const decodedToken = jwt.verify(token, "my private key");
  return decodedToken;
}

const updateUser = async (req, res) => {
  console.log("updating user");

  const updatedData = req.body;
  console.log(updatedData);
  let user;

  const decodedToken = getUserToken(req.cookies.jwt);
  //console.log(decodedToken);
  user = await User.findOneAndUpdate({ _id: decodedToken.id }, updatedData, {new: true});
  console.log(user);

  res.status(200).send(user);
};

const getPlan = async (req, res) => {
  console.log("teeeeeeeeeest " + req.body.email);
  User.find({ email: req.body.email })
    .select({ email: 1, _id: 0 })
    .populate({
      path: "plan",
      populate: {
        path: "workouts.workout",
        model: "workout",
      },
    })
    .then((p) => res.send(p))
    .catch((error) => console.log(error));
};

const getName = async (req, res) => {
  console.log("teeeeeeeeeest23 " + req.body.email);
  User.find({ email: req.body.email })
    .select({ name: 1, _id: 0 })
    .then((p) => res.send(p))
    .catch((error) => console.log(error));
};

module.exports = {
  updateUser,
  getPlan,
  getName,
};
