import json
from operator import itemgetter

# Sample data input (replace with actual data reading if needed)
data = [
{"Image": "./testdata/frame_1493.jpg", "Person": "test test", "Description": "Congressman", "Similarity": 0.8136},
{"Image": "./testdata/frame_1487.jpg", "Person": "test test", "Description": "Congressman", "Similarity": 0.8546},
{"Image": "./testdata/frame_1475.jpg", "Person": "test test", "Description": "Congressman", "Similarity": 0.8273}
]

# Sort data by similarity in descending order
sorted_data = sorted(data, key=itemgetter("Similarity"), reverse=True)

# Generate HTML content
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Image Slider</title>
    <style>
        body, html {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background-color: #f0f0f0;
        }
        #slider {
            width: 80%;
            height: 500px;
            position: relative;
            overflow: hidden;
            border: 1px solid #ddd;
            background-color: #fff;
            margin-bottom: 20px;
        }
        .slide {
            position: absolute;
            width: 100%;
            height: 100%;
            opacity: 0;
            background-size: cover;
            background-position: center;
        }
        .active {
            opacity: 1;
        }
        #imageRange {
            width: 80%;
        }
    </style>
</head>
<body>
    <div id="slider">
"""

for i, entry in enumerate(sorted_data):
    html_content += f"""
        <div class="slide" style="background-image: url('{entry['Image']}');">
            <p>{entry['Person']} - {entry['Description']} - Similarity: {entry['Similarity']}</p>
        </div>
    """

html_content += """
    </div>
    <input type="range" id="imageRange" min="0" max="{max_index}" value="0">

    <script>
        const slides = document.getElementsByClassName('slide');
        const slider = document.getElementById('imageRange');
        let currentIndex = 0;

        function showSlide(index) {
            for (let i = 0; i < slides.length; i++) {
                slides[i].classList.remove('active');
            }
            slides[index].classList.add('active');
        }

        slider.addEventListener('input', (event) => {
            currentIndex = parseInt(event.target.value, 10);
            showSlide(currentIndex);
        });

        // Initialize the slider
        showSlide(currentIndex);
    </script>
</body>
</html>
""".replace("{max_index}", str(len(sorted_data) - 1))

# Write the HTML content to a file
with open("slider.html", "w") as file:
    file.write(html_content)

print("HTML file generated: slider.html")
print("HTML file generated: slider.html")
