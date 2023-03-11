const express = require("express");
const router = express.Router();

const {
    searchForWorkout,
    getAllWorkouts
} = require("../controllers/workoutController");

router.post("/search", searchForWorkout);
router.get("/allWorkouts",getAllWorkouts);

module.exports = router;