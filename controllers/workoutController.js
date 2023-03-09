const mongoose = require("mongoose");
const workout = require("../models/workout");

const searchForWorkout=async(req,res)=>{
   workout.find({workoutName:{$regex:req.body.name,$options:"$i"}}).select({workoutName:1,gif:1 , _id:0})
   .then((p) => res.send(p))
    .catch((error) => console.log(error));
}

module.exports = {
    searchForWorkout
  };
  
