const express = require('express');
const app=express();
const userRouter=require('./routes/userRout');
const bodyParser=require('body-parser');

app.use(express.json())
app.use(bodyParser.urlencoded({ extended: true }));
app.use('/user',userRouter);


app.post('/login',(req,res)=>{

    const user=req.body;
    if(user){
        return res.status(200).send('successfully');
    }
    res.status(400).send('canot accept');
})
app.post('/register',(req,res)=>{

    const user=req.body;
    if(user){
        return res.status(200).send('successfully');
    }
    res.status(400).send('canot accept');
});
app.listen(3000);