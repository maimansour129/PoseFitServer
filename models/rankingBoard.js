const { string } = require('joi');
const { uniqueId } = require('lodash');
const mongoose = require('mongoose');
const schema= mongoose.Schema;

const RanksSchema=new schema({
    user: {
        type: mongoose.Schema.Types.ObjectId,
        ref: "users",
    },
    reps:{
        type:Number,
    },

    duration:{
        type:Number,
    }
});

const user = mongoose.model('rank',RanksSchema);
module.exports=user;