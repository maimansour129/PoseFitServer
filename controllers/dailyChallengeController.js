const dailyChallenge = require("../models/dailyChallenge");
const Rank=require("../models/rankingBoard");

var CronJob=require('cron').CronJob;

var cronJob1 = new CronJob({

    cronTime: '0 0 * * *',
    onTick: async function () {
    await dailyChallenge.updateMany({}, { $set: { flag: false } });
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
    console.log(result[0]);
    const updatedChallenge = await dailyChallenge.findByIdAndUpdate(
      result[0]._id,
      { $set: { flag: true } },
      { new: true }
    );
    console.log(updatedChallenge);
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
  