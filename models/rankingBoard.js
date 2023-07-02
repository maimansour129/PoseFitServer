const { string } = require('joi');
const { uniqueId } = require('lodash');
const { Double } = require('mongodb');
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
    },
    progress:{
        type:Number,
    }
});

const user = mongoose.model('rank',RanksSchema);
module.exports=user;