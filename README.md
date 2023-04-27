# Idea-Generator
ATM VOD Idea Generator
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Atmosphere Video Compilation Ideas</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f3f3f3;
            text-align: center;
            padding: 50px;
        }
        h1 {
            font-size: 2rem;
            color: #333;
        }
        button {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
        }
        p#idea {
            font-size: 1.5rem;
            font-weight: bold;
            color: #666;
            margin-top: 30px;
        }
    </style>
</head>
<body>
    <h1>Atmosphere Video Compilation Ideas Generator</h1>
    <button id="generateIdeaBtn">Generate Idea</button>
    <p id="idea"></p>
    <script>
        const ideas = [
            'Nature and Wildlife Compilation',
            'City Skylines and Architecture Compilation',
            'Extreme Sports Highlights',
            'Underwater Adventures',
            'Aerial Drone Footage',
            'Breathtaking Landscapes',
            'Travel Destinations around the World',
            'Inspiring Time-lapses'
        ];
        document.getElementById('generateIdeaBtn').addEventListener('click', function() {
            const randomIdea = ideas[Math.floor(Math.random() * ideas.length)];
            document.getElementById('idea').innerHTML = randomIdea;
        });
    </script>
</body>
</html>
