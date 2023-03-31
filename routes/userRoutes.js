const express = require("express");
const router = express.Router();

const {
  updateUser,
  getPlan,
  getName
} = require("../controllers/userController");


router.put("/:id", updateUser);
router.post("/plan", getPlan);
router.post("/getName",getName)


module.exports = router;
