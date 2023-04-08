const axios = require("axios");

const bicepCurl = async (req, res) => {
  const imageFile = req.body;
  const imageStr = Buffer.from(imageFile.data).toString("base64");

  axios
    .post("http://127.0.0.1:5000/bicepCurl", imageStr, {
      headers: { "Content-Type": "application/json; charset=UTF-8" },
    })
    .then((response) => {
      res.send({
        reps: response.data.reps,
        correction: response.data.correction,
      });
    })
    .catch((err) => res.send(err));
};

const squat = async (req, res) => {
  const imageFile = req.body;
  const imageStr = Buffer.from(imageFile.data).toString("base64");

  axios
    .post("http://127.0.0.1:5000/squat", imageStr, {
      headers: { "Content-Type": "application/json; charset=UTF-8" },
    })
    .then((response) => {
      res.send({
        reps: response.data.reps,
        correction: response.data.correction,
      });
    })
    .catch((err) => res.send(err));
};

module.exports = {
  bicepCurl,
  squat,
};
