const express = require("express");
const router = express.Router();

const {
  login,
  register,
  updateUser,
} = require("../controllers/userController");

router.post("/login", login);

router.post("/register", register);

router.put("/:id", updateUser);

module.exports = router;
