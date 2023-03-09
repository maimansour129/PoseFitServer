const express = require("express");
const router = express.Router();

const {
  login,
  signup,
  updateUser,
  getPlan
} = require("../controllers/userController");

router.post("/login", login);

router.post("/register", signup);

router.put("/:id", updateUser);
router.post("/plan", getPlan);

module.exports = router;
