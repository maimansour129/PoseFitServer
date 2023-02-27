const express = require("express");
const router = express.Router();

const {
  login,
  signup,
  updateUser,
} = require("../controllers/userController");

router.post("/login", login);

router.post("/register", signup);

router.put("/:id", updateUser);

module.exports = router;
