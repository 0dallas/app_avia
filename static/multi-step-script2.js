const initializeClockCanvas = () => {
    const canvas = document.getElementById('clockCanvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let isDrawing = false;
    let lastX = 0;
    let lastY = 0;
    let drawingHistory = [];
    let currentPath = [];
    let isEraser = false;

    // Set initial canvas state
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 2;
    ctx.lineCap = 'round';

    // Draw initial circle
    ctx.beginPath();
    ctx.arc(150, 150, 140, 0, Math.PI * 2);
    ctx.stroke();

    function draw(e) {
        if (!isDrawing) return;

        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        ctx.beginPath();
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(x, y);
        ctx.stroke();

        currentPath.push({ x, y, isEraser });
        [lastX, lastY] = [x, y];
    }

    function startDrawing(e) {
        isDrawing = true;
        const rect = canvas.getBoundingClientRect();
        [lastX, lastY] = [e.clientX - rect.left, e.clientY - rect.top];
        currentPath = [];
        currentPath.push({ x: lastX, y: lastY, isEraser });
    }

    function stopDrawing() {
        if (isDrawing) {
            drawingHistory.push([...currentPath]);
            currentPath = [];
        }
        isDrawing = false;
    }

    // Event Listeners
    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseout', stopDrawing);

    // Button Functionality
    document.getElementById('eraserBtn')?.addEventListener('click', () => {
        isEraser = !isEraser;
        ctx.strokeStyle = isEraser ? '#fff' : '#000';
        document.getElementById('eraserBtn').classList.toggle('active');
    });

    document.getElementById('clearBtn')?.addEventListener('click', () => {
        clearPreviousDrawing();

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawingHistory = [];
        // Redraw initial circle
        ctx.beginPath();
        ctx.arc(150, 150, 140, 0, Math.PI * 2);
        ctx.stroke();
    });

    document.getElementById('undoBtn')?.addEventListener('click', () => {
        if (drawingHistory.length === 0) return;
        
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawingHistory.pop();
        
        // Redraw initial circle
        ctx.beginPath();
        ctx.arc(150, 150, 140, 0, Math.PI * 2);
        ctx.stroke();

        // Redraw remaining paths
        drawingHistory.forEach(path => {
            path.forEach((point, index) => {
                if (index === 0) {
                    ctx.beginPath();
                    ctx.moveTo(point.x, point.y);
                } else {
                    ctx.lineTo(point.x, point.y);
                }
                ctx.strokeStyle = point.isEraser ? '#fff' : '#000';
                ctx.stroke();
            });
        });
    });
};

function saveClockDrawing() {
    const canvas = document.getElementById('clockCanvas');
    if (!canvas) return;
    
    try {
        // Get the image data
        const imageData = canvas.toDataURL('image/png');
        
        // Save to sessionStorage with timestamp
        const saveData = {
            image: imageData,
            timestamp: new Date().getTime()
        };
        sessionStorage.setItem('clockDrawingData', JSON.stringify(saveData));
        
        // Immediately try to load it to verify save
        console.log('Drawing saved successfully');
    } catch (error) {
        console.error('Error saving drawing:', error);
    }
}

function clearPreviousDrawing() {
    sessionStorage.removeItem('clockDrawing');
}

// Add click handler to the "Continuar" button in the clock drawing step
document.querySelector('.step[data-step="44"] .btn-next').addEventListener('click', saveClockDrawing);
document.querySelector('.step[data-step="45"] .btn-next').addEventListener('click', loadClockDrawing);

// Function to load the saved drawing in the evaluation step
function loadClockDrawing() {
    try {
        // Get the saved data
        const savedDataString = sessionStorage.getItem('clockDrawingData');
        if (!savedDataString) {
            console.log('No saved drawing found');
            return;
        }

        const savedData = JSON.parse(savedDataString);
        const userClockImg = document.getElementById('userClockImage');
        
        if (userClockImg && savedData.image) {
            // Create a new image to ensure loading
            const tempImg = new Image();
            tempImg.onload = function() {
                userClockImg.src = this.src;
                console.log('Drawing loaded successfully');
            };
            tempImg.src = savedData.image;
        }
    } catch (error) {
        console.error('Error loading drawing:', error);
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('multi-step-form');
    const steps = form.querySelectorAll('.step');
    const progressBar = document.querySelector('.progress');
    const stepIndicators = document.querySelectorAll('.step-indicator span');
    const rememberRadios = document.getElementsByName('remembers_words');
    const wordInputStep = document.querySelector('.step[data-step="46"]');
    const clockStep = document.querySelector('.step[data-step="44"]');

    if (clockStep) {
        clearPreviousDrawing();
    }

    let currentStep = 0;

    initializeClockCanvas();

    const evaluationStep = document.querySelector('.step[data-step="47"]');
    if (evaluationStep) {
        loadClockDrawing();
    }

    rememberRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.value === 'no') {
                // If they don't remember, skip the input step
                wordInputStep.style.display = 'none';
                
                // Clear and disable the inputs
                const inputs = wordInputStep.querySelectorAll('input[type="text"]');
                inputs.forEach(input => {
                    input.value = '';
                    input.disabled = true;
                });
            } else {
                // If they do remember, show the input step
                wordInputStep.style.display = 'block';
                
                // Enable the inputs
                const inputs = wordInputStep.querySelectorAll('input[type="text"]');
                inputs.forEach(input => {
                    input.disabled = false;
                });
            }
        });
    });

    function showStep(stepIndex) {
        steps.forEach((step, index) => {
            step.classList.toggle('active', index === stepIndex);
        });
        updateProgress(stepIndex);
        toggleNextButton(stepIndex);

        const currentQuestionElement = document.getElementById('current-question');
        if (currentQuestionElement) {
            currentQuestionElement.textContent = stepIndex + 1;
        }

        // If you want to set total questions dynamically
        const totalQuestionsElement = document.getElementById('total-questions');
        if (totalQuestionsElement) {
            totalQuestionsElement.textContent = steps.length;
        }
    }

    function updateProgress(stepIndex) {
        const progress = ((stepIndex + 1) / steps.length) * 100;
        progressBar.style.width = `${progress}%`;

        stepIndicators.forEach((indicator, index) => {
            indicator.classList.toggle('active', index <= stepIndex);
        });
    }

    function nextStep() {
        if (currentStep < steps.length - 1) {
            currentStep++;
            showStep(currentStep);
        }
    }

    function prevStep() {
        if (currentStep > 0) {
            currentStep--;
            showStep(currentStep);
        }
    }

    function toggleNextButton(stepIndex) {
        const currentStepElement = steps[stepIndex];
        const requiredInputs = currentStepElement.querySelectorAll('input[required]');
        let allValid = true;

        requiredInputs.forEach(input => {
            if (input.type === 'radio') {
                const radioGroup = currentStepElement.querySelectorAll(`input[name="${input.name}"]:checked`);
                if (radioGroup.length === 0) {
                    allValid = false;
                }
            } else if (!input.value) {
                allValid = false;
            }
        });

        const nextButton = currentStepElement.querySelector('.btn-next');
        nextButton.disabled = !allValid;
        if (allValid) {
            nextButton.style.backgroundColor = '#34D399'; // Color habilitado
            nextButton.style.cursor = 'pointer';
        } else {
            nextButton.style.backgroundColor = '#ccc'; // Color deshabilitado
            nextButton.style.cursor = 'not-allowed';
        }
    }

    form.addEventListener('click', function (e) {
        if (e.target.classList.contains('btn-next')) {
            e.preventDefault();
            nextStep();
        } else if (e.target.classList.contains('btn-prev')) {
            e.preventDefault();
            prevStep();
        }
    });

    form.addEventListener('change', function (e) {
        toggleNextButton(currentStep);
    });

    // form.addEventListener('submit', function(e) {
    //     e.preventDefault();
    //     // Aquí puedes agregar el código para enviar los datos del formulario
    //     alert('Formulario enviado!');
    // });

    showStep(currentStep);
});
