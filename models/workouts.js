const { uniqueId } = require('lodash');
const mongoose = require('mongoose');
const schema= mongoose.Schema;

const workoutSchema=new schema({
    WorkoutName:{
        type:String,
        required: true,
        uniqueId:true
    },
    Gif:
    {
        type:String,
       
    }
     
});

const user = mongoose.model('workout',workoutSchema,'users');
module.exports=user;