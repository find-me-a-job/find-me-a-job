const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3032;

// Middleware
app.use(bodyParser.json());
app.use(express.static('public'));

// Route to handle form submission
app.post('/submit', (req, res) => {
    const { field, cities, experience } = req.body;

    const newData = {
        title: field,
        saved_location_list: cities,
        skill_stack: [], // Assuming this is to be updated separately or left empty
        experience: experience,
        favourite: [] // Assuming this is to be updated separately or left empty
    };

    fs.writeFile(path.join(__dirname, 'user_info.json'), JSON.stringify(newData, null, 2), (err) => {
        if (err) {
            console.error(err);
            return res.status(500).send('Server error');
        }
        res.status(200).send('Data saved successfully');
    });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
