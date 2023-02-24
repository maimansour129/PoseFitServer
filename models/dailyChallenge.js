const { uniqueId } = require('lodash');
const mongoose = require('mongoose');
const schema= mongoose.Schema;

const challengeSchema=new schema({
    date:{
        type:String,
       
    },
    // workout:{
    //     type: mongoose.Schema.Types.ObjectId, ref: 'workout'
    // },
    target:{
        type:number,
    }
});

const user = mongoose.model('challenge',challengeSchema);
module.exports=user;