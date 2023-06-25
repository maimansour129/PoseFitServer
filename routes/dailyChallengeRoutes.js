const express = require("express");
const router = express.Router();
const {
    getDailyChallenge
  } = require("../controllers/dailyChallengeController");

router.get("/dailyChallenge", getDailyChallenge);


module.exports = router;