const dailyChallenge = require("../models/dailyChallenge");

var CronJob=require('cron').CronJob;

var cronJob1 = new CronJob({

    cronTime: '00 00 00 * * * ',
    onTick: function () {
    //Your code that is to be executed on every midnight
    setDailyChallenge();
    },
    start: true,
    runOnInit: false
});
const setDailyChallenge = async (req, res) => {
  console.log('getDailyChallenge called!');
  try {
    const result = await dailyChallenge.aggregate([{ $sample: { size: 1 } }]);
    await dailyChallenge.updateMany(
      { _id: { $ne: result[0]._id } },
      { $set: { flag: false } }
    );
    await dailyChallenge.findOneAndUpdate(
      { _id: result[0]._id },
      { $set: { flag: true } }
    );
    console.log(result[0]); // the randomly selected document
    res.send("success");
  } catch (error) {
    console.error(error);
  }
};

const getDailyChallenge = async (req, res) => {
  dailyChallenge.find({ flag: true })
  .populate({
    path: "workout",
    model: "workout"
  })
    .then((p) => res.send(p))
    .catch((error) => console.log(error));
};

module.exports = {
  setDailyChallenge,
  getDailyChallenge,
};
  