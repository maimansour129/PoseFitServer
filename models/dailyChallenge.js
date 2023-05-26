const { string } = require('joi');
const { uniqueId } = require('lodash');
const mongoose = require('mongoose');
const schema= mongoose.Schema;

const challengeSchema=new schema({
    workout: {
        type: mongoose.Schema.Types.ObjectId,
        ref: "workouts",
      },
    targetMuscele:{
        type:String,
    },
    Description:{
        type:String,
    },
    reps:{
        type:Number,
    },

    flag:{
        type:Boolean,
    }
});

const user = mongoose.model('dailyChallenge',challengeSchema);
module.exports=user;