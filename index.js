const express = require('express');
const app = express();
const Jimp = require('jimp');

app.get('/captcha', (req, res) => {
  const url = req.query.url;
  if (!url) {
    return res.status(400).send('Un URL est requise');
  }

  // Extract the characters from the URL
  const characters = url.toUpperCase().split('');

  // Create a new image
  Jimp.write('captcha.png', 200, 50)
    .then(() => {
      // Draw the characters onto the image
      characters.forEach((character, index) => {
        Jimp.loadFont(Jimp.FONT_SANS_32_WHITE)
          .then(font => {
            Jimp.text(character, 20 + (index * 35), 30, font, Jimp.RGBA(255, 255, 255, 255), (err) => {
              if (err) throw err;
            });
          });
      });

      // Send the captcha image as a response
      res.sendFile(__dirname + '/captcha.png');
    })
    .catch(err => {
      console.error(err);
      res.status(500).send('Erreur lors de la génération du captcha');
    });
});

app.listen(3000, () => {
  console.log('Serveur en ligne');
});