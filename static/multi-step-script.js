document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('multi-step-form');
    const steps = form.querySelectorAll('.step');
    const progressBar = document.querySelector('.progress');
    const stepIndicators = document.querySelectorAll('.step-indicator span');
    const nextButtons = form.querySelectorAll('.btn-next');
    let currentStep = 0;
    function showStep(stepIndex) {
        steps.forEach((step, index) => {
            step.classList.toggle('active', index === stepIndex);
        });
        updateProgress(stepIndex);
        toggleNextButton(stepIndex);
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
    form.addEventListener('click', function(e) {
        if (e.target.classList.contains('btn-next')) {
            e.preventDefault();
            nextStep();
        } else if (e.target.classList.contains('btn-prev')) {
            e.preventDefault();
            prevStep();
        }
    });
    form.addEventListener('change', function(e) {
        toggleNextButton(currentStep);
    });
    // form.addEventListener('submit', function(e) {
    //     e.preventDefault();
    //     // Aquí puedes agregar el código para enviar los datos del formulario
    //     alert('Formulario enviado!');
    // });
    showStep(currentStep);
});