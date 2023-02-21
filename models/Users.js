const mongoose = require('mongoose');
const schema= mongoose.Schema;

const userSchema=new schema({
    email:{
        type:String,
        required: true
    },
    name:
    {
        type:String,
       
    },
    password:{
        type:String,
        required: true
    },
    targetWeight:{
        type:Number,
        
    },
    activityProgress:{
        type:String,
       
    },
    age:{
        type:Number,
      
    },
    height:{
        type:Number,
        
    }

});

const user = mongoose.model('User',userSchema,'users');
module.exports=user;
