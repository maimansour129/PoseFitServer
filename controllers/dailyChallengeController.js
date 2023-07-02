const dailyChallenge = require("../models/dailyChallenge");
const Rank=require("../models/rankingBoard");

var CronJob=require('cron').CronJob;

var cronJob1 = new CronJob({

    cronTime: '0 0 * * *',
    onTick: function () {
    setDailyChallenge();
    },
    start: true,
    runOnInit: false,
    timeZone: 'EET'
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
    )
    console.log(result[0]);
  } catch (error) {
    console.error(error);
  }
  Rank.deleteMany({})
  .catch((error) => console.log(error));
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
  