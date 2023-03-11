const express = require("express");
const router = express.Router();

const {
  login,
  signup,
  updateUser,
  getPlan,
  getName
} = require("../controllers/userController");

router.post("/login", login);

router.post("/register", signup);

router.put("/:id", updateUser);
router.post("/plan", getPlan);
router.post("/getName",getName)


module.exports = router;
