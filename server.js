const express = require('express');
const app=express();
const userRouter=require('./routes/userRout');
const bodyParser=require('body-parser');

app.use(express.json())
app.use(bodyParser.urlencoded({ extended: true }));
app.use('/user',userRouter);


app.post('/login',(req,res)=>{

    const user=req.body;

    console.log('hi + ' + user.body.email +'hi')
    if(user){
        return res.send('new person added');
    }
    res.status(400).send('canot accept');
})
app.listen(3000);