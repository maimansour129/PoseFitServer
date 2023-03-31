const [User] = require("../models/user");
const Plan=require("../models/Plan");

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

const getPlan = async (req, res) => {
   console.log("teeeeeeeeeest "+(req.body.email));
   User.find({ email:req.body.email})
    .select({ email: 1, _id: 0 })
    .populate({
      path: "plan",
      populate: {
        path: "workouts.workout",
        model:"workout"
      },
    })
    .then((p) => res.send(p))
    .catch((error) => console.log(error));
};

const getName = async (req, res) => {
  console.log("teeeeeeeeeest23 "+(req.body.email));
  User.find({ email:req.body.email})
   .select({ name: 1, _id: 0 })
   .then((p) => res.send(p))
   .catch((error) => console.log(error));

   
};

module.exports = {
  updateUser,
  getPlan,
  getName,
};
