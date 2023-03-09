const express = require("express");
const router = express.Router();

const {
    searchForWorkout
} = require("../controllers/workoutController");

router.post("/search", searchForWorkout);

module.exports = router;