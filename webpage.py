
webpage = b"""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=0.5">
    <title>Spider Robot Control</title>
</head>
    <style>
    
        p {
            color: blue;
            text-align: center;
            font-family: arial;
            font-size: 15px;
        }     

        p1 {
            color: blue;
            text-align: left;
            font-family: arial;
            font-size: 12px;
        }     

        h1 {
            color: blue;
            text-align: center;
            font-family: arial;
            font-size: 20px;
        }

        body {
            width: 60%;
            height: 100vh;
            margin: 0;
            padding: 0;
            background: rgb(200, 200, 235);
        }
        
        .container {
            background-color: lightgrey;
            width: 525px;
            border: 2px solid blue;
            padding: 10px;
            margin: 10px;
            margin-top: 10px;
        }

        .container1 {
            align: center;
            background-color: lightgrey;
            width: 500px;
            border: 1px solid blue;
            padding: 5px;
            margin: 5px;
        }

        .radiocontainer {
            align: left;
            background-color: lightgrey;
            width: 150px;
            border: 1px solid blue;
            padding: 5px;
            margin: 5px;
        }

        .slidercontainer {
            align: center;
            background-color: lightgrey;
            width: 450px;
            border: 1px solid blue;
            padding: 5px;
            margin: 5px;
        }

        .button {
            width: 100px;
            color: blue;
            text-align: center;
            font-family: arial;
            font-size: 12px;
            padding: 5px 5px;
            margin: 5px;
            cursor: pointer;
            background: rgb(180, 180, 180);
        }
        
        .button1 {background-color: red}

        .slider {
            float: right;
            width: 300px;
            margin-top: 5px;
            font-size: 5px;
        }
    </style>
<body>
    <div class="container">
        <h1>SPIDER ROBOT CONTROL</h1>
        
        <div class="container1">
        <button class="button" id="safeBtn">SAFE</button>
        <button class="button" id="sitBtn">SIT</button>
        <button class="button" id="standBtn">STAND</button>
        <button class="button" id="shutdownBtn">POWERDOWN</button>
            <button class="button" id="quitBtn">QUIT</button>
        </div>
        <br>

        <div class="container1">
            <div class="radiocontainer"><p1>
                <input type="radio" name="gait" id="tripodgaitRadio" checked>
                <label for="tripod">TRIPOD</label>
                <input type="radio" name="gait" id="wavegaitRadio">
                <label for="wave">WAVE</label>
            </p1></div>

            <div class="slidercontainer"><p1>
            <label for="stepsizeSlider">STEP SIZE: <span id="stepsizeValue">60</span></label>
            <input type="range" min="20" max="100" value="60" class="slider" id="stepsizeSlider">
            </p1></div>
    
            <div class="slidercontainer"><p1>
            <label for="speedSlider">SPEED: <span id="speedValue">3</span></label>
            <input type="range" min="1" max="5" value="3" class="slider" id="speedSlider">
            </p1></div>
    
            <div class="slidercontainer"><p1>
            <label for="headingSlider">HEADING: <span id="headingValue">90</span></label>
            <input type="range" min="-180" max="180" value="90" class="slider" id="headingSlider">
            </p1></div>
    
            <div class="slidercontainer"><p1>
            <label for="turnSlider">TURN ANGLE: <span id="turnValue">0</span></label>
            <input type="range" min="-30" max="30" value="0" class="slider" id="turnSlider">
            </p1></div>
    
        </div>
        
        <div class="container1">
            <div class="slidercontainer"><p1>
            <label for="stepsSlider">STEPS: <span id="stepsValue">10</span></label>
            <input type="range" min="-25" max="25" value="10" class="slider" id="stepsSlider">
            </p1></div> 

            <div><p1>
            <button class="button" id="stopBtn">STOP!</button>
            </p1></div>
        </div>

    <script>
        document.getElementById('safeBtn').addEventListener('click', function() {
            spiderCommand('spider.safe()');
        });
        document.getElementById('sitBtn').addEventListener('click', function() {
            spiderCommand('spider.sit()');
        });
        document.getElementById('standBtn').addEventListener('click', function() {
            spiderCommand('spider.stand()');
        });
        document.getElementById('shutdownBtn').addEventListener('click', function() {
            spiderCommand('spider.shutdown()');
        });
        document.getElementById('stopBtn').addEventListener('click', function() {
            spiderCommand('spider.halt=True');
        });
        document.getElementById('quitBtn').addEventListener('click', function() {
            sendQuit();
        });
        document.getElementById('tripodgaitRadio').addEventListener('click', function() {
            updateWalk();
        });
        document.getElementById('wavegaitRadio').addEventListener('click', function() {
            updateWalk();
        });
        document.getElementById('speedSlider').addEventListener('input', function() {
            document.getElementById('speedValue').textContent = this.value;
        });
        document.getElementById('speedSlider').addEventListener('click', function() {
            updateWalk();
        });
        document.getElementById('stepsizeSlider').addEventListener('input', function() {
            document.getElementById('stepsizeValue').textContent = this.value;
        });
        document.getElementById('stepsizeSlider').addEventListener('click', function() {
            updateWalk();
        });
        document.getElementById('headingSlider').addEventListener('input', function() {
            document.getElementById('headingValue').textContent = this.value;
        });
        document.getElementById('headingSlider').addEventListener('click', function() {
            updateWalk();
        });
        document.getElementById('turnSlider').addEventListener('input', function() {
            document.getElementById('turnValue').textContent = this.value;
        });
        document.getElementById('turnSlider').addEventListener('click', function() {
            updateWalk();
        });
        document.getElementById('stepsSlider').addEventListener('input', function() {
            document.getElementById('stepsValue').textContent = this.value;
        });
        document.getElementById('stepsSlider').addEventListener('click', function() {
            walk();
        });

        function spiderCommand(command) {
            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/submit", true);
            xhr.setRequestHeader('Content-Type', 'text/plain');
            xhr.send(command);
        }

        function sendQuit() {
            var payload = "spider.quit";
            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/submit", true);
            xhr.setRequestHeader('Content-Type', 'text/plain');
            xhr.send(payload);
        }
        
        function updateWalk(){
            var selectedgait = 0;
            if (document.getElementById('wavegaitRadio').checked) {
                selectedgait = 1;
            }
            var speed = document.getElementById('speedSlider').value;
            var heading = document.getElementById('headingSlider').value * 0.01745;
            var turn = document.getElementById('turnSlider').value * 0.01745;
            var stepsize = document.getElementById('stepsizeSlider').value;
            var userData = 'gait=' + selectedgait + ', stepsize=' + stepsize;
            userData = userData + ', speed=' + speed +', heading=' + heading + ', turn=' + turn;
            var payload = "spider.setwalk(" + userData + ')';
            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/submit", true);
            xhr.setRequestHeader('Content-Type', 'text/plain');
            xhr.send(payload);        
        }
        
        function walk(){
            var payload = "spider.walk(" + document.getElementById('stepsSlider').value + ')';
            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/submit", true);
            xhr.setRequestHeader('Content-Type', 'text/plain');
            xhr.send(payload);
        }
        
    </script>
  </body>
</html>
"""
