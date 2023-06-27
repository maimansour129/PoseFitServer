const express = require("express");
const router = express.Router();

const {
  updateUser,
  getPlan,
  getName,updateStatus,
  assignPlan,
  addToUserHistory,
  getHistory,
  addRank,
  getAllRanks,
  getInfo
} = require("../controllers/userController");



router.put("/update-user", updateUser);
router.post("/plan", getPlan);
router.post("/getName",getName);
router.put("/workoutStatus",updateStatus);
router.post("/assignPlan",assignPlan);
router.put("/addhistory",addToUserHistory);
router.post("/gethistory",getHistory);
router.post("/addRank",addRank);
router.get("/getRank",getAllRanks);
router.post("/getInfo",getInfo);







module.exports = router;
