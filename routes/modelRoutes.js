const express = require("express");
const router = express.Router();

const { bicepCurl, squat } = require("../controllers/modelController");

router.post("/bicepCurl", bicepCurl);
router.post("/squat", squat);

module.exports = router;
